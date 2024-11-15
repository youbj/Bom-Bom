from openai import AsyncOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage
from confluent_kafka import Producer
from aiokafka import AIOKafkaProducer
import asyncio
import json
import logging
from typing import Dict, Optional, Tuple
from datetime import datetime
from app.config import settings
from app.models.schema import (
    SpeakerType, EmotionalState, RiskLevel,
    SentimentAnalysis, RiskAssessment
)

logger = logging.getLogger(__name__)
        
class GPTService:
    def __init__(self):
        """GPT 서비스 초기화"""
        self.client = AsyncOpenAI(api_key=settings.gpt.api_key)
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        self.producer = None
        self.response_topic = settings.kafka.conversation_topic
        
        self.system_prompt = """당신은 노인과 대화하는 AI 상담사입니다.
            
            다음 원칙을 반드시 따라주세요:

            1. 사용자의 입력을 주의 깊게 듣고 공감적으로 응답합니다
            2. 이전 대화 내용을 참고하여 맥락에 맞는 질문을 합니다
            3. 한 번에 하나의 간단하고 명확한 질문만 합니다
            4. 질문은 대화 마지막에 자연스럽게 포함시킵니다
            5. 노인의 건강, 기분, 일상생활에 관심을 보입니다
            6. 위험 신호(우울, 고립, 건강 악화 등)를 주의깊게 관찰합니다

            응답 형식:
            1. 먼저 사용자의 이야기에 대한 공감과 이해를 표현합니다
            2. 필요한 경우 조언이나 지지를 제공합니다
            3. 상대가 비관적인 응답을 한다면 먼저 위로를 제공합니다.
            4. 마지막에 반드시 이전 대화 맥락을 고려하여 자연스러운 후속 질문을 덧붙입니다

            예시:
            사용자: "오늘 날씨가 좋아서 산책했어요."
            AI: "날씨 좋은 날 산책하시니 기분이 좋으셨겠어요. 산책은 건강에도 매우 좋죠. 
            평소에도 자주 산책을 하시는 편인가요?"

            위와 같은 형식으로 자연스럽게 대화를 이어가주세요."""
    
    async def initialize(self):
        """비동기 초기화"""
        if not self.producer:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=settings.kafka.bootstrap_servers,
                client_id='gpt_service_producer'
            )
            await self.producer.start()
        
    async def analyze_conversation(self, text: str) -> Dict:
        """사용자 입력 분석"""
        try:
            completion = await self.client.chat.completions.create(
                model=settings.gpt.model_name,
                messages=[
                    {"role": "system", "content": "노인 대화 분석 전문가입니다."},
                    {"role": "user", "content": f"""다음 텍스트를 분석해주세요: "{text}"
                    
                    JSON 형식으로 응답해주세요:
                    {{
                        "sentiment": {{
                            "score": 0부터 100 사이의 숫자로 감정 점수,
                            "is_positive": true 또는 false로 긍정/부정 여부,
                            "confidence": 0부터 1 사이의 숫자로 신뢰도,
                            "emotional_state": "positive", "negative", "neutral", "concerned" 중 하나로 감정 상태,
                            "emotion_score": 0부터 100 사이의 숫자로 감정 강도,
                            "description": "감정 상태에 대한 설명"
                        }},
                        "risk": {{
                            "level": "none", "low", "medium", "high" 중 하나로 위험 수준,
                            "factors": ["위험 요소들"],
                            "actions": ["필요한 조치사항들"]
                        }},
                        "keywords": ["주요 키워드들"],
                        "summary": "대화 내용 요약"
                    }}"""}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            analysis = json.loads(completion.choices[0].message.content)
            return analysis
            
        except Exception as e:
            logger.error(f"Conversation analysis failed: {str(e)}")
            return self._get_default_analysis()

    async def generate_response( self, user_message: str, conversation_id: str, memory_id: str, senior_id: int,
        is_initial: bool = False) -> Dict:
        start_time = datetime.now()
        logger.info(f"=== Starting request at: {start_time.isoformat()} ===")

        try:
            if is_initial:
                response_text = "안녕하세요! 오늘 하루는 어떻게 보내고 계신가요?"
                self.memory.save_context({"input": ""}, {"output": response_text})
                user_analysis = self._get_default_analysis()
                # Kafka 데이터 전송
                kafka_data = {
                    "response_text": response_text,
                    "senior_id": senior_id,
                    "conversation_id": conversation_id,
                    "timestamp": datetime.now().isoformat()
                }
                kafka_sent = await self.send_to_kafka(kafka_data)

                # 처리 시간 계산
                total_duration = (datetime.now() - start_time).total_seconds()

                return {
                    "response_text": response_text,
                    "conversation_id": conversation_id,
                    "memory_id": memory_id,
                    "kafka_sent": kafka_sent,
                    "user_analysis": user_analysis,
                    "mysql_data": None,
                    "timestamp": datetime.now().isoformat(),
                    "processing_times": {
                        "total_time": total_duration
                    }
                }
            else:
                # 1. AI 응답 생성 (최우선)
                logger.info("1. Generating AI response...")
                response_start = datetime.now()
                chat_history = self.memory.load_memory_variables({}).get("chat_history", [])
                messages = [{"role": "system", "content": self.system_prompt}]

                for message in chat_history[-6:]:
                    if isinstance(message, HumanMessage):
                        messages.append({"role": "user", "content": message.content})
                    elif isinstance(message, AIMessage):
                        messages.append({"role": "assistant", "content": message.content})

                messages.append({"role": "user", "content": user_message})

                completion = await self.client.chat.completions.create(
                    model=settings.gpt.model_name,
                    messages=messages,
                    temperature=0.7
                )
                response_text = completion.choices[0].message.content
                
                self.memory.save_context({"input": user_message}, {"output": response_text})
                response_time = datetime.now()
                response_duration = (response_time - response_start).total_seconds()
                logger.info(f"Response generated in {response_duration:.2f}s")

                # 2. 응답 검증
                logger.info("2. Validating response...")
                validation_start = response_time
                validation_result = await self.validate_response(response_text, user_message)
                validation_time = datetime.now()
                validation_duration = (validation_time - validation_start).total_seconds()
                logger.info(f"Validation completed in {validation_duration:.2f}s")

                # 3. Kafka로 즉시 전송
                logger.info("3. Sending to Kafka...")
                kafka_start = datetime.now()
                kafka_data = {
                    "response_text": response_text,
                    "senior_id": senior_id,
                    "conversation_id": conversation_id,
                    "timestamp": datetime.now().isoformat()
                }
                kafka_sent = await self.send_to_kafka(kafka_data)
                kafka_time = datetime.now()
                kafka_duration = (kafka_time - kafka_start).total_seconds()
                logger.info(f"Kafka message sent in {kafka_duration:.2f}s")

                # 4. 사용자 입력 분석 (백그라운드)
                logger.info("4. Starting background analysis...")
                analysis_start = datetime.now()
                # 비동기로 분석 시작
                analysis_task = asyncio.create_task(self.analyze_conversation(user_message))

                # 다른 작업 계속 진행
                self.memory.save_context(
                    {"input": user_message},
                    {"output": response_text}
                )

                # 분석 결과 기다리기
                user_analysis = await analysis_task
                analysis_time = datetime.now()
                analysis_duration = (analysis_time - analysis_start).total_seconds()
                logger.info(f"Background analysis completed in {analysis_duration:.2f}s")

            # MySQL 데이터 준비
            mysql_data = {
                'memory_id': memory_id,
                'conversation_id': conversation_id,
                'speaker': SpeakerType.AI,
                'content': response_text,
                'summary': user_analysis.get('summary'),
                'positivity_score': user_analysis.get('sentiment', {}).get('score'),
                'keywords': json.dumps(user_analysis.get('keywords', []), ensure_ascii=False),
                'response_plan': '[]'
            }

            total_duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"=== Total processing time: {total_duration:.2f}s ===")

            return {
                "response_text": response_text,
                "conversation_id": conversation_id,
                "memory_id": memory_id,
                "kafka_sent": kafka_sent,
                "mysql_data": mysql_data,
                "user_analysis": user_analysis,
                "timestamp": datetime.now().isoformat(),
                "processing_times": {
                    "response_generation_time": response_duration,
                    "validation_time": validation_duration,
                    "kafka_time": kafka_duration,
                    "analysis_time": analysis_duration,
                    "total_time": total_duration
                }
            }

        except Exception as e:
            end_time = datetime.now()
            logger.error(f"Response generation failed after {(end_time - start_time).total_seconds()}s: {str(e)}")
            return self._get_error_response(conversation_id, memory_id)
    
        except Exception as e:
            end_time = datetime.now()
            logger.error(f"Response generation failed after {(end_time - start_time).total_seconds()}s: {str(e)}")
            return self._get_error_response(conversation_id, memory_id)
        
    def _get_error_response(self, conversation_id: str, memory_id: str) -> Dict:
        """에러 응답 생성"""
        return {
            "response_text": "죄송합니다. 일시적인 오류가 발생했습니다. 다시 말씀해 주시겠어요?",
            "conversation_id": conversation_id,
            "memory_id": memory_id,
            "timestamp": datetime.now().isoformat(),
            "user_analysis": self._get_default_analysis(),
            "kafka_sent": False,
            "mysql_data": None
        }
        
    def _get_default_analysis(self) -> Dict:
        """기본 분석 결과 반환"""
        return {
            "sentiment": {
                "score": 50.0,
                "is_positive": True,
                "confidence": 0.0,
                "emotional_state": "neutral",
                "emotion_score": 50.0,
                "description": "분석 실패"
            },
            "risk": {
                "level": "none",
                "factors": [],
                "actions": []
            },
            "keywords": [],
            "summary": "분석 실패"
        }

    async def validate_response(self, response: str, context: str = "", elderly_state: Dict = None) -> Dict:
        """응답의 적절성 검증"""
        try:
            completion = await self.client.chat.completions.create(
                model=settings.gpt.model_name,
                messages=[
                    {"role": "system", "content": "응답 검증 전문가입니다."},
                    {"role": "user", "content": f"""다음 응답의 적절성을 검증해주세요:
                    
응답: {response}
맥락: {context}

다음 항목들을 0에서 5점 사이로 평가하여 JSON 형식으로 응답해주세요:

{{
    "scores": {{
        "empathy": "공감도 점수 (0-5)",
        "clarity": "명확성 점수 (0-5)",
        "appropriateness": "적절성 점수 (0-5)",
        "safety": "안전성 점수 (0-5)",
        "usefulness": "유용성 점수 (0-5)"
    }},
    "suggestions": ["개선이 필요한 사항들"],
    "strengths": ["잘된 점들"]
}}"""}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )

            validation_result = json.loads(completion.choices[0].message.content)
            
            # 평균 점수 계산 및 유효성 판단
            scores = validation_result.get("scores", {})
            if scores:
                average_score = sum(float(score) for score in scores.values()) / len(scores)
                validation_result["average_score"] = round(average_score, 2)
                validation_result["is_valid"] = average_score >= 3.0
            else:
                validation_result["is_valid"] = True  # 기본값

            logger.info(f"Response validation result: {validation_result}")
            return validation_result
            
        except Exception as e:
            logger.error(f"검증 실패 in gpt_service: {str(e)}")
            return {
                "is_valid": True,
                "scores": {
                    "empathy": 3,
                    "clarity": 3,
                    "appropriateness": 3,
                    "safety": 3,
                    "usefulness": 3
                },
                "average_score": 3.0,
                "suggestions": [],
                "strengths": []
            }

    async def send_to_kafka(self, data: Dict) -> bool:
        try:
            if not self.producer:
                await self.initialize()

            # 비동기적으로 메시지 전송
            await self.producer.send_and_wait(
                self.response_topic,
                json.dumps(data).encode('utf-8')
            )
            logger.info(f'Message sent to Kafka topic: {self.response_topic}')
            return True
        except Exception as e:
            logger.error(f"Failed to send message to Kafka: {str(e)}")
            return False
        
    def reset_memory(self):
        """메모리 초기화"""
        try:
            if hasattr(self, 'memory'):
                self.memory.clear()
        except Exception as e:
            logger.error(f"Error in reset_memory: {e}")

    async def aclose(self):
        """비동기 정리"""
        try:
            if self.producer:
                await self.producer.stop()
                self.producer = None
            self.reset_memory()
        except Exception as e:
            logger.error(f"Error in aclose: {e}")

    def __del__(self):
        """소멸자"""
        try:
            self.reset_memory()
        except Exception as e:
            logger.error(f"Error in destructor: {e}")
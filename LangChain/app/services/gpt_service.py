from openai import AsyncOpenAI
from langchain.memory import ConversationBufferMemory
from confluent_kafka import Producer
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
            return_messages=True,
            input_key="input",
            output_key="output"
        )
        
        # Kafka Producer 초기화
        self.kafka_config = {
            'bootstrap.servers': settings.kafka.bootstrap_servers,
            'client.id': 'gpt_service_producer'
        }
        self.producer = Producer(self.kafka_config)
        self.response_topic = settings.kafka.conversation_topic
        
        self.system_prompt = """당신은 노인과 대화하는 AI 상담사입니다.
            
            다음 원칙을 반드시 따라주세요:
            1. 사용자의 입력을 주의 깊게 듣고 공감적으로 응답합니다
            2. 이전 대화 내용을 참고하여 맥락에 맞는 질문을 합니다
            3. 한 번에 하나의 간단하고 명확한 질문만 합니다
            4. 질문은 대화 마지막에 자연스럽게 포함시킵니다
            5. 노인의 건강, 기분, 일상생활에 관심을 보입니다
            6. 위험 신호(우울, 고립, 건강 악화 등)를 주의깊게 관찰합니다
            7. 대화가 8번 이상 이어진 경우, 다음 규칙을 따릅니다:
                - 이전 대화 내용을 간단히 요약합니다
                - 긍정적인 마무리 멘트를 합니다
                - 다음에 또 이야기 나누자는 따뜻한 인사로 마무리합니다
                - 더 이상 질문은 하지 않습니다"""

    async def analyze_input(self, text: str) -> Dict:
        """사용자 입력 분석 (ConversationAnalyzer와 동일한 포맷 사용)"""
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
            
            # 스키마에 맞게 변환
            return {
                'sentiment_analysis': SentimentAnalysis(
                    score=float(analysis['sentiment']['score']),
                    is_positive=analysis['sentiment']['is_positive'],
                    confidence=float(analysis['sentiment']['confidence']),
                    emotional_state=analysis['sentiment']['emotional_state'],
                    emotion_score=float(analysis['sentiment']['emotion_score']),
                    emotion_description=analysis['sentiment']['description']
                ).dict(),
                
                'risk_assessment': RiskAssessment(
                    risk_level=RiskLevel(analysis['risk']['level']),
                    risk_factors=analysis['risk']['factors'],
                    needed_actions=analysis['risk']['actions']
                ).dict(),
                
                'keywords': analysis['keywords'],
                'summary': analysis['summary']
            }
            
        except Exception as e:
            logger.error(f"Input analysis failed: {str(e)}")
            return self._get_default_analysis()

    async def generate_response(
        self, 
        user_message: str,
        conversation_id: int,
        memory_id: int,
        is_initial: bool = False
    ) -> Dict:
        """응답 생성 및 처리"""
        try:
            # 1. 사용자 입력 분석
            analysis_result = await self.analyze_input(user_message)
            
            # 2. 응답 생성
            if is_initial:
                response_text = "안녕하세요! 오늘 하루는 어떻게 보내고 계신가요?"
            else:
                messages = [
                    {"role": "system", "content": self.system_prompt}
                ]
                
                # 대화 히스토리 추가
                chat_history = self.memory.load_memory_variables({}).get("chat_history", [])
                if chat_history:
                    history_text = "\n".join([
                        f"{'User' if msg.type == 'human' else 'Assistant'}: {msg.content}"
                        for msg in chat_history[-3:]
                    ])
                    messages.append({"role": "user", "content": f"이전 대화:\n{history_text}"})
                
                messages.append({"role": "user", "content": user_message})
                
                response = await self.client.chat.completions.create(
                    model=settings.gpt.model_name,
                    messages=messages,
                    temperature=0.7
                )
                response_text = response.choices[0].message.content

            # 3. 응답 검증
            is_valid, validation_result = await self.validate_response(response_text, user_message)
            
            if not is_valid:
                logger.warning(f"Response validation failed: {validation_result}")
                return self._get_error_response(conversation_id, memory_id)

            # 4. MySQL 저장용 데이터 준비
            memory_data = {
                'memory_id': memory_id,
                'conversation_id': conversation_id,
                'speaker': SpeakerType.AI,
                'content': response_text,
                'summary': analysis_result['summary'],
                'positivity_score': analysis_result['sentiment_analysis']['score'],
                'keywords': json.dumps(analysis_result['keywords']),
                'response_plan': json.dumps(analysis_result['risk_assessment']['needed_actions'])
            }

            # 5. Kafka 전송 데이터 준비
            kafka_data = {
                "conversation_id": conversation_id,
                "memory_id": memory_id,
                "response_text": response_text,
                "analysis": analysis_result,
                "validation": validation_result,
                "timestamp": datetime.now().isoformat()
            }

            # 6. Kafka로 전송
            kafka_success = await self.send_to_kafka(kafka_data)
            if not kafka_success:
                logger.error("Failed to send message to Kafka")

            # 7. 메모리 업데이트
            self.memory.save_context(
                {"input": user_message},
                {"output": response_text}
            )

            # 8. 결과 반환 (MySQL 저장용 데이터 포함)
            return {
                "response_text": response_text,
                "conversation_id": conversation_id,
                "memory_id": memory_id,
                "analysis": analysis_result,
                "validation": validation_result,
                "kafka_sent": kafka_success,
                "memory_saved": True,
                "mysql_data": memory_data  # ConversationManager에서 사용
            }

        except Exception as e:
            logger.error(f"Response generation failed: {str(e)}")
            return self._get_error_response(conversation_id, memory_id)

    def _get_default_analysis(self) -> Dict:
        """기본 분석 결과 반환 (ConversationAnalyzer와 동일한 포맷)"""
        return {
            'sentiment_analysis': SentimentAnalysis(
                score=50.0,
                is_positive=True,
                confidence=0.0,
                emotional_state=EmotionalState.NEUTRAL,
                emotion_score=50.0,
                emotion_description="분석 실패"
            ).dict(),
            
            'risk_assessment': RiskAssessment(
                risk_level=RiskLevel.NONE,
                risk_factors=[],
                needed_actions=[]
            ).dict(),
            
            'keywords': [],
            'summary': "분석 실패"
        }

    def delivery_report(self, err, msg):
        """Kafka 전송 결과 콜백"""
        if err is not None:
            logger.error(f'Message delivery failed: {err}')
        else:
            logger.info(f'Message delivered to {msg.topic()} [{msg.partition()}]')

    async def validate_response(self, response: str, context: str = "", elderly_state: Dict = None) -> Dict:
        """응답의 적절성 검증"""
        try:
            validation_prompt = fr"""다음 응답의 적절성을 검증하여 JSON 형식으로 응답해주세요:
            
            응답: {response}
            맥락: {context}
            노인 상태: {json.dumps(elderly_state, ensure_ascii=False) if elderly_state else "정보 없음"}
            
            다음 기준으로 평가해주세요:
            1. 공감도: 노인의 감정과 상황에 대한 이해를 보여주는가
            2. 명확성: 이해하기 쉽고 간단한 언어를 사용했는가
            3. 적절성: 노인의 현재 상태와 맥락에 맞는 응답인가
            4. 안전성: 위험 신호에 적절히 대응했는가
            5. 유용성: 실질적인 도움이나 의미 있는 대화를 제공하는가"""

            completion = await self.client.chat.completions.create(
                model=settings.gpt.model_name,
                messages=[
                    {"role": "system", "content": "응답 검증 전문가입니다."},
                    {"role": "user", "content": validation_prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )

            validation_result = json.loads(completion.choices[0].message.content)
            logger.info(f"Response validation result: {validation_result}")
            return validation_result
            
        except Exception as e:
            logger.error(f"Validation failed: {str(e)}")
            return {
                "scores": {
                    "empathy": 3,
                    "clarity": 3,
                    "appropriateness": 3,
                    "safety": 3,
                    "usefulness": 3
                },
                "average_score": 3.0,
                "improvements_needed": [],
                "strengths": []
            }

    async def send_response_to_kafka(self, response_data: Dict) -> bool:
        """Kafka로 응답 전송"""
        try:
            self.producer.produce(
                self.response_topic,
                value=json.dumps(response_data).encode('utf-8'),
                callback=self.delivery_report
            )
            self.producer.flush(timeout=5)
            return True
        except Exception as e:
            logger.error(f"Failed to send message to Kafka: {str(e)}")
            return False
    def reset_memory(self):
        """메모리 초기화"""
        if hasattr(self, 'memory'):
            self.memory.clear()
            
        # Kafka producer 정리
        if hasattr(self, 'producer'):
            self.producer.flush()

    async def aclose(self):
        """비동기 정리"""
        self.reset_memory()
        # 추가적인 비동기 정리 작업이 필요한 경우 여기에 구현

    def __del__(self):
        """소멸자"""
        self.reset_memory()
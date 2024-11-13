from openai import AsyncOpenAI
from langchain.memory import ConversationBufferMemory
from confluent_kafka import Producer
import asyncio
import json
import logging
from typing import Dict, Optional
from datetime import datetime
from app.config import settings

logger = logging.getLogger(__name__)

class GPTService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.gpt.api_key)
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            input_key="input",
            output_key="output"
        )
        
        # System Prompt 정의
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
        
        # Kafka 설정
        self.kafka_config = {
            'bootstrap.servers': settings.kafka.bootstrap_servers,
            'client.id': 'gpt_service_producer'
        }
        self.producer = Producer(self.kafka_config)
        self.response_topic = 'ai_responses'

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

    async def analyze_conversation(self, user_message: str, response_text: str) -> Dict:
        """대화 분석 수행"""
        try:
            analysis_prompt = f"""다음 대화를 분석해주세요:
            사용자: {user_message}
            AI: {response_text}
            
            다음 형식으로 JSON 응답을 제공해주세요:
            {{
                "summary": "대화 요약",
                "positivity_score": 0-100 사이의 감정 점수,
                "keywords": ["주요 키워드들"],
                "response_plan": ["대처 방안들"]
            }}"""

            completion = await self.client.chat.completions.create(
                model=settings.gpt.model_name,
                messages=[
                    {"role": "system", "content": "대화 분석 전문가입니다."},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            return json.loads(completion.choices[0].message.content)
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            return {
                "summary": "",
                "positivity_score": 50,
                "keywords": [],
                "response_plan": []
            }

    async def generate_response(
        self, 
        user_message: str, 
        conversation_id: int,
        memory_id: int,
        is_initial: bool = False
    ) -> Dict:
        """응답 생성 및 처리"""
        try:
            # 1. 응답 생성
            if is_initial:
                response_text = "안녕하세요! 오늘 하루는 어떻게 보내고 계신가요?"
            else:
                chat_history = self.memory.load_memory_variables({}).get("chat_history", [])
                recent_history = chat_history[-3:] if len(chat_history) > 3 else chat_history
                
                context = "\n".join([
                    f"{'User' if msg.type == 'human' else 'Assistant'}: {msg.content}"
                    for msg in recent_history
                ])
                
                response = await self.client.chat.completions.create(
                    model=settings.gpt.model_name,
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": f"이전 대화:\n{context}\n\n사용자: {user_message}"}
                    ],
                    temperature=0.7
                )
                response_text = response.choices[0].message.content

            # 2. 응답 검증
            validation_task = asyncio.create_task(
                self.validate_response(response_text, user_message)
            )

            # 3. Kafka로 응답 전송
            response_data = {
                "response_text": response_text,
                "conversation_id": conversation_id,
                "memory_id": memory_id,
                "timestamp": datetime.now().isoformat()
            }
            kafka_task = asyncio.create_task(
                self.send_response_to_kafka(response_data)
            )

            # 4. 대화 분석 수행
            analysis_task = asyncio.create_task(
                self.analyze_conversation(user_message, response_text)
            )

            # 5. 모든 작업 완료 대기
            validation_result = await validation_task
            await kafka_task
            analysis_result = await analysis_task

            # 6. Memory 컨텍스트 업데이트
            self.memory.save_context(
                {"input": user_message},
                {"output": response_text}
            )

            # 7. 최종 응답 데이터 구성
            return {
                "response_text": response_text,
                "conversation_id": conversation_id,
                "memory_id": memory_id,
                "validation": validation_result,
                "analysis": analysis_result
            }

        except Exception as e:
            logger.error(f"Response generation failed: {str(e)}")
            return {
                "response_text": "죄송합니다. 일시적인 오류가 발생했습니다. 다시 말씀해 주시겠어요?",
                "conversation_id": conversation_id,
                "memory_id": memory_id,
                "validation": {
                    "scores": {"empathy": 3, "clarity": 3, "appropriateness": 3, "safety": 3, "usefulness": 3},
                    "average_score": 3.0,
                    "improvements_needed": [],
                    "strengths": []
                },
                "analysis": {
                    "summary": "",
                    "positivity_score": 50,
                    "keywords": [],
                    "response_plan": []
                }
            }

    def reset_memory(self):
        """메모리 초기화"""
        self.memory.clear()

    def __del__(self):
        """소멸자: Kafka Producer 정리"""
        if hasattr(self, 'producer'):
            self.producer.flush()
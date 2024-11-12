from openai import OpenAI
from langchain.agents import Tool, create_openai_functions_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.memory import ConversationBufferMemory
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
import json
import logging
import asyncio
from typing import Dict, List, Optional
from app.config import settings
from app.models.schema import EmotionalState, RiskLevel

logger = logging.getLogger(__name__)

class ValidateResponseArgs(BaseModel):
    response: str = Field(..., description="검증할 응답 텍스트")
    context: str = Field(default="", description="대화 맥락 (선택사항)")

class AnalyzeConversationArgs(BaseModel):
    message: str = Field(..., description="분석할 메시지")

class GPTService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.gpt.api_key)
        self.llm = ChatOpenAI(temperature=0.7, model=settings.gpt.model_name)
        
        # 1. Memory 초기화 수정
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            input_key="input",  # 입력 키 명시
            output_key="output"  # 출력 키 명시
        )

        # 프롬프트 템플릿
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""당신은 노인과 대화하는 AI 상담사입니다.
            
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
            3. 마지막에 반드시 이전 대화 맥락을 고려하여 자연스러운 후속 질문을 덧붙입니다

            예시:
            사용자: "오늘 날씨가 좋아서 산책했어요."
            AI: "날씨 좋은 날 산책하시니 기분이 좋으셨겠어요. 산책은 건강에도 매우 좋죠. 
            평소에도 자주 산책을 하시는 편인가요?"

            위와 같은 형식으로 자연스럽게 대화를 이어가주세요."""),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessage(content="{text}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        # 3. 도구 정의는 동일하게 유지
        self.tools = [
            StructuredTool(
                name="validate_response",
                func=self._validate_response,
                coroutine=self._validate_response,
                description="생성된 응답의 적절성을 검증합니다",
                args_schema=ValidateResponseArgs
            ),
            StructuredTool(
                name="analyze_conversation",
                func=self._analyze_single_message,
                coroutine=self._analyze_single_message,
                description="사용자의 메시지를 분석하고 감정 상태와 위험도를 평가합니다",
                args_schema=AnalyzeConversationArgs
            )
        ]

        # 4. 에이전트 설정
        self.agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        # 5. AgentExecutor 설정
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            max_iterations=3,
            early_stopping_method="generate",
            handle_parsing_errors=True,
            return_intermediate_steps=False  # 중간 단계 반환 비활성화
        )
        
    async def _validate_response(self, response: str, context: str = "") -> Dict:
        """응답의 적절성 검증"""
        try:
            validation_prompt = f"""다음 응답의 적절성을 검증하여 JSON 형식으로 응답해주세요:
            
            응답: {response}
            
            다음 형식으로 응답하세요:
            {{
                "적절성_점수": 1-5 사이의 점수,
                "명확성_점수": 1-5 사이의 점수,
                "공감도_점수": 1-5 사이의 점수,
                "개선필요사항": ["개선점1", "개선점2"]
            }}
            """
            
            validation_response = self.client.chat.completions.create(
                model=settings.gpt.model_name,
                messages=[{"role": "user", "content": validation_prompt}],
                temperature=0.3,
                response_format={ "type": "json_object" }
            )
            logger.info(f"Analysis result: {validation_response.choices[0].message.content}")
            return json.loads(validation_response.choices[0].message.content)
        
        except Exception as e:
            logger.error(f"응답 검증 실패: {str(e)}")
            return {
                "적절성_점수": 3,
                "명확성_점수": 3,
                "공감도_점수": 3,
                "개선필요사항": []
            }
            
    async def _analyze_single_message(self, message: str) -> Dict:
        """단일 메시지 분석용 래퍼 함수"""
        try:
            analysis_prompt = f"""다음 메시지를 분석해 JSON 형식으로만 응답해주세요:

            메시지: {message}

            다음 형식으로만 응답하세요:
            {{
                "감정_상태": "긍정적/부정적/중립적/우려됨",
                "감정_수치": 숫자(0.00 ~ 100.00 사이의 수치),
                "감정_설명": "수치에 대한 설명 (예: 80.50은 매우 긍정적, 30.25는 다소 부정적)",
                "위험_수준": "없음/낮음/중간/높음",
                "주요_키워드": ["키워드1", "키워드2"],
                "필요_조치사항": ["조치1", "조치2"]
            }}

            감정 수치 산정 기준:
            - 0.00 ~ 20.00: 매우 부정적인 감정 상태
            - 20.01 ~ 40.00: 부정적인 감정 상태
            - 40.01 ~ 60.00: 중립적인 감정 상태
            - 60.01 ~ 80.00: 긍정적인 감정 상태
            - 80.01 ~ 100.00: 매우 긍정적인 감정 상태

            소수점 둘째자리까지 표현해 주세요.
            """
            analysis_response = self.client.chat.completions.create(
                model=settings.gpt.model_name,
                messages=[{"role": "user", "content": analysis_prompt}],
                temperature=0.3,
                response_format={ "type": "json_object" }
            )
            logger.info(f"Analysis result: {analysis_response.choices[0].message.content}")
            return json.loads(analysis_response.choices[0].message.content)
        except Exception as e:
            logger.error(f"메시지 분석 실패: {str(e)}")
            return {
                "감정_상태": "중립적",
                "감정_수치": {
                    "긍정": 0.01,
                    "부정": 0.01
                },
                "위험_수준": "없음",
                "주요_키워드": [],
                "필요_조치사항": []
            }

    async def _analyze_conversation(self, user_message: str, gpt_response: str) -> Dict:
        """대화 내용 분석"""
        try:
            analysis_prompt = f"""다음 대화를 분석해 JSON 형식으로만 응답해주세요:

            사용자: {user_message}
            AI: {gpt_response}

            다음 형식으로만 응답하세요:
            {{
                "감정_상태": "긍정적/부정적/중립적/우려됨",
                "감정_수치": 숫자(0.00 ~ 100.00 사이의 수치),
                "감정_설명": "수치에 대한 설명",
                "위험_수준": "없음/낮음/중간/높음",
                "주요_키워드": ["키워드1", "키워드2"],
                "필요_조치사항": ["조치1", "조치2"]
            }}

            감정 수치 산정 기준:
            - 0.00 ~ 20.00: 매우 부정적인 감정 상태
            - 20.01 ~ 40.00: 부정적인 감정 상태
            - 40.01 ~ 60.00: 중립적인 감정 상태
            - 60.01 ~ 80.00: 긍정적인 감정 상태
            - 80.01 ~ 100.00: 매우 긍정적인 감정 상태

            소수점 둘째자리까지 표현해 주세요.
            """
            
            analysis_response = self.client.chat.completions.create(
                model=settings.gpt.model_name,
                messages=[{"role": "user", "content": analysis_prompt}],
                temperature=0.3,
                response_format={ "type": "json_object" }
            )
            logger.info(f"Analysis result: {analysis_response.choices[0].message.content}")
            return json.loads(analysis_response.choices[0].message.content)
        except Exception as e:
            logger.error(f"응답 분석 실패: {str(e)}")
            return {
                "감정_상태": "중립적",
                "감정_수치": 50.00,
                "위험_수준": "없음",
                "주요_키워드": [],
                "필요_조치사항": []
            }

    async def generate_response(self, user_message: str, is_initial: bool = False) -> Dict:
        try:
            if is_initial:
                response_text = "안녕하세요! 오늘 하루는 어떻게 보내고 계신가요?"
            else:
                # 메모리에서 이전 대화 내용 로드
                chat_history = self.memory.load_memory_variables({}).get("chat_history", [])
                logger.info(f"Loaded chat history: {chat_history}")

                # 대화 히스토리를 GPT 메시지 형식으로 변환
                chat_messages = [
                    {"role": "system", "content": self.prompt.messages[0].content}
                ]

                # 이전 대화 내용 추가
                for message in chat_history:
                    if isinstance(message, HumanMessage):
                        chat_messages.append({"role": "user", "content": message.content})
                    else:
                        chat_messages.append({"role": "assistant", "content": message.content})

                # 현재 사용자 메시지 추가
                chat_messages.append({"role": "user", "content": user_message})

                # GPT 응답 생성
                response = self.client.chat.completions.create(
                    model=settings.gpt.model_name,
                    messages=chat_messages,
                    temperature=0.7,
                    max_tokens=150
                )

                response_text = response.choices[0].message.content.strip()
                logger.info(f"Generated response: {response_text}")

                # Memory 저장
                self.memory.save_context(
                    {"input": user_message},
                    {"output": response_text}
                )

            # 나머지 분석 작업...
            tasks = [
                self._validate_response(response_text),
                self._analyze_single_message(user_message) if not is_initial else None,
                self._analyze_conversation(user_message if not is_initial else "", response_text)
            ]

            results = await asyncio.gather(*[task for task in tasks if task is not None])

            return {
                "response_text": response_text,
                "validation": results[0],
                "user_analysis": results[1] if not is_initial else {
                    "감정_상태": "중립적",
                    "감정_수치": 50.00,
                    "위험_수준": "없음",
                    "주요_키워드": [],
                    "필요_조치사항": []
                },
                "conversation_analysis": results[-1]
            }

        except Exception as e:
            logger.error(f"Response generation failed: {str(e)}", exc_info=True)
            raise
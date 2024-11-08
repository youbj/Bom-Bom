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
        
        # Memory 초기화
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        # 도구 정의 -> StructuredTool로 변경하여 비동기 지원
        self.tools = [
            StructuredTool(
                name="validate_response",
                func=self._validate_response,
                coroutine=self._validate_response,  # 비동기 함수 지정
                description="생성된 응답의 적절성을 검증합니다",
                args_schema=ValidateResponseArgs
            ),
            StructuredTool(
                name="analyze_conversation",
                func=self._analyze_single_message,
                coroutine=self._analyze_single_message,  # 비동기 함수 지정
                description="사용자의 메시지를 분석하고 감정 상태와 위험도를 평가합니다",
                args_schema=AnalyzeConversationArgs
            )
        ]
        
        # 프롬프트 템플릿
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""당신은 노인과 대화하는 AI 상담사입니다.
            다음 원칙을 반드시 따라주세요:

            1. 천천히, 명확하고 간단한 질문을 합니다
            2. 한 번에 하나의 질문만 합니다
            3. 노인의 건강, 기분, 일상생활에 관심을 보입니다
            4. 위험 신호(우울, 고립, 건강 악화 등)를 주의깊게 관찰합니다
            5. 공감적이고 지지적인 태도를 유지합니다
            6. 이전 대화 내용을 기억하고 자연스럽게 이어갑니다

            대화 시에는:
            1. 먼저 이전 대화를 참고하여 맥락을 파악합니다
            2. 적절한 응답을 생성합니다
            3. 노인의 감정 상태를 0.00~100.00 사이의 수치로 정밀하게 분석합니다
            4. 위험 신호를 주의깊게 관찰합니다"""),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessage(content="{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

        # 에이전트 생성
        self.agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        # 에이전트 실행기 초기화
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            max_iterations=3,
            early_stopping_method="force",
            handle_parsing_errors=True,
            return_intermediate_steps=True
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

    async def generate_response(self,
                        user_message: str,
                        recent_context: Optional[List[str]] = None) -> Dict:
        """GPT를 사용하여 응답 생성"""
        try:
            # 1. Agent로 응답 생성
            agent_response = await self.agent_executor.ainvoke({
                "input": user_message
            })

            response_text = agent_response["output"]
            logger.info(f"Agent response: {response_text}")

            # 2. 응답 검증
            validation = await self._validate_response(response_text)
            logger.info(f"Validation result: {validation}")

            # 3. 먼저 사용자 메시지 분석
            user_analysis = await self._analyze_single_message(user_message)
            logger.info(f"User message analysis: {user_analysis}")

            # 4. 전체 대화 분석
            conversation_analysis = await self._analyze_conversation(user_message, response_text)
            logger.info(f"Full conversation analysis: {conversation_analysis}")

            # Agent의 중간 단계 결과 로깅
            if "intermediate_steps" in agent_response:
                logger.info(f"Intermediate steps: {agent_response['intermediate_steps']}")

            # Memory에 대화 저장
            self.memory.save_context(
                {"input": user_message},
                {"output": response_text}
            )

            # 5. 모든 분석 결과를 포함하여 반환
            return {
                "response_text": response_text,
                "validation": validation,
                "user_analysis": user_analysis,
                "conversation_analysis": conversation_analysis,
                "intermediate_steps": agent_response.get("intermediate_steps", [])
            }

        except Exception as e:
            logger.error(f"GPT 응답 생성 실패: {str(e)}", exc_info=True)  # 상세한 에러 정보 로깅
            raise

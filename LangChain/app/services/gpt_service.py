from openai import OpenAI
from langchain.agents import Tool, create_openai_functions_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage
import json
import logging
from typing import Dict, List, Optional
from app.config import settings
from app.models.schema import EmotionalState, RiskLevel

logger = logging.getLogger(__name__)

class GPTService:
    def __init__(self):
        """GPT 서비스 초기화"""
        self.client = OpenAI(api_key=settings.gpt.api_key)
        self.conversation_context = []
        self.llm = ChatOpenAI(temperature=0.7, model=settings.gpt.model_name)
        
        # 도구 정의
        self.tools = [
            Tool(
                name="validate_response",
                func=self._validate_response,
                description="생성된 응답이 대화 맥락에 적절한지 검증합니다."
            ),
            Tool(
                name="summarize_user_response",
                func=self._summarize_user_response,
                description="사용자의 응답을 요약합니다."
            ),
            Tool(
                name="analyze_conversation",
                func=self._analyze_conversation,
                description="대화 내용을 분석하여 감정 상태와 위험도를 평가합니다."
            )
        ]
        
        # 프롬프트 템플릿 생성
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""
                당신은 노인과 대화하는 AI 상담사입니다. 다음 원칙을 따라주세요:

                1. 천천히, 명확하고 간단한 질문을 합니다.
                2. 질문은 반드시 한번에 하나의 질문만 합니다.
                3. 노인의 건강, 기분, 일상생활에 관심을 보입니다.
                4. 위험 신호(우울, 고립, 건강 악화 등)를 주의깊게 관찰합니다.
                5. 대화는 자연스럽게 이어가되, 필요한 정보를 얻을 수 있도록 합니다.
                6. 공감적이고 지지적인 태도를 유지합니다.
                7. 대화를 갑자기 바꾸지 말고 자연스럽게 이어가세요.

                각 응답 후에는 반드시:
                1. 응답의 적절성을 검증하고
                2. 사용자의 답변을 요약하여 저장하고
                3. 대화 내용을 분석하세요.
            """),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessage(content="{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
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
            verbose=True,
            handle_parsing_errors=True
        )

    async def _validate_response(self, response: str, context: str) -> Dict:
        """응답의 적절성 검증"""
        try:
            validation_prompt = f"""
            다음 대화 맥락과 응답을 검증해주세요:
            
            맥락: {context}
            응답: {response}
            
            다음 기준으로 평가해주세요:
            1. 맥락 적절성 (1-5)
            2. 질문의 명확성 (1-5)
            3. 공감도 (1-5)
            4. 개선사항
            
            JSON 형식으로 응답해주세요.
            """
            
            validation_response = await self.client.chat.completions.create(
                model=settings.gpt.MODEL_NAME,
                messages=[{"role": "user", "content": validation_prompt}],
                temperature=0.3
            )
            
            return json.loads(validation_response.choices[0].message.content)
        except Exception as e:
            logger.error(f"응답 검증 실패: {str(e)}")
            return {
                "context_relevance": 3,
                "question_clarity": 3,
                "empathy_level": 3,
                "improvements_needed": []
            }

    async def _summarize_user_response(self, user_message: str) -> Dict:
        """사용자 응답 요약"""
        try:
            summary_prompt = f"""
            다음 사용자의 응답을 요약해주세요:
            
            응답: {user_message}
            
            다음 항목들을 추출해주세요:
            1. 핵심 내용
            2. 주요 키워드
            3. 표현된 감정이나 태도
            
            JSON 형식으로 응답해주세요.
            """
            
            summary_response = await self.client.chat.completions.create(
                model=settings.gpt.MODEL_NAME,
                messages=[{"role": "user", "content": summary_prompt}],
                temperature=0.3
            )
            
            return json.loads(summary_response.choices[0].message.content)
        except Exception as e:
            logger.error(f"응답 요약 실패: {str(e)}")
            return {
                "core_content": "",
                "keywords": [],
                "expressed_emotions": []
            }

    async def _analyze_conversation(self, user_message: str, gpt_response: str) -> Dict:
        """대화 내용 분석"""
        try:
            analysis_prompt = f"""
            다음 대화를 분석해주세요:
            
            사용자: {user_message}
            AI: {gpt_response}
            
            다음 항목들을 평가해주세요:
            1. 감정 상태 (positive/negative/neutral/concerned)
            2. 위험 수준 (none/low/medium/high)
            3. 주요 키워드나 중요 정보
            4. 필요한 조치사항
            
            JSON 형식으로 응답해주세요.
            """
            
            analysis_response = await self.client.chat.completions.create(
                model=settings.gpt.MODEL_NAME,
                messages=[{"role": "user", "content": analysis_prompt}],
                temperature=0.3
            )
            
            return json.loads(analysis_response.choices[0].message.content)
        except Exception as e:
            logger.error(f"응답 분석 실패: {str(e)}")
            return {
                "emotional_state": EmotionalState.NEUTRAL,
                "risk_level": RiskLevel.NONE,
                "keywords": [],
                "actions_needed": []
            }

    async def generate_response(self,
                            user_message: str,
                            recent_context: Optional[List[str]] = None) -> Dict:
        """GPT를 사용하여 응답 생성"""
        try:
            # Agent를 사용하여 응답 생성 및 검증
            agent_response = await self.agent_executor.ainvoke({
                "input": user_message,
                "chat_history": recent_context or []
            })
            
            response_text = agent_response["output"]
            
            # 응답 검증
            validation = await self._validate_response(response_text, str(recent_context))
            
            # 사용자 응답 요약
            summary = await self._summarize_user_response(user_message)
            
            # 대화 분석
            analysis = await self._analyze_conversation(user_message, response_text)
            
            # 컨텍스트 업데이트
            if recent_context is not None:
                self.conversation_context = recent_context[-3:] + [user_message, response_text]
            else:
                self.conversation_context = [user_message, response_text]
            
            return {
                "response_text": response_text,
                "validation": validation,
                "user_response_summary": summary,
                "analysis": analysis
            }
            
        except Exception as e:
            logger.error(f"GPT 응답 생성 실패: {str(e)}")
            raise
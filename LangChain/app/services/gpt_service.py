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
from datetime import datetime
from app.config import settings
from app.models.schema import (
    EmotionalState, RiskLevel, HealthStatus,
    SentimentAnalysis, RiskAssessment, HealthMetrics
)

logger = logging.getLogger(__name__)

class ValidateResponseArgs(BaseModel):
    response: str = Field(..., description="검증할 응답 텍스트")
    context: str = Field(default="", description="대화 맥락 (선택사항)")
    elderly_state: Dict = Field(default_factory=dict, description="노인의 현재 상태 정보")

class AnalyzeMessageArgs(BaseModel):
    message: str = Field(..., description="분석할 메시지")
    conversation_history: List[Dict] = Field(default_factory=list, description="이전 대화 기록")
    
# Pydantic 모델 정의
class AnalysisOutput(BaseModel):
    emotional_analysis: dict = Field(..., description="감정 상태 분석")
    risk_assessment: dict = Field(..., description="위험 수준 평가")
    health_indicators: dict = Field(..., description="건강 지표")
    social_relationships: List[str] = Field(..., description="사회적 관계")
    daily_activities: List[str] = Field(..., description="일상 활동")
    main_concerns: List[str] = Field(..., description="주요 관심사")
    keywords: List[str] = Field(..., description="키워드")

class ResponseOutput(BaseModel):
    response: str = Field(..., description="실제 응답 텍스트")
    intent: str = Field(..., description="응답의 의도")
    focus_areas: List[str] = Field(..., description="주의 깊게 본 영역들")
    suggested_actions: List[str] = Field(..., description="제안된 행동이나 조치들")
    next_topics: List[str] = Field(..., description="다음에 다룰만한 주제들")

class ValidationOutput(BaseModel):
    scores: dict = Field(..., description="평가 점수")
    average_score: float = Field(..., description="평균 점수")
    improvements_needed: List[str] = Field(..., description="개선 필요 사항")
    strengths: List[str] = Field(..., description="강점")
    

class GPTService:
    def __init__(self):
        """GPT 서비스 초기화"""
        self.llm = ChatOpenAI(
            temperature=0.7, 
            model=settings.gpt.model_name,
            api_key=settings.gpt.api_key
        )
        
        # Memory 초기화
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            input_key="input",
            output_key="output"
        )

        self.system_prompt = """"당신은 노인과 대화하는 AI 상담사입니다.
            
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

            위와 같은 형식으로 자연스럽게 대화를 이어가주세요.
        """

        # 프롬프트 템플릿 수정
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=self.system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessage(content="{text}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        # 도구 정의 업데이트
        self.tools = [
            StructuredTool(
                name="validate_response",
                func=self._validate_response,
                coroutine=self._validate_response,
                description="생성된 응답의 적절성을 검증합니다",
                args_schema=ValidateResponseArgs
            ),
            StructuredTool(
                name="analyze_message",
                func=self._analyze_message,
                coroutine=self._analyze_message,
                description="사용자의 메시지를 분석하고 상태를 평가합니다",
                args_schema=AnalyzeMessageArgs
            )
        ]

        # 에이전트 설정
        self.agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        # AgentExecutor 설정
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            max_iterations=3,
            early_stopping_method="generate",
            handle_parsing_errors=True
        )

    async def _validate_response(self, response: str, context: str = "", elderly_state: Dict = None) -> Dict:
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
            5. 유용성: 실질적인 도움이나 의미 있는 대화를 제공하는가
            
            다음 형식으로 응답하세요:
            {{
                "scores": {{
                    "empathy": "1-5 사이의 점수",
                    "clarity": "1-5 사이의 점수",
                    "appropriateness": "1-5 사이의 점수",
                    "safety": "1-5 사이의 점수",
                    "usefulness": "1-5 사이의 점수"
                }},
                "average_score": "평균 점수",
                "improvements_needed": ["개선필요사항1", "개선필요사항2"],
                "strengths": ["강점1", "강점2"]
            }}
            """
            
            validation_response = await self.llm.ainvoke(validation_prompt)
            result = json.loads(validation_response.content)
            
            logger.info(f"Response validation result: {result}")
            return result
        
        except Exception as e:
            logger.error(f"Response validation failed: {str(e)}")
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

    async def _analyze_message(self, message: str, conversation_history: List[Dict] = None) -> Dict:
        """메시지 분석"""
        try:
            analysis_prompt = fr"""다음 메시지와 대화 맥락을 분석해 JSON 형식으로 응답해주세요:

                메시지: "{message}"
                대화 기록: {json.dumps(conversation_history, ensure_ascii=False) if conversation_history else "없음"}

                다음을 포함하여 분석해주세요:
                1. 감정 상태와 강도
                2. 위험 신호와 수준
                3. 건강 관련 언급
                4. 사회적 관계 관련 내용
                5. 일상생활 활동
                6. 주요 관심사나 걱정거리

                다음 형식으로 응답하세요:
                {{
                    "emotional_analysis": {{
                        "state": "감정 상태",
                        "intensity": "0-100 사이의 수치",
                        "description": "상세 설명"
                    }},
                    "risk_assessment": {{
                        "level": "NONE/LOW/MEDIUM/HIGH",
                        "factors": ["위험요소1", "위험요소2"],
                        "needed_actions": ["필요조치1", "필요조치2"]
                    }},
                    "health_indicators": {{
                        "physical": ["신체건강 관련 내용"],
                        "mental": ["정신건강 관련 내용"],
                        "sleep": ["수면 관련 내용"],
                        "appetite": ["식욕 관련 내용"]
                    }},
                    "social_relationships": ["관계1", "관계2"],
                    "daily_activities": ["활동1", "활동2"],
                    "main_concerns": ["걱정거리1", "걱정거리2"],
                    "keywords": ["키워드1", "키워드2"]
                }}"""

            # LangChain ChatOpenAI 대신 직접 OpenAI API 호출
            response = await self.llm.ainvoke(
                [
                    SystemMessage(content="노인 대화 분석 전문가입니다."),
                    HumanMessage(content=analysis_prompt)
                ]
            )
            
            result = json.loads(response.content)
            logger.info(f"Message analysis result: {result}")

            return result

        except Exception as e:
            logger.error(f"Message analysis failed: {str(e)}")
            return {
                "emotional_analysis": {
                    "state": "NEUTRAL",
                    "intensity": 50,
                    "description": "분석 실패"
                },
                "risk_assessment": {
                    "level": "NONE",
                    "factors": [],
                    "needed_actions": []
                },
                "health_indicators": {
                    "physical": [],
                    "mental": [],
                    "sleep": [],
                    "appetite": []
                },
                "social_relationships": [],
                "daily_activities": [],
                "main_concerns": [],
                "keywords": []
            }

    async def generate_response(self, user_message: str, is_initial: bool = False) -> Dict:
        """응답 생성"""
        try:
            if is_initial:
                initial_response = {
                    "response_text": "안녕하세요! 오늘 하루는 어떻게 보내고 계신가요?",
                    "response_data": {
                        "intent": "greeting",
                        "focus_areas": ["일상생활", "기분"],
                        "suggested_actions": ["경청", "공감"],
                        "next_topics": ["하루 일과", "건강 상태"]
                    }
                }
                return initial_response

            # 이전 대화 내용 로드
            chat_history = self.memory.load_memory_variables({}).get("chat_history", [])
            
            # 메시지 분석
            analysis_result = await self._analyze_message(
                user_message,
                [{"role": m.type, "content": m.content} for m in chat_history]
            )
            
            # GPT에 전달할 프롬프트 구성
            response_prompt = fr"""이전 대화와 분석 결과를 고려하여 응답을 생성해주세요:

            사용자 메시지: {user_message}
            
            분석 결과: {json.dumps(analysis_result, ensure_ascii=False)}
            
            다음 사항을 고려하여 응답해주세요:
            1. 감정 상태에 맞는 공감적 반응
            2. 위험 수준에 따른 적절한 대응
            3. 건강 상태에 대한 관심
            4. 사회적 관계 지원
            5. 일상활동 격려
            
            응답은 다음 형식의 JSON으로 작성해주세요:
            {{
                "response": "실제 응답 텍스트",
                "intent": "응답의 의도",
                "focus_areas": ["주의 깊게 본 영역들"],
                "suggested_actions": ["제안된 행동이나 조치들"],
                "next_topics": ["다음에 다룰만한 주제들"]
            }}
            """

            response = await self.llm.ainvoke(response_prompt)
            response_data = json.loads(response.content)
            
            # 응답 검증
            validation_result = await self._validate_response(
                response_data['response'],
                context=user_message,
                elderly_state=analysis_result
            )
            
            # Memory 업데이트
            self.memory.save_context(
                {"input": user_message},
                {"output": response_data['response']}
            )
            
            return {
                "response_text": response_data['response'],
                "response_data": response_data,
                "analysis": analysis_result,
                "validation": validation_result
            }

        except Exception as e:
            logger.error(f"Response generation failed: {str(e)}", exc_info=True)
            return {
                "response_text": "죄송합니다. 잠시 문제가 발생했습니다. 다시 한 번 말씀해 주시겠어요?",
                "response_data": {
                    "intent": "error_handling",
                    "focus_areas": [],
                    "suggested_actions": ["재시도"],
                    "next_topics": []
                },
                "analysis": {},
                "validation": {}
            }

    def reset_memory(self):
        """대화 기록 초기화"""
        self.memory.clear()
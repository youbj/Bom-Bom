
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from typing import Dict
import logging
from app.config import settings
from app.services.tools import InterviewTools
from app.models.schema import ChatResponse

logger = logging.getLogger(__name__)

class InterviewAgent:
    def __init__(self):
        """에이전트 초기화"""
        self.llm = ChatOpenAI(
            model_name=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        self.tools = InterviewTools()
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        self.agent = initialize_agent(
            tools=self.tools.get_tools(),
            llm=self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True
        )
        
        system_prompt = """
        당신은 전문적인 인터뷰어입니다. 사용자와 자연스러운 대화를 통해 깊이 있는 이야기를 이끌어내세요.
        
        다음 원칙을 따르세요:
        1. 사용자의 답변을 깊이 있게 분석하세요
        2. 맥락에 맞는 후속 질문을 생성하세요
        3. 공감적이고 지지적인 태도를 유지하세요
        4. 한 번에 하나의 주제에 집중하세요
        """
        self.agent.agent.system_message = system_prompt

    def process_message(self, user_message: str) -> ChatResponse:
        """사용자 메시지 처리"""
        try:
            # 감정 분석
            analysis = self.tools.analyze_response(user_message)
            
            # 토픽 추출
            topics = self.tools.extract_topics(user_message)
            
            # 다음 질문 생성
            prompt = f"""
            다음 정보를 바탕으로 적절한 후속 질문을 생성해주세요:
            
            사용자 메시지: {user_message}
            감정 분석: {analysis}
            관련 토픽: {topics}
            
            질문은 하나만 생성하고, 자연스러운 대화체로 작성해주세요.
            """
            
            response = self.agent.run(prompt)
            
            return ChatResponse(
                message=response,
                analysis={
                    "sentiment": analysis,
                    "topics": topics
                }
            )
        
        except Exception as e:
            logger.error(f"메시지 처리 실패: {str(e)}")
            return ChatResponse(
                message="죄송합니다. 메시지 처리 중 오류가 발생했습니다."
            )
# test_api.py
import speech_recognition as sr
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor
from langchain_core.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import ChatMessageHistory
import logging
from typing import Dict, List, Optional
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class ConversationAPI:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")
        
        # 메모리 초기화
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            chat_memory=ChatMessageHistory()
        )
        
        # 도구 정의
        self.tools = [
            Tool(
                name="emotion_analysis",
                func=self._analyze_emotion,
                description="사용자의 발화에서 감정을 분석합니다."
            ),
            Tool(
                name="risk_assessment",
                func=self._assess_risk,
                description="대화 내용의 위험도를 평가합니다."
            )
        ]
        
        # 프롬프트 템플릿 생성
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""
                당신은 노인 케어 대화 시스템입니다.
                친근하고 공감적인 태도로 대화하세요.
                
                대화 규칙:
                1. 이전 대화가 있다면 자연스럽게 참고하되, 없다면 새로운 대화를 시작하세요.
                2. 노인분들의 이야기를 경청하고 공감하며 친근하게 대화하세요.
                3. 말씀하신 내용에 대해 구체적인 관심을 보이고 자연스러운 후속 질문을 해주세요.
                4. 위험 신호가 감지되면 이를 기록하고 적절히 대응하세요.
                5. 대화를 갑자기 바꾸지 말고 자연스럽게 이어가세요.
                6. "이전 발화를 찾을 수 없습니다"와 같은 기술적인 언급은 하지 마세요.
                
                대화 예시:
                - 첫 대화: "안녕하세요! 오늘은 어떻게 지내고 계신가요?"
                - 후속 대화: 이전 대화 내용을 자연스럽게 참고하여 대화 이어가기
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
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True
        )
    
    def _analyze_emotion(self, text: str) -> str:
        """감정 분석 도구"""
        return "감정 상태: 보통"
    
    def _assess_risk(self, text: str) -> str:
        """위험도 평가 도구"""
        return "위험 수준: 낮음"
    
    def transcribe_audio(self, audio_file: str) -> Optional[str]:
        """음성 파일을 텍스트로 변환"""
        try:
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio, language='ko-KR')
                return text
        except Exception as e:
            logger.error(f"음성 인식 중 오류 발생: {str(e)}")
            return None
    
    def generate_response(self, text_input: str) -> Optional[str]:
        """에이전트를 사용한 응답 생성"""
        try:
            # 현재 대화 기록 확인
            chat_history = self.memory.load_memory_variables({}).get("chat_history", [])
            
            # 응답 생성
            response = self.agent_executor.invoke({
                "input": text_input,
                "chat_history": chat_history
            })
            
            output = response.get("output", "응답을 생성할 수 없습니다.")
            
            # 메모리에 대화 저장
            self.memory.save_context(
                {"input": text_input},
                {"output": output}
            )
            
            return output
            
        except Exception as e:
            logger.error(f"응답 생성 중 오류 발생: {str(e)}")
            return None
    
    def get_conversation_history(self) -> List:
        """대화 기록 조회"""
        return self.memory.load_memory_variables({}).get("chat_history", [])
    
    def clear_memory(self):
        """대화 기록 초기화"""
        self.memory.clear()
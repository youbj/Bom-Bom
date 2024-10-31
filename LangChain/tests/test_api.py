# test_api.py
import speech_recognition as sr
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain.agents import AgentExecutor, create_openai_tools_agent
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class ConversationAPI:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")
        
        # 메모리 초기화
        self.memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history"
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
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""
                당신은 노인 케어 대화 시스템입니다. 
                노인들의 이야기를 경청하고 공감하며, 
                필요한 경우 적절한 조언이나 도움을 제공해야 합니다.
                대화 중 위험 신호가 감지되면 이를 기록하고 적절히 대응하세요.
                기본적으로는 사용자와의 대화에서 흥미를 찾아내고 질문을 해야합니다.
                질문은 하나만 하여 사용자의 대답을 유도해야합니다
            """),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessage(content="{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # 에이전트 생성
        agent = create_openai_tools_agent(self.llm, self.tools, prompt)
        
        # 에이전트 실행기 초기화
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True
        )
    
    def _analyze_emotion(self, text):
        """감정 분석 도구"""
        return "감정 상태: 보통"
    
    def _assess_risk(self, text):
        """위험도 평가 도구"""
        return "위험 수준: 낮음"
    
    def transcribe_audio(self, audio_file):
        """음성 파일을 텍스트로 변환"""
        try:
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio, language='ko-KR')
                return text
        except Exception as e:
            logger.error(f"음성 인식 중 오류 발생: {str(e)}")
            return None
    
    def generate_response(self, text_input):
        """에이전트를 사용한 응답 생성"""
        try:
            response = self.agent_executor.invoke({"input": text_input})
            return response.get("output", "응답을 생성할 수 없습니다.")
        except Exception as e:
            logger.error(f"응답 생성 중 오류 발생: {str(e)}")
            return None
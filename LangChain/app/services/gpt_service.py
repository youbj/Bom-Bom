from openai import OpenAI
import json
import logging
from typing import Dict, List, Optional
from app.config import settings
from app.models.schema import EmotionalState, RiskLevel

logger = logging.getLogger(__name__)

class GPTService:
    def __init__(self):
        """GPT 서비스 초기화"""
        self.client = OpenAI(api_key=settings.gpt.API_KEY)
        self.conversation_context = []
        
        self.base_prompt = """
        당신은 노인과 대화하는 AI 상담사입니다. 다음 원칙을 따라주세요:

        1. 천천히, 명확하고 간단한 질문을 합니다.
        2. 노인의 건강, 기분, 일상생활에 관심을 보입니다.
        3. 위험 신호(우울, 고립, 건강 악화 등)를 주의깊게 관찰합니다.
        4. 대화는 자연스럽게 이어가되, 필요한 정보를 얻을 수 있도록 합니다.
        5. 공감적이고 지지적인 태도를 유지합니다.

        이전 대화 내용과 맥락을 고려하여 적절한 응답을 생성해주세요.
        """
    # __init__ 끝에 있던 pass 제거
    
    async def generate_response(self,   # async 추가 
                         user_message: str,
                         recent_context: Optional[List[str]] = None) -> Dict:
        """GPT를 사용하여 응답 생성"""
        try:
            # 컨텍스트 구성
            messages = [{"role": "system", "content": self.base_prompt}]
            
            # 이전 대화 컨텍스트 추가
            if recent_context:
                for msg in recent_context[-3:]:  # 최근 3개 메시지만 사용
                    messages.append({"role": "user", "content": msg})
            
            # 현재 메시지 추가
            messages.append({"role": "user", "content": user_message})
            
            # GPT 응답 생성
            response = await self.client.chat.completions.create(  # await 추가
                model=settings.gpt.MODEL_NAME,
                messages=messages,
                temperature=settings.gpt.TEMPERATURE,
                max_tokens=settings.gpt.MAX_TOKENS
            )
            
            # 응답 분석
            analysis = await self._analyze_response(user_message, response.choices[0].message.content)  # await 추가
            
            return {
                "response_text": response.choices[0].message.content,
                "analysis": analysis
            }
            
        except Exception as e:
            logger.error(f"GPT 응답 생성 실패: {str(e)}")
            raise
    
    async def _analyze_response(self, user_message: str, gpt_response: str) -> Dict:  # async 추가
        """대화 내용 분석"""
        try:
            # 분석을 위한 프롬프트
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
            
            analysis_response = await self.client.chat.completions.create(  # await 추가
                model=settings.gpt.MODEL_NAME,
                messages=[{"role": "user", "content": analysis_prompt}],
                temperature=0.3
            )
            
            # JSON 파싱 및 반환
            return json.loads(analysis_response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"응답 분석 실패: {str(e)}")
            return {
                "emotional_state": EmotionalState.NEUTRAL,
                "risk_level": RiskLevel.NONE,
                "keywords": [],
                "actions_needed": []
            }
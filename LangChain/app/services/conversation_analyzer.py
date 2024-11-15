from typing import Dict, List, Tuple
import logging
from openai import AsyncOpenAI  # AsyncOpenAI로 변경
import json
from app.models.schema import (
    EmotionalState, RiskLevel, HealthStatus,
    SentimentAnalysis, RiskAssessment, HealthMetrics
)
from app.config import settings

logger = logging.getLogger(__name__)

class ConversationAnalyzer:
    def __init__(self):
        """분석기 초기화"""
        self.client = AsyncOpenAI(api_key=settings.gpt.api_key)  # AsyncOpenAI 사용
    
    async def analyze_conversation(self, text: str) -> Dict:
        """대화 내용 분석"""
        try:
            prompt = f"""다음 텍스트를 분석해주세요: "{text}"
    
    JSON 형식으로 다음 내용을 포함하여 응답해주세요:
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
    }}"""
    
            # GPT API 호출
            async with self.client as client:
                completion = await client.chat.completions.create(
                    model=settings.gpt.model_name,
                    messages=[
                        {"role": "system", "content": "노인 대화 분석 전문가입니다."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    response_format={"type": "json_object"}
                )
    
            # 응답 파싱
            analysis = json.loads(completion.choices[0].message.content)
            logger.info(f"GPT Analysis result: {analysis}")
    
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
            logger.error(f"대화 분석 실패: {str(e)}")
            return self._get_default_analysis()
    
    def _get_default_analysis(self) -> Dict:
        """기본 분석 결과 반환"""
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
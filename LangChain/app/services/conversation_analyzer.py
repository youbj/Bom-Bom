from typing import Dict, List, Tuple
import logging
from app.models.schema import (
    EmotionalState, RiskLevel, HealthStatus,
    ConversationAnalysis, HealthMetrics
)

logger = logging.getLogger(__name__)

class ConversationAnalyzer:
    def __init__(self):
        self.health_keywords = {
            'physical': ['아프다', '통증', '피곤', '약'],
            'mental': ['걱정', '불안', '우울', '외롭다'],
            'sleep': ['잠', '불면', '피곤'],
            'appetite': ['밥', '식사', '먹다', '입맛']
        }
        
        self.risk_keywords = {
            'high': ['자살', '죽고', '혼자', '무섭다'],
            'medium': ['아프다', '우울', '불안', '병원'],
            'low': ['피곤', '걱정', '스트레스']
        }

        # 감정 분석을 위한 키워드
        self.emotion_keywords = {
            'positive': ['좋다', '행복', '즐겁다', '기쁘다', '감사', '좋아'],
            'negative': ['나쁘다', '슬프다', '힘들다', '불안', '우울', '외롭다'],
            'neutral': ['보통', '그냥', '괜찮다'],
            'concerned': ['걱정', '염려', '근심']
        }
    
    def analyze_sentiment(self, text: str) -> Dict:
        """텍스트의 감정 분석"""
        try:
            # 긍정/부정 점수 계산
            positive_count = sum(1 for word in self.emotion_keywords['positive'] if word in text)
            negative_count = sum(1 for word in self.emotion_keywords['negative'] if word in text)
            
            # -100에서 100 사이의 점수로 변환
            score = (positive_count - negative_count) * 50
            
            return {
                "score": score,
                "is_positive": score > 0,
                "confidence": min(abs(score) / 100, 1.0)
            }
        except Exception as e:
            logger.error(f"감정 분석 실패: {str(e)}")
            return {"score": 0, "is_positive": True, "confidence": 0}

    def summarize_text(self, text: str) -> str:
        """텍스트 요약"""
        try:
            sentences = text.split('.')
            if len(sentences) <= 2:
                return text.strip()
            
            # 첫 문장만 반환하여 확실히 더 짧게 만듦
            summary = f"{sentences[0].strip()}."
            return summary
        except Exception as e:
            logger.error(f"텍스트 요약 실패: {str(e)}")
            return text[:len(text)//2]  # 최소한 원본의 절반 길이로 반환

    def analyze_conversation(self, text: str) -> ConversationAnalysis:
        """대화 내용 분석"""
        try:
            # 감정 상태 분석
            emotional_state = self._analyze_emotion(text)
            
            # 건강 상태 분석
            health_metrics = self._analyze_health(text)
            
            # 위험 수준 평가
            risk_level, risk_factors = self._assess_risk(text)
            
            # 일상 활동 추출
            daily_activities = self._extract_activities(text)
            
            # 사회적 상호작용 분석
            social_interactions = self._analyze_social(text)
            
            return ConversationAnalysis(
                health_metrics=health_metrics,
                emotional_state=emotional_state,
                risk_level=risk_level,
                risk_factors=risk_factors,
                daily_activities=daily_activities,
                social_interactions=social_interactions,
                summary=self._generate_summary(text),
                action_needed=(risk_level in [RiskLevel.MEDIUM, RiskLevel.HIGH])
            )
        except Exception as e:
            logger.error(f"대화 분석 실패: {str(e)}")
            return self._get_default_analysis()
    
    def _analyze_emotion(self, text: str) -> EmotionalState:
        """감정 상태 분석"""
        try:
            # 각 감정 카테고리의 키워드 출현 횟수 계산
            emotion_counts = {
                emotion: sum(1 for word in keywords if word in text)
                for emotion, keywords in self.emotion_keywords.items()
            }
            
            # 가장 많이 출현한 감정 선택
            dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0]
            
            return EmotionalState(dominant_emotion)
        except Exception as e:
            logger.error(f"감정 분석 실패: {str(e)}")
            return EmotionalState.NEUTRAL
    
    def _analyze_health(self, text: str) -> HealthMetrics:
        """건강 상태 분석"""
        try:
            # 각 건강 카테고리별 키워드 출현 횟수 계산
            health_scores = {}
            for category, keywords in self.health_keywords.items():
                count = sum(1 for word in keywords if word in text)
                health_scores[category] = min(count * 0.25, 1.0)  # 0~1 사이의 점수로 정규화
            
            # 전반적인 건강 상태 결정
            if max(health_scores.values()) > 0.7:
                status = HealthStatus.CONCERNING
            elif max(health_scores.values()) > 0.4:
                status = HealthStatus.FAIR
            elif max(health_scores.values()) > 0:
                status = HealthStatus.GOOD
            else:
                status = HealthStatus.UNKNOWN
            
            return HealthMetrics(
                status=status,
                physical_health={"score": health_scores.get('physical', 0)},
                mental_health={"score": health_scores.get('mental', 0)},
                sleep_quality=health_scores.get('sleep', None),
                appetite_level=health_scores.get('appetite', None)
            )
        except Exception as e:
            logger.error(f"건강 상태 분석 실패: {str(e)}")
            return HealthMetrics(
                status=HealthStatus.UNKNOWN,
                physical_health={},
                mental_health={},
                sleep_quality=None,
                appetite_level=None
            )
    
    def _assess_risk(self, text: str) -> Tuple[RiskLevel, List[str]]:
        """위험 수준 평가"""
        try:
            risk_factors = []
            highest_risk = RiskLevel.NONE
            
            # 각 위험 수준별 키워드 확인
            for level, keywords in self.risk_keywords.items():
                found_keywords = [word for word in keywords if word in text]
                if found_keywords:
                    risk_factors.extend(found_keywords)
                    highest_risk = RiskLevel(level)
            
            return highest_risk, risk_factors
        except Exception as e:
            logger.error(f"위험 수준 평가 실패: {str(e)}")
            return RiskLevel.NONE, []
    
    def _extract_activities(self, text: str) -> List[str]:
        """일상 활동 추출"""
        try:
            # 기본적인 활동 키워드
            activity_keywords = ['산책', '운동', '식사', '청소', '쇼핑', '텔레비전', 'TV']
            
            # 발견된 활동들 수집
            activities = [word for word in activity_keywords if word in text]
            
            return activities if activities else ['특별한 활동이 언급되지 않음']
        except Exception as e:
            logger.error(f"활동 추출 실패: {str(e)}")
            return []
    
    def _analyze_social(self, text: str) -> List[str]:
        """사회적 상호작용 분석"""
        try:
            # 사회적 관계 키워드
            social_keywords = ['가족', '친구', '이웃', '자녀', '손주', '방문']
            
            # 발견된 사회적 상호작용 수집
            interactions = [word for word in social_keywords if word in text]
            
            return interactions if interactions else ['특별한 사회적 상호작용이 언급되지 않음']
        except Exception as e:
            logger.error(f"사회적 상호작용 분석 실패: {str(e)}")
            return []
    
    def _generate_summary(self, text: str) -> str:
        """대화 요약 생성"""
        return self.summarize_text(text)
    
    def _get_default_analysis(self) -> ConversationAnalysis:
        """기본 분석 결과 반환"""
        return ConversationAnalysis(
            health_metrics=HealthMetrics(
                status=HealthStatus.UNKNOWN,
                physical_health={},
                mental_health={},
                sleep_quality=None,
                appetite_level=None
            ),
            emotional_state=EmotionalState.NEUTRAL,
            risk_level=RiskLevel.NONE,
            risk_factors=[],
            daily_activities=[],
            social_interactions=[],
            summary="분석 실패",
            action_needed=False
        )
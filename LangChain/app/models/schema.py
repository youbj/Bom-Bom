from pydantic import BaseModel, ConfigDict
from typing import Dict, Optional, List
from enum import Enum

class HealthStatus(str, Enum):
    """건강 상태 Enum"""
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    CONCERNING = "concerning"
    UNKNOWN = "unknown"

class EmotionalState(str, Enum):
    """감정 상태 Enum"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    CONCERNED = "concerned"

class RiskLevel(str, Enum):
    """위험 수준 Enum"""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class SpeakerType(str, Enum):
    """화자 타입 Enum"""
    USER = "user"
    SYSTEM = "system"

class HealthMetrics(BaseModel):
    """건강 지표 모델"""
    status: HealthStatus
    physical_health: Dict[str, float] = {}
    mental_health: Dict[str, float] = {} 
    sleep_quality: Optional[float] = None
    appetite_level: Optional[float] = None
    
class SentimentAnalysis(BaseModel):
    """감정 분석 결과 모델"""
    score: float
    is_positive: bool
    confidence: float

class ConversationResponse(BaseModel):
    """대화 응답 모델"""
    conversation_id: str
    text_response: str
    sentiment_analysis: SentimentAnalysis
    text_summary: str
    analysis: Dict

class ConversationMessage(BaseModel):
    """대화 메시지 모델"""
    conversation_id: str
    speaker_type: SpeakerType
    text_content: str
    sentiment_score: float
    summary: str

class ConversationAnalysis(BaseModel):
    """대화 분석 결과 모델"""
    health_metrics: HealthMetrics
    emotional_state: EmotionalState
    risk_level: RiskLevel
    risk_factors: List[str]
    daily_activities: List[str]
    social_interactions: List[str]
    summary: str
    action_needed: bool

    class Config:
        use_enum_values = True
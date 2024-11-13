from enum import Enum
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class SpeakerType(str, Enum):
    USER = "USER"
    AI = "AI"

class EmotionalState(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    CONCERNED = "concerned"

class RiskLevel(str, Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class HealthStatus(str, Enum):
    UNKNOWN = "unknown"
    GOOD = "good"
    FAIR = "fair"
    CONCERNING = "concerning"

class SentimentAnalysis(BaseModel):
    score: float
    is_positive: bool
    confidence: float
    emotional_state: Optional[str]
    emotion_score: Optional[float]
    emotion_description: Optional[str]

class RiskAssessment(BaseModel):
    risk_level: RiskLevel
    risk_factors: List[str]
    needed_actions: List[str]

class HealthMetrics(BaseModel):
    status: HealthStatus
    physical_health_score: Optional[float]
    mental_health_score: Optional[float]
    sleep_quality_score: Optional[float]
    appetite_level_score: Optional[float]

class Message(BaseModel):
    conversation_id: str
    speaker_type: SpeakerType
    text_content: str
    message_number: int
    sentiment_analysis: Optional[SentimentAnalysis]
    risk_assessment: Optional[RiskAssessment]
    summary: Optional[str]
    keywords: Optional[List[str]]
    created_at: Optional[datetime]

class ConversationSession(BaseModel):
    conversation_id: str
    start_time: datetime
    end_time: Optional[datetime]
    messages: List[Message] = []
    health_monitoring: Optional[HealthMetrics]
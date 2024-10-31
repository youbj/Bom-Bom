
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum

class SpeakerType(str, Enum):
    AI = "ai"
    ELDERLY = "elderly"

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

class HealthStatus(BaseModel):
    physical_health: str
    mental_health: str
    sleep_quality: str
    appetite: str
    pain_points: List[str] = []

class ConversationMessage(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    speaker_type: SpeakerType
    audio_path: Optional[str]
    text_content: str
    emotional_state: EmotionalState
    
class ConversationAnalysis(BaseModel):
    conversation_id: str
    timestamp: datetime
    health_status: HealthStatus
    emotional_state: EmotionalState
    risk_level: RiskLevel
    risk_factors: List[str] = []
    daily_activities: List[str] = []
    social_interactions: List[str] = []
    summary: str
    action_needed: bool = False
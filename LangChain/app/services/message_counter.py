from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

@dataclass
class ConversationStats:
    total_messages: int = 0
    user_messages: int = 0
    ai_messages: int = 0
    start_time: Optional[datetime] = None
    last_message_time: Optional[datetime] = None
    
class MessageCounter:
    def __init__(self):
        self._conversations: Dict[str, ConversationStats] = {}
        
    def start_conversation(self, conversation_id: str) -> None:
        """새 대화 시작"""
        self._conversations[conversation_id] = ConversationStats(
            start_time=datetime.now()
        )
        logger.info(f"Started counting messages for conversation: {conversation_id}")
    
    def increment_count(self, conversation_id: str, is_user: bool = True) -> int:
        """메시지 카운트 증가"""
        if conversation_id not in self._conversations:
            self.start_conversation(conversation_id)
            
        stats = self._conversations[conversation_id]
        stats.total_messages += 1
        if is_user:
            stats.user_messages += 1
        else:
            stats.ai_messages += 1
        stats.last_message_time = datetime.now()
        
        return stats.total_messages
    
    def get_stats(self, conversation_id: str) -> Optional[ConversationStats]:
        """대화 통계 조회"""
        return self._conversations.get(conversation_id)
    
    def should_end_conversation(self, conversation_id: str, max_messages: int = 16) -> bool:
        """대화 종료 여부 판단"""
        stats = self.get_stats(conversation_id)
        if not stats:
            return False
            
        return stats.total_messages >= max_messages
    
    def get_message_count(self, conversation_id: str) -> int:
        """현재 메시지 수 조회"""
        stats = self.get_stats(conversation_id)
        return stats.total_messages if stats else 0
    
    def end_conversation(self, conversation_id: str) -> None:
        """대화 종료"""
        if conversation_id in self._conversations:
            del self._conversations[conversation_id]
            logger.info(f"Ended message counting for conversation: {conversation_id}")

    def get_conversation_duration(self, conversation_id: str) -> Optional[float]:
        """대화 지속 시간 계산 (분 단위)"""
        stats = self.get_stats(conversation_id)
        if not stats or not stats.start_time or not stats.last_message_time:
            return None
            
        duration = stats.last_message_time - stats.start_time
        return duration.total_seconds() / 60
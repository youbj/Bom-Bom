
from fastapi import Depends
from typing import Dict, Optional
import uuid
import logging
from datetime import datetime
from app.services.gpt_service import GPTService
from app.services.conversation_analyzer import ConversationAnalyzer
from app.services.kafka_manager import KafkaManager
from app.database.mysql_manager import MySQLManager
from app.models.schema import SpeakerType, ConversationMessage

logger = logging.getLogger(__name__)

class ConversationManager:
    def __init__(self):
        """대화 관리 시스템 초기화"""
        self.gpt_service = GPTService()
        self.analyzer = ConversationAnalyzer()
        self.kafka_manager = KafkaManager()
        self.mysql_manager = MySQLManager()
        self.current_conversation_id = None
    
    def start_conversation(self) -> str:
        """새로운 대화 시작"""
        self.current_conversation_id = str(uuid.uuid4())
        return self.current_conversation_id
    
    async def process_text_input(self, text: str) -> Dict:
        """텍스트 입력 처리"""
        try:
            if not self.current_conversation_id:
                self.current_conversation_id = self.start_conversation()

            # 최근 대화 컨텍스트 조회
            try:
                recent_contexts = self.kafka_manager.get_recent_conversations()
            except Exception as e:
                logger.warning(f"Kafka 연결 실패, 빈 컨텍스트 사용: {str(e)}")
                recent_contexts = []
        
            # 감정 분석
            sentiment_analysis = self.analyzer.analyze_sentiment(text)
            
            # 텍스트 요약
            text_summary = self.analyzer.summarize_text(text)
            
            # GPT 응답 생성
            gpt_response = await self.gpt_service.generate_response(
                text,
                recent_context=[msg.get('text_content', '') for msg in recent_contexts]
            )
            
            # 대화 저장 (Kafka & MySQL)
            conversation_data = ConversationMessage(
                conversation_id=self.current_conversation_id,
                speaker_type=SpeakerType.USER,
                text_content=text,
                sentiment_score=sentiment_analysis['score'],
                summary=text_summary
            )
            
            self.kafka_manager.store_conversation(conversation_data.dict())
            self.mysql_manager.save_conversation(conversation_data.dict())
            
            return {
                "text_response": gpt_response['response_text'],
                "sentiment_analysis": sentiment_analysis,
                "text_summary": text_summary,
                "analysis": gpt_response['analysis']
            }
            
        except Exception as e:
            logger.error(f"텍스트 입력 처리 실패: {str(e)}")
            raise
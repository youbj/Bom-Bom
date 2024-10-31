from typing import Optional, Dict, List  # Dict 추가
import uuid
import os  # os 모듈 추가
import logging
from datetime import datetime
from app.services.audio_processor import AudioProcessor
from app.services.gpt_service import GPTService
from app.services.conversation_analyzer import ConversationAnalyzer
from app.services.kafka_manager import KafkaManager
from app.services.report_generator import ReportGenerator
from app.database.mysql_manager import MySQLManager
from app.models.schema import SpeakerType, ConversationMessage

logger = logging.getLogger(__name__)

class ConversationManager:
    def __init__(self):
        """대화 관리 시스템 초기화"""
        self.audio_processor = AudioProcessor()
        self.gpt_service = GPTService()
        self.analyzer = ConversationAnalyzer()
        self.kafka_manager = KafkaManager()
        self.mysql_manager = MySQLManager()
        self.report_generator = ReportGenerator()
        
        self.current_conversation_id = None
    
    def start_conversation(self) -> str:
        """새로운 대화 시작"""
        self.current_conversation_id = str(uuid.uuid4())
        return self.current_conversation_id
    
    async def process_audio_input(self, audio_path: str) -> Dict:
        """음성 입력 처리"""
        try:
            # 음성을 텍스트로 변환
            text = await self.audio_processor.speech_to_text(audio_path)  # async 추가
            if not text:
                raise ValueError("음성 인식 실패")
        
            # 최근 대화 컨텍스트 조회
            try:
                recent_contexts = self.kafka_manager.get_recent_conversations()
            except Exception as e:
                logger.warning(f"Kafka 연결 실패, 빈 컨텍스트 사용: {str(e)}")
                recent_contexts = []
        
            # GPT 응답 생성
            gpt_response = await self.gpt_service.generate_response(  # await 추가
                text,
                recent_context=[msg.get('text_content', '') for msg in recent_contexts]
            )
            
            # 응답 분석
            analysis = self.analyzer.analyze_conversation(text)
            
            # 대화 저장 (Kafka & MySQL)
            conversation_data = ConversationMessage(
                conversation_id=self.current_conversation_id,
                speaker_type=SpeakerType.ELDERLY,
                audio_path=audio_path,
                text_content=text,
                emotional_state=analysis.emotional_state
            )
            
            self.kafka_manager.store_conversation(conversation_data.dict())
            self.mysql_manager.save_conversation(conversation_data.dict())
            self.mysql_manager.save_analysis(analysis.dict())
            
            # 음성 응답 생성
            response_audio_path = f"response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
            self.audio_processor.text_to_speech(
                gpt_response['response_text'],
                response_audio_path
            )
            
            return {
                "text_response": gpt_response['response_text'],
                "audio_response": response_audio_path,
                "analysis": analysis.dict()
            }
            
        except Exception as e:
            logger.error(f"음성 입력 처리 실패: {str(e)}")
            raise
    
    def generate_report(self, 
                       start_date: datetime,
                       end_date: datetime,
                       elderly_id: str) -> str:
        """보고서 생성"""
        try:
            # 분석 데이터 조회
            analyses = self.mysql_manager.get_analyses(
                elderly_id=elderly_id,
                start_date=start_date,
                end_date=end_date
            )
            
            # PDF 보고서 생성
            report_path = self.report_generator.generate_pdf_report(
                analyses=analyses,
                start_date=start_date,
                end_date=end_date
            )
            
            return report_path
            
        except Exception as e:
            logger.error(f"보고서 생성 실패: {str(e)}")
            raise
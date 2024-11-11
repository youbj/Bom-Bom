from fastapi import Depends
from typing import Dict, Optional, List
import uuid
import logging
from datetime import datetime
from app.services.gpt_service import GPTService
from app.services.conversation_analyzer import ConversationAnalyzer
from app.database.mysql_manager import MySQLManager
from app.models.schema import SpeakerType, ConversationMessage

logger = logging.getLogger(__name__)

class ConversationManager:
    message_counter = 0
    
    def __init__(self):
        """대화 관리 시스템 초기화"""
        self.gpt_service = GPTService()
        self.analyzer = ConversationAnalyzer()
        self.mysql_manager = MySQLManager()
        self.current_conversation_id = None
        self.messages = []
    
    def start_conversation(self) -> str:
        """새로운 대화 시작"""
        self.current_conversation_id = str(uuid.uuid4())
        print(f"\n=== 새로운 대화 시작 (ID: {self.current_conversation_id}) ===\n")
        return self.current_conversation_id

    async def process_text_input(self, text: str, is_initial: bool = False) -> Dict:
        """텍스트 입력 처리"""
        try:
            # conversation_id가 없으면 새로 생성
            if not self.current_conversation_id:
                self.current_conversation_id = self.start_conversation()
            
            if is_initial:
                # 초기 인사 메시지 생성
                gpt_response = await self.gpt_service.generate_response(
                    user_message="",
                    is_initial=True
                )
                return {
                    "conversation_id": self.current_conversation_id,
                    "response_text": gpt_response['response_text']
                }
            
            # 일반 대화 처리
            ConversationManager.message_counter += 1
            print(f"\n[사용자 입력 #{ConversationManager.message_counter}]")
            print(f"내용: {text}")
            
            # 감정 분석
            sentiment_analysis = self.analyzer.analyze_sentiment(text)
            print("\n[감정 분석 결과]")
            print(f"감정 점수: {sentiment_analysis['score']}")
            print(f"긍정/부정: {'긍정' if sentiment_analysis['is_positive'] else '부정'}")
            
            # 텍스트 요약
            text_summary = self.analyzer.summarize_text(text)
            print("\n[텍스트 요약]")
            print(text_summary)
            
            # GPT 응답 생성
            print("\n[응답 생성 중...]")
            gpt_response = await self.gpt_service.generate_response(
                user_message=text,
                is_initial=False
            )
            
            # 응답 출력
            response_text = gpt_response['response_text']
            print(f"\n[AI 응답 #{ConversationManager.message_counter}]")
            print(response_text)
            
            # 대화 내용 저장
            message_data = {
                'number': ConversationManager.message_counter,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'user_input': text,
                'ai_response': response_text,
                'sentiment_score': sentiment_analysis['score'],
                'summary': text_summary
            }
            self.messages.append(message_data)
            
            # MySQL 저장
            conversation_data = ConversationMessage(
                conversation_id=self.current_conversation_id,
                speaker_type=SpeakerType.USER,
                text_content=text,
                sentiment_score=sentiment_analysis['score'],
                summary=text_summary
            )
            self.mysql_manager.save_conversation(conversation_data.dict())
            
            ai_message_data = ConversationMessage(
                conversation_id=self.current_conversation_id,
                speaker_type=SpeakerType.AI,
                text_content=response_text,
                sentiment_score=None,  # AI 응답은 감정 점수 불필요
                summary=None  # AI 응답은 요약 불필요
            )
            self.mysql_manager.save_conversation(ai_message_data.dict())
            
            print("\n" + "="*50 + "\n")
            
            return {
                "conversation_id": self.current_conversation_id,
                "text_response": response_text,
                "sentiment_analysis": sentiment_analysis,
                "text_summary": text_summary,
                "analysis": gpt_response.get('conversation_analysis', {}),
                "message_number": ConversationManager.message_counter
            }
            
        except Exception as e:
            print(f"\n[오류 발생] {str(e)}")
            logger.error(f"텍스트 입력 처리 실패: {str(e)}", exc_info=True)
            raise
    
    def end_conversation(self):
        """대화 종료 및 정리"""
        try:
            if self.current_conversation_id:
                # 메시지 히스토리 출력
                self.print_conversation_history()
                
                # 메모리 정리
                self.messages = []
                self.current_conversation_id = None
                
                print("\n=== 대화가 종료되었습니다 ===\n")
                logger.info("Conversation ended successfully")
        except Exception as e:
            logger.error(f"대화 종료 중 오류 발생: {str(e)}")
            raise
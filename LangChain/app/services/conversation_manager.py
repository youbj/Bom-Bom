from fastapi import Depends
from typing import Dict, Optional, List
import uuid
import logging
from datetime import datetime
from app.services.gpt_service import GPTService
from app.services.conversation_analyzer import ConversationAnalyzer
from app.database.mysql_manager import MySQLManager
from app.models.schema import (
    SpeakerType, ConversationSession, Message,
    SentimentAnalysis, RiskAssessment, HealthMetrics
)

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
        try:
            self.current_conversation_id = str(uuid.uuid4())
            self.message_counter = 0
            
            # 데이터베이스에 새 대화 세션 생성
            success = self.mysql_manager.start_conversation(self.current_conversation_id)
            if not success:
                raise Exception("Failed to create conversation session")
            
            logger.info(f"Started new conversation: {self.current_conversation_id}")
            return self.current_conversation_id
            
        except Exception as e:
            logger.error(f"Failed to start conversation: {str(e)}")
            raise

    async def process_text_input(self, text: str, is_initial: bool = False) -> Dict:
        """텍스트 입력 처리"""
        try:
            # conversation_id가 없으면 새로 생성
            if not self.current_conversation_id:
                self.current_conversation_id = self.start_conversation()
                self.mysql_manager.start_conversation(self.current_conversation_id)
                
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
            self.message_counter += 1
            logger.info(f"Processing message #{self.message_counter} for conversation {self.current_conversation_id}")
            
            # 대화 분석
            analysis_result = await self.analyzer.analyze_conversation(text)  # await 추가
            
            # GPT 응답 생성
            gpt_response = await self.gpt_service.generate_response(
                user_message=text,
                is_initial=False
            )
            
            # 사용자 메시지 저장
            user_message_data = {
                'conversation_id': self.current_conversation_id,
                'speaker_type': 'USER',
                'text_content': text,
                'message_number': self.message_counter,
                'sentiment_analysis': analysis_result['sentiment_analysis'],
                'risk_assessment': analysis_result['risk_assessment'],
                'summary': analysis_result['summary'],
                'keywords': analysis_result['keywords']
            }
            
            user_message_id = self.mysql_manager.save_message(user_message_data)
            
            if not user_message_id:
                raise Exception("Failed to save user message")
            
            # AI 응답 저장
            self.message_counter += 1
            ai_message_data = {
                'conversation_id': self.current_conversation_id,
                'speaker_type': 'AI',
                'text_content': gpt_response['response_text'],
                'message_number': self.message_counter
            }
            
            ai_message_id = self.mysql_manager.save_message(ai_message_data)
            
            if not ai_message_id:
                raise Exception("Failed to save AI response")
            
            return {
                "conversation_id": self.current_conversation_id,
                "text_response": gpt_response['response_text'],
                "message_number": self.message_counter,
                "analysis": {
                    "sentiment": analysis_result['sentiment_analysis'],
                    "risk_level": analysis_result['risk_assessment']['risk_level'],
                    "health_status": analysis_result.get('health_metrics', {}).get('status', 'UNKNOWN'),
                    "keywords": analysis_result['keywords'],
                    "summary": analysis_result['summary']
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to process text input: {str(e)}", exc_info=True)
            raise

    def end_conversation(self) -> bool:
        """대화 종료 및 정리"""
        try:
            if self.current_conversation_id:
                # 대화 세션 종료 처리
                success = self.mysql_manager.end_conversation(self.current_conversation_id)
                if not success:
                    raise Exception("Failed to end conversation in database")
                
                # 대화 히스토리 출력
                conversation_history = self.mysql_manager.get_conversation_history(
                    self.current_conversation_id
                )
                
                # 메모리 정리
                self.messages = []
                self.current_conversation_id = None
                self.message_counter = 0
                
                logger.info(f"Conversation ended successfully: {len(conversation_history)} messages processed")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to end conversation: {str(e)}")
            return False

    def get_conversation_summary(self, conversation_id: str) -> Dict:
        """대화 요약 정보 조회"""
        try:
            conversation_history = self.mysql_manager.get_conversation_history(conversation_id)
            
            if not conversation_history:
                return {
                    "status": "not_found",
                    "message": "Conversation not found"
                }
            
            # 대화 통계 계산
            total_messages = len(conversation_history)
            user_messages = sum(1 for msg in conversation_history if msg['speaker_type'] == SpeakerType.USER)
            ai_messages = total_messages - user_messages
            
            # 감정 분석 통계
            sentiment_scores = [
                msg.get('sentiment_score', 0) 
                for msg in conversation_history 
                if msg.get('sentiment_score') is not None
            ]
            
            avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
            
            # 위험 수준 추적
            risk_levels = [
                msg.get('risk_level') 
                for msg in conversation_history 
                if msg.get('risk_level')
            ]
            
            highest_risk = max(risk_levels, default='NONE')
            
            # 주요 키워드 집계
            keywords = {}
            for msg in conversation_history:
                if msg.get('keywords'):
                    for keyword in msg['keywords']:
                        keywords[keyword] = keywords.get(keyword, 0) + 1
            
            top_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:5]
            
            return {
                "status": "success",
                "summary": {
                    "total_messages": total_messages,
                    "user_messages": user_messages,
                    "ai_messages": ai_messages,
                    "average_sentiment": avg_sentiment,
                    "highest_risk_level": highest_risk,
                    "top_keywords": top_keywords,
                    "start_time": conversation_history[0]['created_at'],
                    "end_time": conversation_history[-1]['created_at']
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to get conversation summary: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
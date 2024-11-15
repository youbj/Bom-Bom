from typing import Dict, Optional
import uuid
import logging
import json
from datetime import datetime
from app.services.gpt_service import GPTService
from app.database.mysql_manager import MySQLManager
from app.services.message_counter import MessageCounter
from app.config import settings
from app.models.schema import SpeakerType

logger = logging.getLogger(__name__)

class ConversationManager:
    def __init__(self, mysql_manager: MySQLManager, gpt_service: GPTService):
        """대화 관리 시스템 초기화"""
        self.gpt_service = gpt_service
        self.mysql_manager = mysql_manager
        self.current_conversation_id = None
        self.memory_id = None
        
        # 메시지 카운터 추가
        self.message_counter = MessageCounter(mysql_manager)
        
        # 대화 설정
        self.max_turns = settings.max_conversation_turns
        self.warning_threshold = settings.warning_threshold

    async def start_conversation(self, senior_id: int) -> Dict:
        """새로운 대화 시작"""
        try:
            # Memory ID 생성
            self.memory_id = str(uuid.uuid4())

            # DB에 대화 세션 생성
            self.current_conversation_id = await self.mysql_manager.start_conversation(
                memory_id=self.memory_id,
                senior_id=senior_id
            )

            if not self.current_conversation_id:
                raise Exception("대화 memory 모듈 생성 실패")
            
            # 메시지 카운터 시작
            await self.message_counter.start_conversation(str(self.current_conversation_id))

            # 초기 응답 생성
            initial_response = await self.gpt_service.generate_response(
                user_message="",
                conversation_id=self.current_conversation_id,
                memory_id=self.memory_id,
                senior_id=senior_id,
                is_initial=True
            )

            # AI 응답 저장
            memory_data = {
                'memory_id': self.memory_id,
                'conversation_id': self.current_conversation_id,
                'speaker': 'AI',  
                'content': initial_response['response_text'],
                'summary': None,
                'positivity_score': 50, 
                'keywords': json.dumps([]),  
                'response_plan': json.dumps([])  
            }

            await self.mysql_manager.save_memory(memory_data)

            logger.info(f"Started new conversation: {self.current_conversation_id}")
            return {
                "conversation_id": self.current_conversation_id,
                "memory_id": self.memory_id,
                "response": initial_response
            }

        except Exception as e:
            logger.error(f"Failed to start conversation: {str(e)}")
            raise

    async def process_message(self, text: str, senior_id: int) -> Dict:
        """메시지 처리"""
        try:
            if not self.current_conversation_id:
                raise Exception("No active conversation")
            
            # 사용자 메시지 카운트 증가
            await self.message_counter.increment_count(str(self.current_conversation_id), is_user=True)

            if not self.memory_id:
                conversation_info = await self.mysql_manager.get_conversation_status(self.current_conversation_id)
                if conversation_info and 'memory_id' in conversation_info:
                    self.memory_id = conversation_info['memory_id']
                else:
                    # memory_id가 없으면 새로 생성
                    self.memory_id = str(uuid.uuid4())


            # 대화 종료 체크
            stats = self.message_counter.get_stats(str(self.current_conversation_id))
            if self.message_counter.should_end_conversation(str(self.current_conversation_id)):
                return await self.end_conversation(
                    final_message="좋은 대화를 나눌 수 있어서 기뻤습니다! 제가 필요한 일이 있으면 또 불러주세요!"
                )

            # 사용자 메시지 저장
            user_memory_data = {
                'memory_id': self.memory_id,
                'conversation_id': self.current_conversation_id,
                'speaker': 'User', 
                'content': text,
                'summary': None,
                'positivity_score': 50, 
                'keywords': json.dumps([]),  
                'response_plan': json.dumps([])  
            }

            await self.mysql_manager.save_memory(user_memory_data)

            # GPT 응답 생성
            gpt_response = await self.gpt_service.generate_response(
                user_message=text,
                conversation_id=self.current_conversation_id,
                memory_id=self.memory_id,
                senior_id=senior_id,
                is_initial=False
            )
            
            await self.message_counter.increment_count(str(self.current_conversation_id), is_user=False)
            
            # AI 응답 저장
            ai_memory_data = {
                'memory_id': self.memory_id,
                'conversation_id': self.current_conversation_id,
                'speaker': 'AI',  # enum 값과 정확히 일치하도록 수정
                'content': gpt_response['response_text'],
                'summary': gpt_response.get('user_analysis', {}).get('summary'),
                'positivity_score': gpt_response.get('user_analysis', {}).get('sentiment', {}).get('score', 50),
                'keywords': json.dumps(gpt_response.get('user_analysis', {}).get('keywords', [])),  # JSON 문자열로 변환
                'response_plan': json.dumps(gpt_response.get('user_analysis', {}).get('response_plan', []))  # JSON 문자열로 변환
            }

            await self.mysql_manager.save_memory(ai_memory_data)
            
            stats = self.message_counter.get_stats(str(self.current_conversation_id))
            
            return {
                "conversation_id": self.current_conversation_id,
                "memory_id": self.memory_id,
                "response": gpt_response,
                "current_turn": stats.total_messages if stats else 0,
                "remaining_turns": self.max_turns - (stats.total_messages if stats else 0),  # 수정
                "should_warn": (stats.total_messages if stats else 0) >= self.warning_threshold,  # 수정
                "stats": {  # 통계 정보 추가
                    "total_messages": stats.total_messages if stats else 0,
                    "user_messages": stats.user_messages if stats else 0,
                    "ai_messages": stats.ai_messages if stats else 0
                }
            }

        except Exception as e:
            logger.error(f"Failed to process message: {str(e)}")
            raise

    async def end_conversation(self, final_message: Optional[str] = None) -> Dict:
        """대화 종료"""
        try:
            if not self.current_conversation_id:
                raise Exception("No active conversation to end")
            
            # 대화 통계 가져오기
            duration = self.message_counter.get_conversation_duration(str(self.current_conversation_id))
            stats = self.message_counter.get_stats(str(self.current_conversation_id))
            
            # 메시지 카운터에서 대화 제거
            self.message_counter.end_conversation(str(self.current_conversation_id))

            # 최종 메시지가 있는 경우 저장
            if final_message:
                await self.mysql_manager.save_memory({
                    'memory_id': self.memory_id,
                    'conversation_id': self.current_conversation_id,
                    'speaker': SpeakerType.AI,
                    'content': final_message
                })

            # 대화 세션 종료
            success = await self.mysql_manager.end_conversation(self.current_conversation_id)
            if not success:
                raise Exception("Failed to end conversation in database")

            # GPT 서비스 메모리 초기화
            self.gpt_service.reset_memory()

            # 대화 상태 초기화
            final_status = {
                "conversation_id": self.current_conversation_id,
                "memory_id": self.memory_id,
                "total_turns": stats.total_messages if stats else 0,
                "end_time": datetime.now().isoformat(),
                "final_message": final_message if final_message else "대화가 종료되었습니다.",
                "stats": {  # 통계 정보 추가
                    "total_messages": stats.total_messages if stats else 0,
                    "user_messages": stats.user_messages if stats else 0,
                    "ai_messages": stats.ai_messages if stats else 0,
                    "duration_minutes": duration if duration else 0
                }
            }

            self.current_conversation_id = None
            self.memory_id = None

            return final_status

        except Exception as e:
            logger.error(f"Failed to end conversation: {str(e)}")
            raise

    async def get_conversation_status(self) -> Dict:
        """현재 대화 상태 조회"""
        if not self.current_conversation_id:
            return {"status": "no_active_conversation"}

        conversation_status = await self.mysql_manager.get_conversation_status(
            self.current_conversation_id
        )

        stats = self.message_counter.get_stats(str(self.current_conversation_id))

        return {
            "conversation_id": self.current_conversation_id,
            "memory_id": self.memory_id,
            "current_turn": stats.total_messages if stats else 0,
            "remaining_turns": self.max_turns - (stats.total_messages if stats else 0),
            "should_warn": (stats.total_messages if stats else 0) >= self.warning_threshold,
            "stats": {
                "total_messages": stats.total_messages if stats else 0,
                "user_messages": stats.user_messages if stats else 0,
                "ai_messages": stats.ai_messages if stats else 0
            },
            **conversation_status
        }
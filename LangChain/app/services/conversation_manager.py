from typing import Dict, Optional
import uuid
import logging
import json
from datetime import datetime
from app.services.gpt_service import GPTService
from app.database.mysql_manager import MySQLManager
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
        
        # 대화 설정
        self.max_turns = settings.max_conversation_turns
        self.warning_threshold = settings.warning_threshold
        self.current_turn = 0

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
                'speaker': 'AI',  # enum 값과 정확히 일치하도록 수정
                'content': initial_response['response_text'],
                'summary': None,
                'positivity_score': 50,  # 기본값 설정
                'keywords': json.dumps([]),  # JSON 문자열로 변환
                'response_plan': json.dumps([])  # JSON 문자열로 변환
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

            self.current_turn += 1

            # 대화 턴 수 체크
            if self.current_turn >= self.max_turns:
                return await self.end_conversation(
                    final_message="대화를 마무리할 시간이 되었네요. 오늘도 즐거운 대화 나눌 수 있어서 좋았습니다."
                )

            # 사용자 메시지 저장
            user_memory_data = {
                'memory_id': self.memory_id,
                'conversation_id': self.current_conversation_id,
                'speaker': 'User',  # enum 값과 정확히 일치하도록 수정
                'content': text,
                'summary': None,
                'positivity_score': 50,  # 기본값 설정
                'keywords': json.dumps([]),  # JSON 문자열로 변환
                'response_plan': json.dumps([])  # JSON 문자열로 변환
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

            return {
                "conversation_id": self.current_conversation_id,
                "memory_id": self.memory_id,
                "response": gpt_response,
                "current_turn": self.current_turn,
                "remaining_turns": self.max_turns - self.current_turn,
                "should_warn": self.current_turn >= self.warning_threshold
            }

        except Exception as e:
            logger.error(f"Failed to process message: {str(e)}")
            raise

    async def end_conversation(self, final_message: Optional[str] = None) -> Dict:
        """대화 종료"""
        try:
            if not self.current_conversation_id:
                raise Exception("No active conversation to end")

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
                "total_turns": self.current_turn,
                "end_time": datetime.now().isoformat(),
                "final_message": final_message if final_message else "대화가 종료되었습니다."
            }

            self.current_conversation_id = None
            self.memory_id = None
            self.current_turn = 0

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

        return {
            "conversation_id": self.current_conversation_id,
            "memory_id": self.memory_id,
            "current_turn": self.current_turn,
            "remaining_turns": self.max_turns - self.current_turn,
            "should_warn": self.current_turn >= self.warning_threshold,
            **conversation_status
        }
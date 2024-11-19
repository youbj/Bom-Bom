from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, Dict
from pydantic import BaseModel
from datetime import datetime
from app.services.conversation_manager import ConversationManager
from app.database.mysql_manager import MySQLManager
from app.services.gpt_service import GPTService
from app.api.deps import get_conversation_manager, get_mysql_manager, get_gpt_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class TextInput(BaseModel):
    text: str
    senior_id: Optional[int] = 1

class ConversationFilter(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    include_analysis: bool = False

@router.post("/start")
async def start_conversation(
    input_data: TextInput,
    manager: ConversationManager = Depends(get_conversation_manager)
) -> Dict:
    """새로운 대화 시작"""
    try:
        response = await manager.start_conversation(senior_id=input_data.senior_id)
        return response
    except Exception as e:
        logger.error(f"Failed to start conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat")
async def process_message(
    input_data: TextInput,
    conversation_id: Optional[str] = None,
    manager: ConversationManager = Depends(get_conversation_manager)
) -> Dict:
    """메시지 처리"""
    try:
        if not conversation_id:
            # 새 대화 시작
            start_response = await manager.start_conversation(senior_id=input_data.senior_id)
            conversation_id = start_response["conversation_id"]
            
        # conversation_id 설정
        manager.current_conversation_id = str(conversation_id)  # str로 변환 추가
        
        # 메시지 처리
        response = await manager.process_message(
            text=input_data.text,
            senior_id=input_data.senior_id
        )
        return response
        
    except Exception as e:
        logger.error(f"Failed to process message: {str(e)}")
        if "No active conversation" in str(e):
            raise HTTPException(
                status_code=404,
                detail="대화를 찾을 수 없습니다. 새로운 대화를 시작해주세요."
            )
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{conversation_id}")
async def get_conversation_status(
    conversation_id: str,
    manager: ConversationManager = Depends(get_conversation_manager)
) -> Dict:
    """대화 상태 조회"""
    try:
        manager.current_conversation_id = conversation_id
        status = await manager.get_conversation_status()
        return status
    except Exception as e:
        logger.error(f"Failed to get conversation status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{conversation_id}")
async def end_conversation(
    conversation_id: str,
    manager: ConversationManager = Depends(get_conversation_manager)
) -> Dict:
    """대화 종료"""
    try:
        manager.current_conversation_id = conversation_id
        result = await manager.end_conversation()
        return result
    except Exception as e:
        logger.error(f"Failed to end conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
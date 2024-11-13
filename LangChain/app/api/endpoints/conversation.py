from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, Dict, List
from pydantic import BaseModel
from datetime import datetime
from app.services.conversation_manager import ConversationManager
from app.database.mysql_manager import MySQLManager
from app.api.deps import get_mysql_manager
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class TextInput(BaseModel):
    text: str
    conversation_id: Optional[str] = None

class ConversationFilter(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    include_analysis: bool = False

@router.post("/start")
async def start_conversation(
    db: MySQLManager = Depends(get_mysql_manager)
) -> Dict:
    """새로운 대화 시작"""
    try:
        manager = ConversationManager()
        initial_response = await manager.process_text_input(
            text="",
            is_initial=True
        )
        return initial_response
    except Exception as e:
        logger.error(f"Failed to start conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/process")
async def process_text(
    text_input: TextInput,
    db: MySQLManager = Depends(get_mysql_manager)
) -> Dict:
    """텍스트 처리"""
    try:
        manager = ConversationManager()
        
        if text_input.conversation_id:
            manager.current_conversation_id = text_input.conversation_id
            
        response = await manager.process_text_input(
            text=text_input.text,
            is_initial=False
        )
        return response
    except Exception as e:
        logger.error(f"Failed to process text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    filters: ConversationFilter,
    db: MySQLManager = Depends(get_mysql_manager)
) -> Dict:
    """대화 내용 조회"""
    try:
        # 대화 세션 정보 조회
        session = db.get_conversation_session(conversation_id)
        if not session:
            raise HTTPException(status_code=404, detail="대화를 찾을 수 없습니다")
            
        # 메시지 히스토리 조회
        messages = db.get_conversation_history(
            conversation_id=conversation_id,
            start_date=filters.start_date,
            end_date=filters.end_date
        )
        
        response = {
            "session": session,
            "messages": messages
        }
        
        # 분석 결과 포함 여부
        if filters.include_analysis:
            response["analysis"] = {
                "sentiment": db.get_sentiment_analysis_by_conversation(conversation_id),
                "risk": db.get_risk_assessments_by_conversation(conversation_id),
                "health": db.get_health_monitoring_by_conversation(conversation_id)
            }
        
        return response
    except Exception as e:
        logger.error(f"Failed to get conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{conversation_id}")
async def end_conversation(
    conversation_id: str,
    db: MySQLManager = Depends(get_mysql_manager)
) -> Dict:
    """대화 종료"""
    try:
        manager = ConversationManager()
        manager.current_conversation_id = conversation_id
        success = manager.end_conversation()
        
        if not success:
            raise HTTPException(status_code=500, detail="대화 종료에 실패했습니다")
            
        return {"message": "대화가 성공적으로 종료되었습니다"}
    except Exception as e:
        logger.error(f"Failed to end conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
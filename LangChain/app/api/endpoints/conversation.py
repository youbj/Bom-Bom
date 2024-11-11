from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, Dict
from pydantic import BaseModel
from app.services.conversation_manager import ConversationManager

router = APIRouter()

class TextInput(BaseModel):
    text: str
    conversation_id: Optional[str] = None

@router.post("/start", response_model=Dict[str, str])
async def start_conversation():
    """새로운 대화 시작"""
    manager = ConversationManager()
    initial_response = await manager.process_text_input(
        text="",
        is_initial=True
    )
    return initial_response

@router.post("/process")
async def process_text(text_input: TextInput):
    """텍스트 처리"""
    manager = ConversationManager()
    
    try:
        if text_input.conversation_id:
            manager.current_conversation_id = text_input.conversation_id
            
        response = await manager.process_text_input(
            text=text_input.text,
            is_initial=False
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
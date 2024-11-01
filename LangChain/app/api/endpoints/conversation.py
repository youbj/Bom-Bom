from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, Dict
from pydantic import BaseModel
from app.services.conversation_manager import ConversationManager
from app.models.schema import ConversationResponse

router = APIRouter();

class TextInput(BaseModel):
    text: str
    conversation_id: Optional[str] = None

@router.post("/start", response_model=Dict[str, str])
async def start_conversation():
    """새로운 대화 시작"""
    manager = ConversationManager()
    conversation_id = manager.start_conversation()
    return {"conversation_id": conversation_id}

@router.post("/process")
async def process_text(text_input: TextInput):
    manager = ConversationManager()
    if text_input.conversation_id:
        manager.current_conversation_id = text_input.conversation_id
    else:
        manager.current_conversation_id = manager.start_conversation()
    
    response = await manager.process_text_input(text_input.text)
    return {
        "conversation_id": manager.current_conversation_id,
        **response
    }
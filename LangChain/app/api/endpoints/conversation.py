from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from typing import Dict, Any
from app.services.conversation_manager import ConversationManager
from app.api.deps import get_conversation_manager
import logging
import os  # os 모듈 추가

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/start")
async def start_conversation(
    manager: ConversationManager = Depends(get_conversation_manager)
) -> Dict[str, str]:
    """새 대화 세션 시작"""
    try:
        conversation_id = manager.start_conversation()
        return {"conversation_id": conversation_id}
    except Exception as e:
        logger.error(f"대화 시작 실패: {str(e)}")
        raise HTTPException(status_code=500, detail="대화 시작 실패")

@router.post("/{conversation_id}/audio")
async def process_audio(
    conversation_id: str,
    audio_file: UploadFile = File(...),
    manager: ConversationManager = Depends(get_conversation_manager)
) -> Dict[str, Any]:
    """음성 입력 처리"""
    try:
        # 업로드 디렉토리 생성
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        # 음성 파일 저장
        audio_path = os.path.join(upload_dir, f"{conversation_id}_{audio_file.filename}")
        
        with open(audio_path, "wb") as f:
            content = await audio_file.read()
            f.write(content)
        
        # 음성 처리 및 응답 생성 (await 추가)
        response = await manager.process_audio_input(audio_path)  # await 추가
        return response
        
    except Exception as e:
        logger.error(f"음성 처리 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # 임시 파일 정리
        try:
            if os.path.exists(audio_path):
                os.remove(audio_path)
        except Exception as e:
            logger.warning(f"임시 파일 삭제 실패: {str(e)}")
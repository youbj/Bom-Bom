from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from typing import Dict
from datetime import datetime
from app.services.report_generator import ReportGenerator
from app.api.deps import get_conversation_manager
from app.services.conversation_manager import ConversationManager  # 이 줄 추가

router = APIRouter()

@router.post("/generate")
async def generate_report(
    elderly_id: str,
    start_date: datetime,
    end_date: datetime,
    manager: ConversationManager = Depends(get_conversation_manager)
) -> Dict[str, str]:
    """보고서 생성"""
    try:
        report_path = manager.generate_report(
            start_date=start_date,
            end_date=end_date,
            elderly_id=elderly_id
        )
        return {"report_url": f"/api/v1/reports/download/{report_path}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/{report_name}")
async def download_report(report_name: str):
    """보고서 다운로드"""
    try:
        report_path = f"data/reports/{report_name}"
        return FileResponse(
            report_path,
            media_type='application/pdf',
            filename=report_name
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail="보고서를 찾을 수 없습니다")
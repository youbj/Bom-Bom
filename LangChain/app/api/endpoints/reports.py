from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from typing import Dict, List
from datetime import datetime
from app.services.report_generator import ReportGenerator
from app.database.mysql_manager import MySQLManager
from app.api.deps import get_mysql_manager
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/generate/{conversation_id}")
async def generate_report(
    conversation_id: str,
    start_date: datetime,
    end_date: datetime,
    db: MySQLManager = Depends(get_mysql_manager)
) -> Dict[str, str]:
    """보고서 생성"""
    try:
        # 대화 데이터 조회
        conversation_data = db.get_conversation_history(conversation_id)
        if not conversation_data:
            raise HTTPException(status_code=404, detail="대화 데이터를 찾을 수 없습니다")
        
        # 보고서 생성
        generator = ReportGenerator()
        report_path = generator.generate_pdf_report(
            conversation_data=conversation_data,
            start_date=start_date,
            end_date=end_date
        )
        
        # 상대 경로로 변환
        relative_path = os.path.basename(report_path)
        
        return {
            "report_path": relative_path,
            "download_url": f"/api/reports/download/{relative_path}"
        }
    except Exception as e:
        logger.error(f"Failed to generate report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/{report_name}")
async def download_report(report_name: str):
    """보고서 다운로드"""
    try:
        report_path = os.path.join("data/reports", report_name)
        
        if not os.path.exists(report_path):
            raise HTTPException(status_code=404, detail="보고서 파일을 찾을 수 없습니다")
            
        return FileResponse(
            report_path,
            media_type='application/pdf',
            filename=report_name
        )
    except Exception as e:
        logger.error(f"Failed to download report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list")
async def list_reports(
    conversation_id: str,
    db: MySQLManager = Depends(get_mysql_manager)
) -> List[Dict]:
    """생성된 보고서 목록 조회"""
    try:
        reports_dir = "data/reports"
        if not os.path.exists(reports_dir):
            return []
            
        reports = []
        for filename in os.listdir(reports_dir):
            if filename.startswith(f"report_{conversation_id}"):
                file_path = os.path.join(reports_dir, filename)
                reports.append({
                    "filename": filename,
                    "created_at": datetime.fromtimestamp(os.path.getctime(file_path)),
                    "size": os.path.getsize(file_path),
                    "download_url": f"/api/reports/download/{filename}"
                })
        
        return sorted(reports, key=lambda x: x['created_at'], reverse=True)
    except Exception as e:
        logger.error(f"Failed to list reports: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{report_name}")
async def delete_report(report_name: str):
    """보고서 삭제"""
    try:
        report_path = os.path.join("data/reports", report_name)
        
        if not os.path.exists(report_path):
            raise HTTPException(status_code=404, detail="보고서 파일을 찾을 수 없습니다")
            
        os.remove(report_path)
        return {"message": "보고서가 삭제되었습니다"}
    except Exception as e:
        logger.error(f"Failed to delete report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
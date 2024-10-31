
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from datetime import datetime
from app.services.conversation_analyzer import ConversationAnalyzer
from app.database.mysql_manager import MySQLManager
from app.api.deps import get_mysql_manager

router = APIRouter()

@router.get("/{conversation_id}")
async def get_conversation_analysis(
    conversation_id: str,
    db: MySQLManager = Depends(get_mysql_manager)
) -> Dict:
    """대화 분석 결과 조회"""
    try:
        analysis = db.get_analysis(conversation_id)
        if not analysis:
            raise HTTPException(status_code=404, detail="분석 결과를 찾을 수 없습니다")
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary/{elderly_id}")
async def get_analysis_summary(
    elderly_id: str,
    start_date: datetime,
    end_date: datetime,
    db: MySQLManager = Depends(get_mysql_manager)
) -> Dict:
    """기간별 분석 요약"""
    try:
        return db.get_analysis_summary(elderly_id, start_date, end_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
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
        # 메시지와 관련된 모든 분석 데이터 조회
        messages = db.get_conversation_history(conversation_id)
        if not messages:
            raise HTTPException(status_code=404, detail="대화를 찾을 수 없습니다")
            
        # 감정 분석 데이터
        sentiment_data = db.get_sentiment_analysis_by_conversation(conversation_id)
        
        # 위험 평가 데이터
        risk_data = db.get_risk_assessments_by_conversation(conversation_id)
        
        # 건강 모니터링 데이터
        health_data = db.get_health_monitoring_by_conversation(conversation_id)
        
        return {
            "messages": messages,
            "sentiment_analysis": sentiment_data,
            "risk_assessments": risk_data,
            "health_monitoring": health_data
        }
    except Exception as e:
        logger.error(f"Failed to get conversation analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary/{conversation_id}")
async def get_analysis_summary(
    conversation_id: str,
    start_date: datetime,
    end_date: datetime,
    db: MySQLManager = Depends(get_mysql_manager)
) -> Dict:
    """기간별 분석 요약"""
    try:
        # 대화 세션 기본 정보
        session = db.get_conversation_session(conversation_id)
        if not session:
            raise HTTPException(status_code=404, detail="대화 세션을 찾을 수 없습니다")
        
        # 메시지 통계
        message_stats = db.get_message_statistics(conversation_id, start_date, end_date)
        
        # 감정 분석 요약
        sentiment_summary = db.get_sentiment_summary(conversation_id, start_date, end_date)
        
        # 위험 평가 요약
        risk_summary = db.get_risk_assessment_summary(conversation_id, start_date, end_date)
        
        # 건강 상태 요약
        health_summary = db.get_health_monitoring_summary(conversation_id, start_date, end_date)
        
        # 주요 키워드
        keywords = db.get_top_keywords(conversation_id, start_date, end_date)
        
        return {
            "session_info": session,
            "message_statistics": message_stats,
            "sentiment_summary": sentiment_summary,
            "risk_summary": risk_summary,
            "health_summary": health_summary,
            "top_keywords": keywords
        }
    except Exception as e:
        logger.error(f"Failed to get analysis summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
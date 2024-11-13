from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Optional
from datetime import datetime
from app.database.mysql_manager import MySQLManager
from app.api.deps import get_mysql_manager
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/{conversation_id}")
async def get_conversation_analysis(
    conversation_id: str,
    db: MySQLManager = Depends(get_mysql_manager)
) -> Dict:
    """대화 분석 결과 조회"""
    try:
        # 대화 내용 조회
        conversation = await db.get_conversation_status(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="대화를 찾을 수 없습니다")
            
        # Memory 조회
        memories = await db.get_conversation_memories(conversation_id)
        
        # 분석 결과 집계
        analysis = {
            "total_messages": len(memories),
            "average_positivity": sum(m.get('positivity_score', 50) for m in memories) / len(memories) if memories else 50,
            "keywords": list(set(sum((m.get('keywords', []) for m in memories), []))),
            "response_plans": list(set(sum((m.get('response_plan', []) for m in memories), []))),
            "summaries": [m.get('summary') for m in memories if m.get('summary')],
        }
        
        return {
            "conversation_info": conversation,
            "analysis_result": analysis
        }
    except Exception as e:
        logger.error(f"Failed to get conversation analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary/{conversation_id}")
async def get_conversation_summary(
    conversation_id: str,
    db: MySQLManager = Depends(get_mysql_manager)
) -> Dict:
    """대화 요약 정보 조회"""
    try:
        # 대화 정보 조회
        conversation = await db.get_conversation_status(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="대화를 찾을 수 없습니다")
        
        # Memory 조회
        memories = await db.get_conversation_memories(conversation_id)
        
        # 요약 정보 구성
        summary = {
            "start_time": conversation.get('start_date'),
            "end_time": conversation.get('end_time'),
            "total_duration": (conversation.get('end_time') - conversation.get('start_date')).total_seconds() / 60 if conversation.get('end_time') else None,
            "total_turns": len(memories),
            "average_sentiment": sum(m.get('positivity_score', 50) for m in memories) / len(memories) if memories else 50,
            "main_topics": list(set(sum((m.get('keywords', []) for m in memories), [])))[:5],  # 상위 5개 키워드
            "key_summaries": [m.get('summary') for m in memories if m.get('summary')][-3:],  # 최근 3개 요약
        }
        
        return summary
    except Exception as e:
        logger.error(f"Failed to get conversation summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
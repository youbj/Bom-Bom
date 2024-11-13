from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Optional, List
from datetime import datetime
from app.database.mysql_manager import MySQLManager
from app.api.deps import get_mysql_manager
import logging
from statistics import mean

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/{conversation_id}")
async def get_conversation_analysis(
    conversation_id: str,
    db: MySQLManager = Depends(get_mysql_manager)
) -> Dict:
    """대화 분석 결과 조회"""
    try:
        # DB 초기화 확인
        await db.initialize()
        
        # 대화 내용 및 메모리 동시 조회
        conversation = await db.get_conversation_status(int(conversation_id))
        if not conversation:
            raise HTTPException(status_code=404, detail="대화를 찾을 수 없습니다")
            
        memories = await db.get_conversation_memories(int(conversation_id))
        
        if not memories:
            return {
                "conversation_info": conversation,
                "analysis_result": {
                    "total_messages": 0,
                    "average_positivity": 50,
                    "keywords": [],
                    "response_plans": [],
                    "summaries": []
                }
            }
        
        # 분석 결과 집계
        analysis = {
            "total_messages": len(memories),
            "average_positivity": mean([m.get('positivity_score', 50) for m in memories]),
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
        # DB 초기화 확인
        await db.initialize()
        
        # 대화 정보 및 메모리 동시 조회
        conversation = await db.get_conversation_status(int(conversation_id))
        if not conversation:
            raise HTTPException(status_code=404, detail="대화를 찾을 수 없습니다")
        
        memories = await db.get_conversation_memories(int(conversation_id))
        
        if not memories:
            return {
                "start_time": conversation.get('start_date'),
                "end_time": None,
                "total_duration": None,
                "total_turns": 0,
                "average_sentiment": 50,
                "main_topics": [],
                "key_summaries": []
            }
        
        # 요약 정보 구성
        end_time = conversation.get('end_time')
        start_time = conversation.get('start_date')
        
        summary = {
            "start_time": start_time,
            "end_time": end_time,
            "total_duration": (end_time - start_time).total_seconds() / 60 if end_time and start_time else None,
            "total_turns": len(memories),
            "average_sentiment": mean([m.get('positivity_score', 50) for m in memories]),
            "main_topics": list(set(sum((m.get('keywords', []) for m in memories), [])))[:5],
            "key_summaries": [m.get('summary') for m in memories if m.get('summary')][-3:]
        }
        
        return summary
    except Exception as e:
        logger.error(f"Failed to get conversation summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
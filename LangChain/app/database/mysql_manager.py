from mysql.connector import pooling
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging
import json
from app.config import settings

logger = logging.getLogger(__name__)

class MySQLManager:
    def __init__(self):
        """데이터베이스 연결 풀 초기화"""
        self.dbconfig = {
            "host": settings.mysql.host,
            "port": settings.mysql.port,
            "database": settings.mysql.database,
            "user": settings.mysql.user,
            "password": settings.mysql.password
        }
        
        try:
            self.connection_pool = pooling.MySQLConnectionPool(
                pool_name="mypool",
                pool_size=5,
                **self.dbconfig
            )
            logger.info("MySQL connection pool initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize MySQL connection pool: {str(e)}")
            raise

    def get_connection(self):
        """커넥션 풀에서 연결 가져오기"""
        return self.connection_pool.get_connection()

    def start_conversation(self, conversation_id: str) -> bool:
        """새로운 대화 세션 시작"""
        query = """
        INSERT INTO conversation_sessions (conversation_id)
        VALUES (%s)
        """
        
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (conversation_id,))
                    conn.commit()
                    return True
        except Exception as e:
            logger.error(f"Failed to start conversation: {str(e)}")
            return False

    def end_conversation(self, conversation_id: str) -> bool:
        """대화 세션 종료"""
        query = """
        UPDATE conversation_sessions 
        SET end_time = CURRENT_TIMESTAMP
        WHERE conversation_id = %s
        """
        
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (conversation_id,))
                    conn.commit()
                    return True
        except Exception as e:
            logger.error(f"Failed to end conversation: {str(e)}")
            return False

    def save_message(self, message_data: Dict) -> Optional[int]:
        """메시지 저장 및 message_id 반환"""
        message_query = """
        INSERT INTO messages (conversation_id, speaker_type, text_content, message_number)
        VALUES (%s, %s, %s, %s)
        """
        
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    # 메시지 저장
                    cursor.execute(message_query, (
                        message_data['conversation_id'],
                        message_data['speaker_type'],
                        message_data['text_content'],
                        message_data['message_number']
                    ))
                    
                    message_id = cursor.lastrowid
                    conn.commit()
                    
                    # 감정 분석 결과 저장
                    if 'sentiment_analysis' in message_data:
                        self._save_sentiment_analysis(message_id, message_data['sentiment_analysis'])
                    
                    # 위험 평가 저장
                    if 'risk_assessment' in message_data:
                        self._save_risk_assessment(message_id, message_data['risk_assessment'])
                    
                    # 요약 저장
                    if 'summary' in message_data:
                        self._save_summary(message_id, message_data['summary'])
                    
                    # 키워드 저장
                    if 'keywords' in message_data:
                        self._save_keywords(message_id, message_data['keywords'])
                    
                    return message_id
                    
        except Exception as e:
            logger.error(f"Failed to save message: {str(e)}")
            return None

    def _save_sentiment_analysis(self, message_id: int, sentiment_data: Dict) -> bool:
        """감정 분석 결과 저장"""
        query = """
        INSERT INTO sentiment_analysis (
            message_id, sentiment_score, is_positive, confidence,
            emotional_state, emotion_score, emotion_description
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (
                        message_id,
                        sentiment_data.get('score'),
                        sentiment_data.get('is_positive'),
                        sentiment_data.get('confidence'),
                        sentiment_data.get('emotional_state'),
                        sentiment_data.get('emotion_score'),
                        sentiment_data.get('emotion_description')
                    ))
                    conn.commit()
                    return True
        except Exception as e:
            logger.error(f"Failed to save sentiment analysis: {str(e)}")
            return False

    def _save_risk_assessment(self, message_id: int, risk_data: Dict) -> bool:
        """위험 평가 결과 저장"""
        query = """
        INSERT INTO risk_assessments (
            message_id, risk_level, risk_factors, needed_actions
        ) VALUES (%s, %s, %s, %s)
        """
        
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (
                        message_id,
                        risk_data.get('risk_level'),
                        json.dumps(risk_data.get('risk_factors', [])),
                        json.dumps(risk_data.get('needed_actions', []))
                    ))
                    conn.commit()
                    return True
        except Exception as e:
            logger.error(f"Failed to save risk assessment: {str(e)}")
            return False

    def _save_summary(self, message_id: int, summary_text: str) -> bool:
        """메시지 요약 저장"""
        query = """
        INSERT INTO message_summaries (message_id, summary_text)
        VALUES (%s, %s)
        """
        
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (message_id, summary_text))
                    conn.commit()
                    return True
        except Exception as e:
            logger.error(f"Failed to save summary: {str(e)}")
            return False

    def _save_keywords(self, message_id: int, keywords: List[str]) -> bool:
        """키워드 저장 및 메시지와 연결"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    for keyword in keywords:
                        # 키워드 저장 (이미 있으면 무시)
                        cursor.execute("""
                            INSERT IGNORE INTO keywords (keyword)
                            VALUES (%s)
                        """, (keyword,))
                        
                        # 키워드 ID 가져오기
                        cursor.execute("""
                            SELECT id FROM keywords WHERE keyword = %s
                        """, (keyword,))
                        keyword_id = cursor.fetchone()[0]
                        
                        # 메시지-키워드 연결
                        cursor.execute("""
                            INSERT IGNORE INTO message_keywords (message_id, keyword_id)
                            VALUES (%s, %s)
                        """, (message_id, keyword_id))
                    
                    conn.commit()
                    return True
        except Exception as e:
            logger.error(f"Failed to save keywords: {str(e)}")
            return False

    def save_health_monitoring(self, health_data: Dict) -> bool:
        """건강 상태 모니터링 데이터 저장"""
        query = """
        INSERT INTO health_monitoring (
            conversation_id, health_status, physical_health_score,
            mental_health_score, sleep_quality_score, appetite_level_score
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (
                        health_data['conversation_id'],
                        health_data.get('health_status'),
                        health_data.get('physical_health_score'),
                        health_data.get('mental_health_score'),
                        health_data.get('sleep_quality_score'),
                        health_data.get('appetite_level_score')
                    ))
                    conn.commit()
                    return True
        except Exception as e:
            logger.error(f"Failed to save health monitoring data: {str(e)}")
            return False

    def get_conversation_history(self, conversation_id: str) -> List[Dict]:
        """대화 히스토리 조회"""
        query = """
        SELECT m.*, 
               sa.sentiment_score, sa.emotional_state,
               ra.risk_level, ra.risk_factors,
               ms.summary_text
        FROM messages m
        LEFT JOIN sentiment_analysis sa ON m.id = sa.message_id
        LEFT JOIN risk_assessments ra ON m.id = ra.message_id
        LEFT JOIN message_summaries ms ON m.id = ms.message_id
        WHERE m.conversation_id = %s
        ORDER BY m.message_number
        """
        
        try:
            with self.get_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(query, (conversation_id,))
                    return cursor.fetchall()
        except Exception as e:
            logger.error(f"Failed to get conversation history: {str(e)}")
            return []

    def close(self):
        """연결 풀 정리"""
        # connection pool will be automatically closed
        pass
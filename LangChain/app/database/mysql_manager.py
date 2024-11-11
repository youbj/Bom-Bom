import mysql.connector
from mysql.connector import pooling
from typing import Dict, List, Optional
from datetime import datetime
import logging
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
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
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

    def save_conversation(self, conversation_data: Dict) -> bool:
        """대화 내용 저장"""
        query = """
        INSERT INTO conversations (
            conversation_id, speaker_type, text_content, 
            sentiment_score, summary, created_at
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            values = (
                conversation_data['conversation_id'],
                conversation_data['speaker_type'],
                conversation_data['text_content'],
                conversation_data['sentiment_score'],
                conversation_data['summary'],
                datetime.now()
            )
            
            cursor.execute(query, values)
            conn.commit()
            
            logger.info(f"Saved conversation: {conversation_data['conversation_id']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save conversation: {str(e)}")
            return False
            
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def get_conversations(self, 
                            elderly_id: Optional[str] = None,
                            start_date: Optional[datetime] = None,
                            end_date: Optional[datetime] = None) -> List[Dict]:
        """대화 내역 조회"""
        query = """
        SELECT * FROM conversations 
        WHERE 1=1
        """
        params = []
        
        if elderly_id:
            query += " AND elderly_id = %s"
            params.append(elderly_id)
            
        if start_date:
            query += " AND created_at >= %s"
            params.append(start_date)
            
        if end_date:
            query += " AND created_at <= %s"
            params.append(end_date)
            
        query += " ORDER BY created_at DESC"
        
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to get conversations: {str(e)}")
            return []
            
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def close(self):
        """연결 풀 정리"""
        # connection pool will be automatically closed
        pass
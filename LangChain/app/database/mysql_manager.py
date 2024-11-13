import mysql.connector
from mysql.connector import pooling
import logging
from typing import Dict, List, Optional
from datetime import datetime
from app.config import settings

logger = logging.getLogger(__name__)

class MySQLManager:
    def __init__(self):
        """데이터베이스 매니저 초기화"""
        try:
            # config 먼저 설정
            self.config = {
                "host": settings.mysql.host,
                "port": settings.mysql.port,
                "database": settings.mysql.database,
                "user": settings.mysql.user,
                "password": settings.mysql.password,
                "charset": settings.mysql.charset
            }
            
            # 연결 생성
            self.connection = mysql.connector.connect(**self.config)
            logger.info("MySQL connection established")
            
        except Exception as e:
            logger.error(f"Failed to initialize MySQL connection: {str(e)}")
            raise

    def reconnect_if_needed(self):
        """필요한 경우 재연결"""
        try:
            if not self.connection.is_connected():
                self.connection = mysql.connector.connect(**self.config)
                logger.info("MySQL connection re-established")
        except Exception as e:
            logger.error(f"Failed to reconnect: {str(e)}")
            raise

    def close(self):
        """연결 종료"""
        try:
            if hasattr(self, 'connection') and self.connection.is_connected():
                self.connection.close()
                logger.info("MySQL connection closed")
        except Exception as e:
            logger.error(f"Error closing connection: {str(e)}")

    def start_conversation(self, memory_id: int, senior_id: int = 1) -> Optional[int]:
        """새로운 대화 세션 시작"""
        self.reconnect_if_needed()
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO Conversation (memory_id, senior_id, start_date)
                VALUES (%s, %s, NOW())
            """, (memory_id, senior_id))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            logger.error(f"Failed to start conversation: {str(e)}")
            return None
        finally:
            cursor.close()

    def end_conversation(self, conversation_id: int) -> bool:
        """대화 세션 종료"""
        self.reconnect_if_needed()
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                UPDATE Conversation 
                SET end_time = CURRENT_TIME()
                WHERE conversation_id = %s
            """, (conversation_id,))
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to end conversation: {str(e)}")
            return False
        finally:
            cursor.close()

    def get_conversation_status(self, conversation_id: int) -> Optional[Dict]:
        """대화 상태 조회"""
        self.reconnect_if_needed()
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT c.*, COUNT(m.id) as message_count
                FROM Conversation c
                LEFT JOIN Memory m ON c.conversation_id = m.conversation_id
                WHERE c.conversation_id = %s
                GROUP BY c.conversation_id
            """, (conversation_id,))
            return cursor.fetchone()
        except Exception as e:
            logger.error(f"Failed to get conversation status: {str(e)}")
            return None
        finally:
            cursor.close()

    def save_memory(self, data: Dict) -> Optional[int]:
        """메모리 저장"""
        self.reconnect_if_needed()
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO Memory (
                    memory_id, conversation_id, speaker, content, 
                    summary, positivity_score, keywords, response_plan
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                data['memory_id'],
                data['conversation_id'],
                data['speaker'],
                data['content'],
                data.get('summary'),
                data.get('positivity_score', 50),
                data.get('keywords', '[]'),
                data.get('response_plan', '[]')
            ))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            logger.error(f"Failed to save memory: {str(e)}")
            return None
        finally:
            cursor.close()

    def __del__(self):
        """소멸자"""
        self.close()
import aiomysql
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
from app.config import settings

logger = logging.getLogger(__name__)

class MySQLManager:
    def __init__(self):
        """데이터베이스 매니저 초기화"""
        self.pool = None
        self.config = {
            "host": settings.mysql.host,
            "port": settings.mysql.port,
            "db": settings.mysql.database,
            "user": settings.mysql.user,
            "password": settings.mysql.password,
            "charset": settings.mysql.charset,
            "autocommit": True,
            "minsize": 1,
            "maxsize": 10
        }
    async def ensure_connection(self):
        """연결 보장"""
        if not self.pool:
            try:
                self.pool = await aiomysql.create_pool(**self.config)
                logger.info("MySQL connection pool established")
            except Exception as e:
                logger.error(f"Failed to initialize MySQL pool: {str(e)}")
                raise

    async def initialize(self):
        """비동기 풀 초기화"""
        if not self.pool:
            try:
                self.pool = await aiomysql.create_pool(**self.config)
                logger.info("MySQL connection pool established")
            except Exception as e:
                logger.error(f"Failed to initialize MySQL pool: {str(e)}")
                raise

    async def close(self):
        """연결 종료"""
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            logger.info("MySQL connection pool closed")

    async def get_conversation_status(self, conversation_id: int) -> Optional[Dict]:
        """대화 상태 조회"""
        await self.ensure_connection()
        
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                try:
                    await cursor.execute("""
                        SELECT c.*, COUNT(m.id) as message_count
                        FROM conversation c
                        LEFT JOIN memory m ON c.conversation_id = m.conversation_id
                        WHERE c.conversation_id = %s
                        GROUP BY c.conversation_id
                    """, (conversation_id,))
                    result = await cursor.fetchone()
                    return dict(result) if result else None
                except Exception as e:
                    logger.error(f"Failed to get conversation status: {str(e)}")
                    return None

    async def get_conversation_memories(self, conversation_id: int) -> List[Dict]:
        """대화 메모리 조회"""
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                try:
                    await cursor.execute("""
                        SELECT *
                        FROM memory
                        WHERE conversation_id = %s
                        ORDER BY id ASC
                    """, (conversation_id,))
                    results = await cursor.fetchall()
                    
                    # JSON 필드 파싱
                    for result in results:
                        if result.get('keywords'):
                            result['keywords'] = json.loads(result['keywords'])
                        if result.get('response_plan'):
                            result['response_plan'] = json.loads(result['response_plan'])
                    
                    return [dict(row) for row in results]
                except Exception as e:
                    logger.error(f"Failed to get conversation memories: {str(e)}")
                    return []

    async def get_conversation_messages(self, conversation_id: str) -> List[Dict]:
        """대화의 모든 메시지 조회"""
        await self.ensure_connection()
        
        query = """
            SELECT speaker, content, memory_id 
            FROM memory 
            WHERE conversation_id = %s 
            ORDER BY id ASC
        """
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, (conversation_id,))
                    messages = await cursor.fetchall()
                    return [
                        {
                            'speaker': msg[0],
                            'content': msg[1],
                            'memory_id': msg[2]
                        }
                        for msg in messages
                    ]
        except Exception as e:
            logger.error(f"Failed to get conversation messages: {str(e)}")
            return []
        
    async def start_conversation(self, memory_id: str, senior_id: int = 1) -> Optional[int]:
        """새로운 대화 세션 시작"""
        await self.ensure_connection()
        
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                try:
                    await cursor.execute("""
                        INSERT INTO conversation (memory_id, senior_id, start_date)
                        VALUES (%s, %s, NOW())
                    """, (memory_id, senior_id))
                    await conn.commit()
                    return cursor.lastrowid
                except Exception as e:
                    logger.error(f"Failed to start conversation: {str(e)}")
                    return None


    async def save_memory(self, data: Dict) -> Optional[int]:
        """메모리 저장"""
        await self.ensure_connection()
        
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                try:
                    await cursor.execute("""
                        INSERT INTO memory (
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
                    await conn.commit()
                    return cursor.lastrowid
                except Exception as e:
                    logger.error(f"Failed to save memory: {str(e)}")
                    return None

    async def close(self):
        """연결 종료"""
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            logger.info("MySQL connection pool closed")

    async def end_conversation(self, conversation_id: int) -> bool:
        """대화 세션 종료"""
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                try:
                    # 평균 점수 계산 및 종료 시간 업데이트
                    await cursor.execute("""
                        UPDATE conversation c
                        SET end_time = CURTIME(),
                            avg_score = (
                                SELECT AVG(positivity_score)
                                FROM memory
                                WHERE conversation_id = %s
                            )
                        WHERE conversation_id = %s
                    """, (conversation_id, conversation_id))
                    return True
                except Exception as e:
                    logger.error(f"Failed to end conversation: {str(e)}")
                    return False
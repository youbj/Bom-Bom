from typing import AsyncGenerator
from fastapi import Depends
from app.services.conversation_manager import ConversationManager
from app.services.gpt_service import GPTService
from app.database.mysql_manager import MySQLManager

async def get_mysql_manager() -> AsyncGenerator[MySQLManager, None]:
    """MySQLManager 의존성 제공"""
    manager = MySQLManager()
    try:
        yield manager
    finally:
        await manager.close()  # 비동기 close 호출

async def get_gpt_service() -> AsyncGenerator[GPTService, None]:
    """GPTService 의존성 제공"""
    gpt_service = GPTService()
    try:
        yield gpt_service
    finally:
        if hasattr(gpt_service, 'producer'):
            gpt_service.producer.flush()
        await gpt_service.aclose()  # 비동기 정리 추가

async def get_conversation_manager(
    mysql_manager: MySQLManager = Depends(get_mysql_manager),
    gpt_service: GPTService = Depends(get_gpt_service)
) -> AsyncGenerator[ConversationManager, None]:
    """ConversationManager 의존성 제공"""
    manager = ConversationManager(mysql_manager=mysql_manager, gpt_service=gpt_service)
    try:
        yield manager
    finally:
        if hasattr(manager, 'gpt_service'):
            manager.gpt_service.reset_memory()
            await manager.gpt_service.aclose()  # 비동기 정리 추가
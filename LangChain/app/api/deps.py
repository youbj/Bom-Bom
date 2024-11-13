from typing import Generator
from fastapi import Depends
from app.services.conversation_manager import ConversationManager
from app.services.gpt_service import GPTService
from app.database.mysql_manager import MySQLManager

def get_mysql_manager() -> Generator[MySQLManager, None, None]:
    """MySQLManager 의존성 제공"""
    manager = MySQLManager()
    try:
        yield manager
    finally:
        manager.close()

def get_gpt_service() -> Generator[GPTService, None, None]:
    """GPTService 의존성 제공"""
    gpt_service = GPTService()
    try:
        yield gpt_service
    finally:
        if hasattr(gpt_service, 'producer'):
            gpt_service.producer.flush()

def get_conversation_manager(
    mysql_manager: MySQLManager = Depends(get_mysql_manager),
    gpt_service: GPTService = Depends(get_gpt_service)
) -> Generator[ConversationManager, None, None]:
    """ConversationManager 의존성 제공"""
    manager = ConversationManager(mysql_manager=mysql_manager, gpt_service=gpt_service)
    try:
        yield manager
    finally:
        if hasattr(manager, 'gpt_service'):
            manager.gpt_service.reset_memory()

from typing import Generator
from app.services.conversation_manager import ConversationManager
from app.services.kafka_manager import KafkaManager
from app.database.mysql_manager import MySQLManager

def get_conversation_manager() -> Generator[ConversationManager, None, None]:
    manager = ConversationManager()
    try:
        yield manager
    finally:
        # 필요한 정리 작업
        pass

def get_kafka_manager() -> Generator[KafkaManager, None, None]:
    manager = KafkaManager()
    try:
        yield manager
    finally:
        pass

def get_mysql_manager() -> Generator[MySQLManager, None, None]:
    manager = MySQLManager()
    try:
        yield manager
    finally:
        manager.close()
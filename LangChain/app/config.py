from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()

class KafkaSettings(BaseModel):
    """Kafka 설정"""
    bootstrap_servers: str = "k11a202.p.ssafy.io:9092"
    conversation_topic: str = "elderly_conversations"
    analysis_topic: str = "conversation_analysis"
    group_id: str = "elderly_care_group"
    retention_period: int = 10

class MySQLSettings(BaseModel):
    """MySQL 설정"""
    host: str = "localhost"
    port: int = 3306
    database: str = "elderly_care"
    user: str = "root"
    password: str = "1234"
    charset: str = "utf8mb4"
    pool_size: int = 5

    def get_connection_url(self) -> str:
        return f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

class GPTSettings(BaseModel):
    """GPT 설정"""
    model_config = ConfigDict(
        protected_namespaces=()  # 경고 제거를 위한 설정
    )
    api_key: str = os.getenv("OPENAI_API_KEY", "")
    model_name: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 150

class Settings(BaseSettings):
    """전체 설정"""
    model_config = {"env_file": ".env", "extra": "allow"}
    
    # 대화 관리 설정
    max_conversation_turns: int = 16
    warning_threshold: int = 12
    memory_expiry_minutes: int = 30
    
    # 컴포넌트 설정
    kafka: KafkaSettings = KafkaSettings()
    mysql: MySQLSettings = MySQLSettings()
    gpt: GPTSettings = GPTSettings()

settings = Settings()
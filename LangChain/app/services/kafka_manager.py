from typing import Dict, List
import logging
from datetime import datetime
from confluent_kafka import Producer, Consumer, KafkaError
import json
from app.config import settings

logger = logging.getLogger(__name__)

class KafkaManager:
    def __init__(self):
        """Kafka 매니저 초기화"""
        self.producer_config = {
            'bootstrap.servers': settings.kafka.bootstrap_servers,
            'client.id': 'elderly_care_producer'
        }
        
        self.consumer_config = {
            'bootstrap.servers': settings.kafka.bootstrap_servers,
            'group.id': settings.kafka.group_id,
            'auto.offset.reset': 'earliest'
        }
        
        self.producer = Producer(self.producer_config)
        self.consumer = Consumer(self.consumer_config)
        self.consumer.subscribe([settings.kafka.conversation_topic])
        
    def store_conversation(self, conversation_data: Dict):
        """대화 내용을 Kafka에 저장"""
        try:
            # 타임스탬프 추가
            conversation_data['timestamp'] = datetime.now().isoformat()
            
            # JSON으로 직렬화
            message = json.dumps(conversation_data)
            
            # Kafka로 메시지 전송
            self.producer.produce(
                settings.kafka.conversation_topic,
                value=message.encode('utf-8'),
                callback=self._delivery_report
            )
            
            # 버퍼 플러시
            self.producer.flush()
            
            logger.info(f"대화 내용이 Kafka에 저장되었습니다: {conversation_data.get('conversation_id', 'unknown')}")
            
        except Exception as e:
            logger.error(f"Kafka 메시지 저장 실패: {str(e)}")
            raise
    
    def get_recent_conversations(self, days: int = 10) -> List[Dict]:
        """최근 대화 내역 조회"""
        conversations = []
        try:
            # 타임아웃 설정 (10초)
            timeout = 10
            messages_to_read = 100  # 최대 읽을 메시지 수
            
            while len(conversations) < messages_to_read:
                msg = self.consumer.poll(timeout=timeout)
                
                if msg is None:
                    break
                
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        logger.error(f"Kafka 에러: {msg.error()}")
                        break
                
                try:
                    # 메시지 디코딩 및 파싱
                    value = json.loads(msg.value().decode('utf-8'))
                    
                    # 타임스탬프 확인
                    msg_datetime = datetime.fromisoformat(value['timestamp'])
                    if (datetime.now() - msg_datetime).days <= days:
                        conversations.append(value)
                    
                except json.JSONDecodeError as e:
                    logger.error(f"JSON 파싱 에러: {str(e)}")
                except Exception as e:
                    logger.error(f"메시지 처리 중 에러 발생: {str(e)}")
            
            return conversations
            
        except Exception as e:
            logger.error(f"대화 내역 조회 중 에러 발생: {str(e)}")
            return []
        
    def _delivery_report(self, err, msg):
        """Kafka 전송 결과 콜백"""
        if err is not None:
            logger.error(f'메시지 전송 실패: {err}')
        else:
            logger.info(f'메시지 전송 성공: {msg.topic()} [{msg.partition()}]')
            
    def __del__(self):
        """소멸자: 리소스 정리"""
        if hasattr(self, 'producer'):
            self.producer.flush()
        if hasattr(self, 'consumer'):
            self.consumer.close()
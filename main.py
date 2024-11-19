from fastapi import FastAPI, BackgroundTasks
from kafka import KafkaConsumer
import asyncio
import json
import logging
import uvicorn
import torch
import pandas as pd
import pickle
import numpy as np
from os.path import exists
from dataloader.dataset import FSLDataset
from runner.utils import get_config, extract_test_sample
from model.vit import ViT
import runner.proto as proto
import torch.nn.functional as F

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 전역 변수 선언
global model, z_proto, consumer, mac_dict, P_COUNT
model = None
z_proto = None
consumer = None
P_COUNT = 0

# FastAPI 앱 초기화
app = FastAPI()

# 설정 로드
logger.info("Loading configuration")
config = get_config('config.yaml')
use_cuda = config['GPU']['cuda']
device = torch.device("cuda:0" if use_cuda else "cpu")

# 기본 설정
KAFKA_TOPIC = 'CSI3'
KAFKA_BOOTSTRAP_SERVERS = ['k11a202.p.ssafy.io:9092']
mac = config['application']['client']['mac']
window_size = config['SVL']['dataset']['window_size']
num_sub = config['subcarrier'][config['application']['client']["bandwidth"]]
activities = config['application']['client']["activity_labels"]
columns = []
for i in range(0, num_sub):
    columns.append('_'+str(i))
mac_dict = {mac: pd.DataFrame(columns=columns)}
null_pilot_col_list = ['_' + str(x + 32) for x in [-32, -31, -30, -29, -21, -7, 0, 7, 21, 29, 30, 31]]
def initialize_model():
    """모델 초기화 및 로드"""
    global model
    logger.info("Initializing model")
    try:
        model = ViT(
            in_channels=config['application']['model']['ViT']["in_channels"],
            patch_size=(config['application']['model']['ViT']["patch_size"], 
                       config['subcarrier'][config['application']['client']["bandwidth"]]),
            embed_dim=config['application']['model']['ViT']["embed_dim"],
            num_layers=config['application']['model']['ViT']["num_layers"],
            num_heads=config['application']['model']['ViT']["num_heads"],
            mlp_dim=config['application']['model']['ViT']["mlp_dim"],
            num_classes=len(config['application']['client']["activity_labels"]),
            in_size=[config['application']['client']["window_size"], 
                    config['subcarrier'][config['application']['client']["bandwidth"]]]
        )
        model.load_state_dict(torch.load(
            config['application']['SVL']['save_model_path'],
            map_location=device
        ))

        if use_cuda:
            model.to(config['GPU']['gpu_ids'][0])  # 두 번째 코드처럼 GPU ID를 명시적으로 할당
        logger.info("Model initialized and loaded successfully")
    except Exception as e:
        logger.error(f"Error initializing model: {e}")
        raise

def create_prototypes():
    """프로토타입 생성"""
    global z_proto
    logger.info("Creating prototypes")
    try:
        n_way = config['FSL']['test']['n_way']
        n_support = config['FSL']['test']['n_support']
        n_query = config['FSL']['test']['n_query']

        support_data = FSLDataset(
            config['FSL']['dataset']['test_dataset_path'],
            win_size=window_size,
            mode='test',
            mac=False, time=False
        )
        logger.info(f"Support data loaded with shape: {support_data.data_x.shape}")

        support_x, support_y = support_data.data_x, support_data.data_y
        support_x = np.expand_dims(support_x, axis=1)
        support_sample = extract_test_sample(n_way, n_support, n_query, support_x, support_y, config)
        z_proto = model.create_protoNet(support_sample)
        logger.info(f"Prototypes created with shape: {z_proto.shape}")
    except Exception as e:
        logger.error(f"Error creating prototypes: {e}")
        raise

def initialize_kafka_consumer():
    """Kafka 컨슈머 초기화"""
    global consumer
    logger.info("Initializing Kafka consumer")
    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            group_id='my_group',
            auto_offset_reset='latest',
            enable_auto_commit=True
        )
        logger.info("Kafka consumer initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing Kafka consumer: {e}")
        raise

def get_prediction_probabilities(logits):
    """예측 확률 계산"""
    probabilities = F.softmax(logits, dim=1)
    return probabilities.squeeze().cpu().numpy()

async def process_message(message):
    """메시지 처리"""
    global P_COUNT, mac_dict
    try:
        buffer = pickle.loads(message)
        if not buffer:
            logger.error("Failed to receive data!")
            return None
        P_COUNT += 1
        logger.debug(f"Received buffer length: {len(buffer)}")
        
        columns_with_prefix = ['_' + str(i) for i in range(num_sub)]
        csi_df = pd.DataFrame([buffer], columns=columns_with_prefix)
        
        try:
            mac_dict[mac] = pd.concat([mac_dict[mac], csi_df], ignore_index=True)
            
            if len(mac_dict[mac]) == window_size and (P_COUNT == window_size or P_COUNT == window_size//2):
                # 데이터 준비
                c_data = np.array(mac_dict[mac])
                c_data = torch.from_numpy(c_data).unsqueeze(0).unsqueeze(0).float().to(device)
                
                with torch.no_grad():
                    # 모델 예측
                    outputs = model(c_data)
                    # 소프트맥스 적용
                    probabilities = F.softmax(outputs, dim=1)
                    # 가장 높은 확률을 가진 클래스 선택
                    y_hat = torch.argmax(probabilities, dim=1)
                    
                    # 결과 및 확률 처리
                    result = activities[y_hat.item()]
                    prob_dict = {
                        activities[i]: f"{prob:.2%}" 
                        for i, prob in enumerate(probabilities[0].cpu().numpy())
                    }
                    
                    logger.info(f'Prediction result: {result}')
                
                # 데이터프레임 업데이트
                mac_dict[mac].drop(0, inplace=True)
                mac_dict[mac].reset_index(drop=True, inplace=True)
                P_COUNT = 0
                
                return {
                    'predicted_activity': result,
                    'probabilities': prob_dict
                }
                
            elif len(mac_dict[mac]) == window_size:
                # window_size에 도달했지만 P_COUNT가 조건에 맞지 않을 때
                mac_dict[mac].drop(0, inplace=True)
                mac_dict[mac].reset_index(drop=True, inplace=True)
                
            elif len(mac_dict[mac]) > window_size:
                # window_size를 초과할 경우 처리
                logger.warning(f"DataFrame size ({len(mac_dict[mac])}) exceeded window_size ({window_size}), resetting buffer")
                mac_dict[mac] = pd.DataFrame(columns=columns_with_prefix)
                P_COUNT = 0
            
        except Exception as e:
            logger.error(f'Error in message processing: {e}', exc_info=True)
            return None
            
    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        return None
    
def kafka_message_handler():
    """Kafka 메시지 처리 핸들러"""
    logger.info("Starting Kafka message handler")
    try:
        for message in consumer:
            asyncio.run(process_message(message.value))
    except Exception as e:
        logger.error(f"Error in Kafka message handler: {e}")
        raise

@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 실행"""
    try:
        logger.info("Starting up application")
        initialize_model()
        # create_prototypes()
        initialize_kafka_consumer()
        loop = asyncio.get_running_loop()
        loop.run_in_executor(None, kafka_message_handler)  # Kafka 소비 작업을 별도의 스레드로 실행
        logger.info("Application startup complete")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "status": "running",
        "model_loaded": model is not None,
        "prototypes_created": z_proto is not None,
        "kafka_connected": consumer is not None
    }

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {
        "status": "healthy",
        "model_status": "loaded" if model is not None else "not_loaded",
        "prototype_status": "created" if z_proto is not None else "not_created",
        "kafka_status": "connected" if consumer is not None else "not_connected"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
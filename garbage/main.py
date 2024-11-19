from fastapi import FastAPI
import torch
from model.vit import ViT
from runner.utils import get_config
from model.lstm import BiLSTMModel
from kafka import KafkaConsumer
import json
import threading
import numpy as np
import pandas as pd
import torch.nn.functional as F
import pickle
import time
from scipy.signal import butter, filtfilt

app = FastAPI()

# Configuration and global variables
global config, P_COUNT, start_time, message_count, predict_counter
config = get_config('config.yaml')
mac = config['application']['client']['mac'].strip()  # 공백 제거
P_COUNT = 0
window_size = config['application']['client']['window_size']
num_sub = config['subcarrier'][config['application']['client']["bandwidth"]]
activities = config['application']['client']["activity_labels"]
# columns = ['_' + str(i) for i in range(num_sub)]
activities = ["empty", "walk", "stand", "fall"]  # 예측할 활동 레이블 # 필요한 서브캐리어 데이터 인덱스
null_pilot_col_list = ['_' + str(x + 32) for x in [-32, -31, -30, -29, -21, -7, 0, 7, 21, 29, 30, 31]]
exclude_indices = [0, 1, 2, 3, 11, 25, 32, 39, 53, 61, 62, 63]  # 제외할 인덱스 목록
# Message count and start time for tracking
columns = [str(i) for i in range(64) if i not in exclude_indices]
message_count = 0
start_time = time.time()
predict_counter = 1  # 예측 결과 번호를 추적하는 변수

global mac_dict
mac_dict = {}
mac_dict[mac] = pd.DataFrame(columns=columns)
def butterworth_filter(data, cutoff=25, fs=200, order=5):
    """버터워스 필터 적용"""
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, data)

def preprocess_data(data):
    """
    64개의 서브캐리어 데이터에서 지정된 인덱스를 제외한 52개의 데이터만 추출하고 필터링
    """
    # 제외할 인덱스 리스트
    exclude_indices = [0, 1, 2, 3, 11, 25, 32, 39, 53, 61, 62, 63]
    
    # 버터워스 필터 적용
    filtered_data = butterworth_filter(data, cutoff=25, fs=200, order=5)
    
    # 제외할 인덱스를 제외한 데이터만 선택
    selected_data = [filtered_data[i] for i in range(len(filtered_data)) if i not in exclude_indices]
    
    
    return np.array(selected_data, dtype=np.float32)

# def consume_messages():
#     """Kafka 메시지 소비 및 처리"""
#     global P_COUNT, message_count, predict_counter
#     for message in consumer:
#         try:
#             buffer = message.value[:2048]
#             try:
#                 buffer = pickle.loads(buffer)
#             except Exception as e:
#                 print("Failed to deserialize message:", e)
#                 continue
            
#             try:
#                 csi_df = pd.DataFrame([buffer], columns=columns)
#             except Exception as e:
#                 print("Failed to convert to DataFrame:", e)
#                 continue
#             P_COUNT += 1
#             message_count += 1
            
#             try:
#                 mac_dict[mac] = pd.concat([mac_dict[mac], csi_df], ignore_index=True)

#                 if len(mac_dict[mac]) == window_size and (P_COUNT == window_size or P_COUNT == window_size // 2):
#                     c_data = np.array(mac_dict[mac])
#                     # c_data = torch.from_numpy(c_data).unsqueeze(0).unsqueeze(0).float()
#                     c_data = torch.from_numpy(c_data).squeeze(0).float()  # channels 차원을 제거하여 3D로 만듦
#                     print("c_data = ",c_data)
#                     outputs = model(c_data)
#                     outputs = F.log_softmax(outputs, dim=1)
#                     probabilities = F.softmax(outputs, dim=1)
#                     y_hat = torch.from_numpy(np.array([np.argmax(outputs.cpu().data.numpy()[ii]) for ii in range(len(outputs))]))
#                     print(f'Predict result {predict_counter}:', activities[y_hat[0]])
#                     probs_percent = probabilities[0].detach().cpu().numpy() * 100
#                     print("\nProbabilities for each activity:")
#                     for activity, prob in zip(activities, probs_percent):
#                         print(f"{activity}: {prob:.2f}%")
#                     mac_dict[mac].drop(0, inplace=True)
#                     mac_dict[mac].reset_index(drop=True, inplace=True)
#                     P_COUNT = 0
#                 elif len(mac_dict[mac]) == window_size:
#                     mac_dict[mac].drop(0, inplace=True)
#                     mac_dict[mac].reset_index(drop=True, inplace=True)

#                 elif len(mac_dict[mac]) > window_size:
#                     print("Error: window_size exceeded for mac_dict")

#             except Exception as e:
#                 print('Error during data processing and prediction:', e)

#         except Exception as e:
#             print(f"Error in consume_messages loop: {str(e)}")
def consume_messages():
    global P_COUNT, message_count, predict_counter
    exclude_indices = [0, 1, 2, 3, 11, 25, 32, 39, 53, 61, 62, 63]
    valid_columns = [str(i) for i in range(64) if i not in exclude_indices]
    
    for message in consumer:
        try:
            buffer = message.value[:2048]
            try:
                csi_data = pickle.loads(buffer)
                
                # 데이터 전처리
                processed_data = preprocess_data(csi_data)
                
                # DataFrame 생성 - 52개 컬럼만 사용
                csi_df = pd.DataFrame([processed_data], columns=valid_columns)
                
                # P_COUNT 증가 및 DataFrame 누적
                P_COUNT += 1
                message_count += 1
                
                if mac_dict[mac].empty:
                    mac_dict[mac] = pd.DataFrame(columns=valid_columns)
                mac_dict[mac] = pd.concat([mac_dict[mac], csi_df], ignore_index=True)

                # window_size에 도달했고, P_COUNT가 조건을 만족할 때만 예측
                if len(mac_dict[mac]) == window_size and (P_COUNT == window_size or P_COUNT == window_size // 2):
                    # 모델 입력 준비
                    input_data = mac_dict[mac][valid_columns].values
                    input_data = torch.tensor(input_data, dtype=torch.float32).unsqueeze(0)
                    
                    # 예측 수행
                    with torch.no_grad():
                        outputs = model(input_data)
                        outputs = F.log_softmax(outputs, dim=1)
                        probabilities = F.softmax(outputs, dim=1)
                        predicted_class = torch.argmax(probabilities, dim=1)
                        
                        probs = probabilities[0].cpu().numpy() * 100
                        print("\nProbabilities for each activity:")
                        for activity, prob in zip(activities, probs):
                            print(f"{activity}: {prob:.2f}%")
                        
                        predict_counter += 1
                    
                    # 가장 오래된 데이터 제거 및 P_COUNT 초기화
                    mac_dict[mac].drop(0, inplace=True)
                    mac_dict[mac].reset_index(drop=True, inplace=True)
                    P_COUNT = 0
                
                # window_size에 도달했지만 P_COUNT 조건을 만족하지 않을 때
                elif len(mac_dict[mac]) == window_size:
                    mac_dict[mac].drop(0, inplace=True)
                    mac_dict[mac].reset_index(drop=True, inplace=True)
                
                # window_size를 초과한 경우
                elif len(mac_dict[mac]) > window_size:
                    print("Error: window_size exceeded for mac_dict")

            except Exception as e:
                print('Error during data processing and prediction:', e)
                print(f"Error details: {str(e)}")
                import traceback
                print(traceback.format_exc())

        except Exception as e:
            print(f"Error in consume_messages loop: {str(e)}")
# @app.on_event("startup")
# async def startup_event():
#     global model, consumer, config, window_size, columns, activities, mac_dict
#     print("Starting application...")
    
#     # Load configuration and initialize model
#     config = get_config('config.yaml')
#     window_size = config['application']['client']['window_size']
#     print("window size = ",window_size)
#     num_sub = config['subcarrier'][config['application']['client']["bandwidth"]]
#     activities = config['application']['client']["activity_labels"]
#     columns = ['_' + str(i) for i in range(num_sub)]
#     mac_dict = {}
#     mac_dict[mac] = pd.DataFrame(columns=columns)

#     # Load pretrained model
#     print('======> Load model')
#     model = ViT(
#         in_channels=config['application']['model']['ViT']["in_channels"],
#         patch_size=(config['application']['model']['ViT']["patch_size"], 
#                    config['subcarrier'][config['application']['client']["bandwidth"]]),
#         embed_dim=config['application']['model']['ViT']["embed_dim"],
#         num_layers=config['application']['model']['ViT']["num_layers"],
#         num_heads=config['application']['model']['ViT']["num_heads"],
#         mlp_dim=config['application']['model']['ViT']["mlp_dim"],
#         num_classes=len(config['application']['client']["activity_labels"]),
#         in_size=[window_size, config['subcarrier'][config['application']['client']["bandwidth"]]]
#     )
#     # model.load_state_dict(torch.load(config['application']['FSL']['save_model_path'], map_location=torch.device('cpu')))
#     state_dict = torch.load(config['application']['SVL']['save_model_path'], map_location=torch.device('cpu'))

#     # 키 이름에서 'encoder.' 제거
#     new_state_dict = {}
#     for k, v in state_dict.items():
#         new_key = k.replace("encoder.", "")  # 'encoder.' 제거
#         new_state_dict[new_key] = v

#     # 새로운 state_dict를 모델에 로드
#     model.load_state_dict(new_state_dict)
#     model.eval()
#     print('======> Success')
    
#     # Initialize Kafka Consumer
#     global consumer
#     consumer = KafkaConsumer(
#         'CSI3',
#         bootstrap_servers=['k11a202.p.ssafy.io:9092'],
#         group_id='my_group',
#         auto_offset_reset='latest',
#         enable_auto_commit=True
#     )
#     print("Consumer initialized successfully")
    
#     # Start message consumption thread
#     consumer_thread = threading.Thread(target=consume_messages)
#     consumer_thread.daemon = True
#     consumer_thread.start()
@app.on_event("startup")
async def startup_event():
    global model, consumer, config, window_size, columns, activities, mac_dict
    print("Starting application...")
    
    # Load configuration and initialize model
    config = get_config('config.yaml')
    window_size = config['application']['client']['window_size']
    print("Window size:", window_size)
    
    activities = config['application']['client']["activity_labels"]
    columns = [str(i) for i in range(num_sub)]
    mac_dict = {}
    mac_dict[mac] = pd.DataFrame(columns=columns)

    # Load pretrained BiLSTM model
    print('======> Load BiLSTM model')
    model = BiLSTMModel()
    model.load_state_dict(torch.load(config['application']['SVL']['save_model_path'], map_location=torch.device('cpu')))
    model.eval()
    print('======> Model loaded successfully')
    
    # Initialize Kafka Consumer
    global consumer
    consumer = KafkaConsumer(
        'CSI3',
        bootstrap_servers=['k11a202.p.ssafy.io:9092'],
        group_id='my_group',
        auto_offset_reset='latest',
        enable_auto_commit=True
    )
    print("Consumer initialized successfully")
    
    # Start message consumption thread
    consumer_thread = threading.Thread(target=consume_messages)
    consumer_thread.daemon = True
    consumer_thread.start()

@app.on_event("shutdown")
async def shutdown_event():
    # Calculate elapsed time and print message count and duration
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Application shutdown. Total messages received: {message_count}")
    print(f"Total time elapsed: {elapsed_time:.2f} seconds")

@app.get("/")
async def root():
    return {"message": "Server is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, BackgroundTasks
from kafka import KafkaConsumer
import asyncio
import json
import matplotlib.pyplot as plt
import numpy as np
import torch
import pandas as pd
import pickle
import torch.nn.functional as F
from os.path import exists
from dataloader.dataset import FSLDataset
from runner.utils import get_config, extract_test_sample
from model.vit import ViT
import runner.proto as proto
import logging
import uvicorn


app = FastAPI()

# Kafka consumer 설정
consumer = KafkaConsumer(
    'CSI3',
    bootstrap_servers=['k11a202.p.ssafy.io:9092'],
    group_id='my_group',
    auto_offset_reset='latest',
    enable_auto_commit=True
)

async def consume_messages():
    async def consume():
        for message in consumer:
            # 메시지 처리 로직 추가 (예: 메시지 출력)
            print(f"Received message: {message.value.decode('utf-8')}")
            await asyncio.sleep(0.1)  # 비동기 처리를 위한 짧은 대기시간 추가

    # Kafka 컨슈머를 별도의 스레드로 실행
    await asyncio.to_thread(consume)

@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 Kafka 메시지를 소비하는 작업 시작"""
    asyncio.create_task(consume_messages())


@app.get("/")
def root():
    """루트 엔드포인트"""
    return {
        "gdgd"
    }
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
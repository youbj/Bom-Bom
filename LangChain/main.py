
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
import logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title="노인 케어 대화 시스템",
    description="AI 기반 노인 케어 대화 및 분석 시스템",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    logger.info("애플리케이션 시작")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("애플리케이션 종료")
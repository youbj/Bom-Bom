import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
import logging
import uvicorn
import platform

logger = logging.getLogger(__name__)

# Windows에서 이벤트 루프 정책 설정
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

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
app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    logger.info("애플리케이션 시작")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("애플리케이션 종료")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
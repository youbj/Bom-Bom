
from fastapi import APIRouter
from app.api.endpoints import conversation, analysis, reports

api_router = APIRouter()

api_router.include_router(
    conversation.router,
    prefix="/conversations",
    tags=["conversations"]
)

api_router.include_router(
    analysis.router,
    prefix="/analysis",
    tags=["analysis"]
)

api_router.include_router(
    reports.router,
    prefix="/reports",
    tags=["reports"]
)
from fastapi.testclient import TestClient
import pytest
from unittest.mock import Mock, patch
from main import app  # 경로 수정
from app.models.schema import (
    EmotionalState, RiskLevel, HealthStatus,
    ConversationAnalysis, HealthMetrics
)
from app.services.conversation_manager import ConversationManager
from app.services.conversation_analyzer import ConversationAnalyzer
from app.services.gpt_service import GPTService

client = TestClient(app)

# 테스트 데이터
test_texts = [
    "오늘은 날씨가 좋아서 공원에서 산책했어요. 기분이 정말 좋았답니다.",
    "요즘 잠을 잘 못자고 불안한 생각이 자주 들어요.",
    "손주들이 와서 같이 점심도 먹고 이야기도 많이 했어요."
]

@pytest.fixture
def conversation_manager():
    return ConversationManager()

@pytest.fixture
def mock_gpt_response():
    return {
        "response_text": "네, 말씀해주셔서 감사합니다. 산책은 건강에 매우 좋은 활동이에요.",
        "analysis": {
            "emotional_state": "positive",
            "risk_level": "none",
            "keywords": ["산책", "날씨", "기분"],
            "actions_needed": []
        }
    }

# API 엔드포인트 테스트
def test_start_conversation():
    response = client.post("/api/conversation/start")
    assert response.status_code == 200
    assert "conversation_id" in response.json()

def test_process_text():
    # 대화 시작
    start_response = client.post("/api/conversation/start")
    conversation_id = start_response.json()["conversation_id"]
    
    # 텍스트 처리 테스트
    response = client.post(
        "/api/conversation/process",
        json={
            "text": test_texts[0],
            "conversation_id": conversation_id
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "text_response" in data
    assert "sentiment_analysis" in data
    assert "text_summary" in data
    assert "analysis" in data

# 단위 테스트
class TestConversationAnalyzer:
    def test_analyze_sentiment(self):
        analyzer = ConversationAnalyzer()
        
        # 긍정적인 텍스트 테스트
        positive_result = analyzer.analyze_sentiment(test_texts[0])
        assert positive_result["score"] > 0
        assert positive_result["is_positive"] is True
        
        # 부정적인 텍스트 테스트
        negative_result = analyzer.analyze_sentiment(test_texts[1])
        assert negative_result["score"] < 0
        assert negative_result["is_positive"] is False
    
    def test_summarize_text(self):
        analyzer = ConversationAnalyzer()
        original_text = "이것은 첫 번째 문장입니다. 이것은 두 번째 문장입니다. 이것은 세 번째 문장입니다."
        summary = analyzer.summarize_text(original_text)
        
        assert len(summary) < len(original_text)
        assert isinstance(summary, str)
        assert len(summary.strip()) > 0

class TestConversationManager:
    @pytest.mark.asyncio
    async def test_process_text_input(self, conversation_manager, mock_gpt_response):
        with patch('app.services.gpt_service.GPTService.generate_response') as mock_generate:
            mock_generate.return_value = mock_gpt_response
            
            response = await conversation_manager.process_text_input(test_texts[0])
            
            assert "text_response" in response
            assert "sentiment_analysis" in response
            assert "text_summary" in response
            assert "analysis" in response

# 통합 테스트
@pytest.mark.asyncio
async def test_full_conversation_flow():
    manager = ConversationManager()
    
    # 대화 시작
    conversation_id = manager.start_conversation()
    assert conversation_id is not None
    
    # 연속된 메시지 처리
    for text in test_texts:
        response = await manager.process_text_input(text)
        
        # 응답 검증
        assert "text_response" in response
        assert "sentiment_analysis" in response
        assert isinstance(response["sentiment_analysis"], dict)
        assert "score" in response["sentiment_analysis"]
        assert "text_summary" in response
        assert "analysis" in response

if __name__ == "__main__":
    pytest.main(["-v", "test_conversation.py"])
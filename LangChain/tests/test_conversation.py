import httpx
import pytest
from unittest.mock import Mock, patch
from main import app
from app.models.schema import (
    EmotionalState, RiskLevel, HealthStatus,
    ConversationAnalysis, HealthMetrics
)
from app.services.conversation_manager import ConversationManager
from app.services.conversation_analyzer import ConversationAnalyzer
from app.services.gpt_service import GPTService

# 기본 테스트 데이터
test_texts = [
    "오늘 날씨가 좋아서 산책하니 정말 행복했어요. 기분이 너무 좋네요!",
    "아주 잘났다 잘났어",
    "뒤질래? 나한테 말걸지마",
]

# Fixtures
@pytest.fixture
def conversation_manager():
    """ConversationManager 인스턴스를 생성하는 fixture"""
    manager = ConversationManager()
    yield manager
    # 테스트 후 정리 (cleanup)
    if manager.current_conversation_id:
        manager.end_conversation()

@pytest.fixture
async def async_client():
    """비동기 HTTP 클라이언트 fixture"""
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
def mock_analyzer_responses():
    """분석기 응답을 위한 mock 데이터"""
    return {
        test_texts[0]: {
            "sentiment": {
                "score": 85,
                "is_positive": True
            },
            "summary": "날씨가 좋아 산책하며 행복을 느낌"
        },
        test_texts[1]: {
            "sentiment": {
                "score": 45,
                "is_positive": False
            },
            "summary": "자신을 과시하는 발언"
        },
        test_texts[2]: {
            "sentiment": {
                "score": 15,
                "is_positive": False
            },
            "summary": "공격적인 발언과 거부감 표현"
        }
    }

@pytest.fixture
def mock_gpt_responses():
    """GPT 응답을 위한 mock 데이터"""
    return {
        test_texts[0]: {
            "response_text": "날씨 좋은 날 산책을 즐기셨다니 정말 좋으시겠어요. 산책은 기분 전환에도 좋고 건강에도 매우 좋죠. 평소에도 자주 산책을 하시나요?",
            "validation": {
                "적절성_점수": 5,
                "명확성_점수": 4,
                "공감도_점수": 5,
                "개선필요사항": []
            },
            "user_analysis": {
                "감정_상태": "긍정적",
                "감정_수치": 85.5,
                "위험_수준": "없음"
            },
            "conversation_analysis": {
                "감정_상태": "긍정적",
                "감정_수치": 85.5,
                "위험_수준": "없음",
                "주요_키워드": ["날씨", "산책", "행복", "기분"],
                "필요_조치사항": []
            }
        },
        test_texts[1]: {
            "response_text": "무언가 불편한 일이 있으신 것 같네요. 어떤 일이 있으셨나요?",
            "validation": {
                "적절성_점수": 4,
                "명확성_점수": 4,
                "공감도_점수": 4,
                "개선필요사항": []
            },
            "user_analysis": {
                "감정_상태": "부정적",
                "감정_수치": 45.0,
                "위험_수준": "낮음"
            },
            "conversation_analysis": {
                "감정_상태": "부정적",
                "감정_수치": 45.0,
                "위험_수준": "낮음",
                "주요_키워드": ["잘났다"],
                "필요_조치사항": ["공감적 경청", "상황 파악"]
            }
        },
        test_texts[2]: {
            "response_text": "많이 힘드신 것 같아 마음이 아프네요. 혹시 제가 도움을 드릴 수 있는 부분이 있을까요?",
            "validation": {
                "적절성_점수": 5,
                "명확성_점수": 4,
                "공감도_점수": 5,
                "개선필요사항": []
            },
            "user_analysis": {
                "감정_상태": "부정적",
                "감정_수치": 15.0,
                "위험_수준": "높음"
            },
            "conversation_analysis": {
                "감정_상태": "부정적",
                "감정_수치": 15.0,
                "위험_수준": "높음",
                "주요_키워드": ["뒤질래", "말걸지마"],
                "필요_조치사항": ["즉각적 개입", "전문가 상담 고려"]
            }
        }
    }

@pytest.fixture
def mock_db():
    """데이터베이스 mock fixture"""
    return Mock()

# 테스트 케이스들...
class TestConversationManager:
    @pytest.mark.asyncio
    async def test_process_text_input(self, conversation_manager, mock_gpt_responses, mock_analyzer_responses):
        """대화 처리 테스트"""
        with patch('app.services.gpt_service.GPTService.generate_response') as mock_gpt, \
             patch('app.services.conversation_analyzer.ConversationAnalyzer.analyze_sentiment') as mock_sentiment, \
             patch('app.services.conversation_analyzer.ConversationAnalyzer.summarize_text') as mock_summary:
            
            test_text = test_texts[0]
            mock_gpt.return_value = mock_gpt_responses[test_text]
            mock_sentiment.return_value = mock_analyzer_responses[test_text]["sentiment"]
            mock_summary.return_value = mock_analyzer_responses[test_text]["summary"]
            
            response = await conversation_manager.process_text_input(text=test_text)
            
            assert response["text_response"] == mock_gpt_responses[test_text]["response_text"]
            assert response["sentiment_analysis"] == mock_analyzer_responses[test_text]["sentiment"]
            assert response["text_summary"] == mock_analyzer_responses[test_text]["summary"]

@pytest.mark.asyncio
async def test_full_conversation_flow(conversation_manager, mock_gpt_responses, mock_analyzer_responses):
    """전체 대화 흐름 테스트"""
    with patch('app.services.gpt_service.GPTService.generate_response') as mock_gpt, \
         patch('app.services.conversation_analyzer.ConversationAnalyzer.analyze_sentiment') as mock_sentiment, \
         patch('app.services.conversation_analyzer.ConversationAnalyzer.summarize_text') as mock_summary:
        
        conversation_id = conversation_manager.start_conversation()
        assert conversation_id is not None
        
        for text in test_texts:
            print(f"\n테스트 입력: {text}")
            
            mock_gpt.return_value = mock_gpt_responses[text]
            mock_sentiment.return_value = mock_analyzer_responses[text]["sentiment"]
            mock_summary.return_value = mock_analyzer_responses[text]["summary"]
            
            response = await conversation_manager.process_text_input(text=text)
            
            print("\n=== 응답 데이터 ===")
            print(f"AI 응답: {response['text_response']}")
            print(f"감정 분석: {response['sentiment_analysis']}")
            print(f"텍스트 요약: {response['text_summary']}")
            
            assert response["text_response"] == mock_gpt_responses[text]["response_text"]
            assert response["sentiment_analysis"] == mock_analyzer_responses[text]["sentiment"]
            assert response["text_summary"] == mock_analyzer_responses[text]["summary"]

        conversation_manager.print_conversation_history()
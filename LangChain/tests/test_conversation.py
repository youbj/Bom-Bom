from test_recorder import AudioRecorder
from test_api import ConversationAPI
import logging

logger = logging.getLogger(__name__)

class ConversationTester:
    def __init__(self):
        self.recorder = AudioRecorder()
        self.api = ConversationAPI()
        self.conversation_history = []
    
    def record_and_process(self):
        """음성 녹음 및 처리"""
        try:
            # 음성 녹음
            audio_file = self.recorder.record()
            
            # 음성을 텍스트로 변환
            text = self.api.transcribe_audio(audio_file)
            if not text:
                return None
            
            logger.info(f"음성 인식 결과: {text}")
            
            # 응답 생성
            response = self.api.generate_response(text)
            if not response:
                return None
            
            # 대화 기록 저장
            conversation = {
                "input": text,
                "response": response,
                "audio_file": audio_file
            }
            self.conversation_history.append(conversation)
            
            return conversation
            
        except Exception as e:
            logger.error(f"대화 처리 중 오류 발생: {str(e)}")
            return None
    
    def get_conversation_history(self):
        """대화 기록 조회"""
        return self.conversation_history
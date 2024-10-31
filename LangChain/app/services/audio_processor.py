import speech_recognition as sr
from gtts import gTTS
import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class AudioProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # 필요한 디렉토리 생성
        self.ensure_directories()
    
    def ensure_directories(self):
        """필요한 디렉토리 생성"""
        dirs = ['data/audio/input', 'data/audio/output', 'uploads']
        for dir_path in dirs:
            os.makedirs(dir_path, exist_ok=True)
    
    async def speech_to_text(self, audio_path: str) -> Optional[str]:
        """음성을 텍스트로 변환"""
        try:
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"오디오 파일을 찾을 수 없습니다: {audio_path}")
                
            with sr.AudioFile(audio_path) as source:
                audio = self.recognizer.record(source)
                return self.recognizer.recognize_google(audio, language='ko-KR')
        except Exception as e:
            logger.error(f"STT 변환 실패: {str(e)}")
            return None
    
    async def text_to_speech(self, text: str, output_path: str) -> bool:
        """텍스트를 음성으로 변환"""
        try:
            # 출력 디렉토리 확인
            output_dir = os.path.dirname(output_path)
            os.makedirs(output_dir, exist_ok=True)
            
            tts = gTTS(text=text, lang='ko')
            tts.save(output_path)
            return True
        except Exception as e:
            logger.error(f"TTS 변환 실패: {str(e)}")
            return False
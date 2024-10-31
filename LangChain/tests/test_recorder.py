
import pyaudio
import wave
import datetime
import os
import logging

logger = logging.getLogger(__name__)

class AudioRecorder:
    def __init__(self, output_dir="recordings"):
        self.output_dir = output_dir
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def record(self):
        p = pyaudio.PyAudio()
        
        stream = p.open(format=self.format,
                       channels=self.channels,
                       rate=self.rate,
                       input=True,
                       frames_per_buffer=self.chunk)
        
        logger.info("녹음을 시작합니다. 종료하려면 Ctrl+C를 누르세요.")
        frames = []
        
        try:
            while True:
                data = stream.read(self.chunk)
                frames.append(data)
        except KeyboardInterrupt:
            logger.info("녹음을 종료합니다.")
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recording_{timestamp}.wav"
        filepath = os.path.join(self.output_dir, filename)
        
        wf = wave.open(filepath, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        return filepath
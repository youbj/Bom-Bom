#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import threading
import time
import requests
import json
from kafka import KafkaConsumer
import RPi.GPIO as GPIO
import gc

import MicrophoneStream as MS
import ex2_getVoice2Text as voice
import ex6_queryVoice as query

RATE = 16000
CHUNK = 512
BUTTON_PIN = 29
SCHEDULE_API_URL = "http://k11a202.p.ssafy.io:8080/api/v1/schedule/today?senior-id=1"
START_CONVERSATION_URL = "http://k11a202.p.ssafy.io:8000/api/conversation/start"
CHAT_API_URL = "http://k11a202.p.ssafy.io:8000/api/conversation/chat"
KAFKA_TOPIC = 'elderly_conversations'
KAFKA_SERVER = 'k11a202.p.ssafy.io:9092'

# 전역 변수
global_consumer = None
conversation_id = None


def create_kafka_consumer():
    """
    Kafka Consumer를 생성하여 전역 변수에 저장.
    """
    global global_consumer
    if global_consumer is None:
        global_consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=[KAFKA_SERVER],
            auto_offset_reset='latest',
            enable_auto_commit=True,
            group_id='elderly_conversation_group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        )
        print("Kafka Consumer 생성 완료")
    return global_consumer


from kafka import TopicPartition

# 전역 변수로 메시지 수를 관리
message_count = 0  # 메시지 수 초기화

def fetch_kafka_response(conversation_id):
    """
    Kafka에서 특정 conversation_id에 해당하는 메시지를 기다리는 함수.
    """
    global global_consumer
    global message_count  # 메시지 수 관리

    if global_consumer is None:
        create_kafka_consumer()

    print(f"Kafka 메시지 대기 중... (conversation_id: {conversation_id})")
    try:
        # message_count = 0  # 메시지 수 초기화

        for message in global_consumer:
            # 메시지 수를 체크
            message_count += 1
            print(f"현재 메시지 수: {message_count}")

            if message_count > 4:  # 5번 메시지를 수신하면 대기를 종료
                print("Kafka 메시지 대기 횟수를 초과했습니다.")
                message_count=0
                return ""

            kafka_data = message.value
            print(f"Kafka 수신 메시지: {kafka_data}")

            # 특정 conversation_id와 일치하는 메시지만 처리
            # Kafka 메시지의 conversation_id와 Python의 conversation_id를 문자열로 비교
            if str(kafka_data.get("conversation_id")) == str(conversation_id):
                response_text = kafka_data.get("response_text", "")
                print(f"Kafka 메시지 수신 성공 - response_text: {response_text}")
                return response_text

        print("Kafka 메시지를 찾을 수 없습니다.")
        return "Kafka에서 메시지를 찾을 수 없습니다."
    except Exception as e:
        print(f"Kafka 메시지 처리 중 오류 발생: {e}")
        return "Kafka 메시지를 처리하는 중 오류가 발생했습니다."
    finally:
        print("Kafka 메시지 대기 종료.")



def start_conversation():
    """
    대화를 시작하고 conversation_id를 반환합니다.
    """
    global conversation_id
    try:
        response = requests.post(START_CONVERSATION_URL, json={"text": "", "senior_id": "1"})
        if response.status_code == 200:
            conversation_id = response.json().get("conversation_id")
            if conversation_id:
                print(f"대화 시작 - conversation_id: {conversation_id}")
                return conversation_id
            else:
                print("conversation_id를 받을 수 없습니다.")
                return None
        else:
            print("대화 시작 요청 실패. 상태 코드:", response.status_code)
            return None
    except Exception as e:
        print(f"대화 시작 요청 중 오류 발생: {e}")
        return None


def call_custom_ai_api(user_query):
    """
    서버에 사용자의 질문을 보내고 Kafka에서 AI 응답을 받아옵니다.
    """
    global conversation_id

    # conversation_id가 없으면 대화 시작
    if not conversation_id:
        conversation_id = start_conversation()
        if not conversation_id:
            return "대화를 시작하는 데 실패했습니다."

    # AI 응답 요청
    try:
        response = requests.post(
            f"{CHAT_API_URL}?conversation_id={conversation_id}",
            json={"text": user_query, "senior_id": "1"}
        )
        if response.status_code == 200:
            print(f"AI 요청 성공 - conversation_id: {conversation_id}")
            return fetch_kafka_response(conversation_id)  # Kafka에서 응답 대기
        else:
            print("AI 응답 요청 실패. 상태 코드:", response.status_code)
            return "AI 응답을 가져오는 데 실패했습니다."
    except Exception as e:
        print(f"AI 응답 요청 중 오류 발생: {e}")
        return "AI 응답 요청 중 오류가 발생했습니다."



def fetch_schedule():
    """
    서버에서 일정 데이터를 가져옵니다.
    """
    try:
        response = requests.get(SCHEDULE_API_URL)
        if response.status_code == 200:
            schedules = response.json()
            return schedules
        else:
            print("서버에서 일정을 가져올 수 없습니다. 상태 코드:", response.status_code)
            return []
    except Exception as e:
        print(f"서버 요청 중 오류 발생: {e}")
        return []


def speak_schedule(schedules):
    """
    일정 데이터를 음성으로 변환하고 재생합니다.
    """
    if schedules:
        for schedule in schedules:
            time = schedule.get("time", "시간 정보 없음")
            memo = schedule.get("memo", "일정 정보 없음")
            template = f"{time}에 {memo}이 있습니다."
            print(f"생성된 음성 텍스트: {template}")
            try:
                query.tts.getText2VoiceStream(template, "schedule_message.wav")
                MS.play_file("schedule_message.wav")
            except Exception as e:
                print(f"TTS 변환 또는 재생 중 오류 발생: {e}")
    else:
        no_schedule_message = "일정이 없습니다."
        print(f"생성된 음성 텍스트: {no_schedule_message}")
        try:
            query.tts.getText2VoiceStream(no_schedule_message, "no_schedule_message.wav")
            MS.play_file("no_schedule_message.wav")
        except Exception as e:
            print(f"TTS 변환 또는 재생 중 오류 발생: {e}")


def handle_button_press(channel):
    """
    버튼이 눌렸을 때 실행되는 콜백 함수.
    """
    print("버튼이 눌렸습니다! 서버에서 일정 데이터를 가져옵니다...")
    schedules = fetch_schedule()
    speak_schedule(schedules)


def monitor_button():
    """
    버튼 상태를 모니터링하는 스레드 함수.
    """
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=handle_button_press, bouncetime=300)

    print("버튼 모니터링 시작...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("버튼 모니터링 종료...")
    finally:
        GPIO.cleanup()


def wait_for_keyword():
    """
    Waits for the keyword 'Jarvis' to be recognized.
    """
    print("\n\n자비스라고 말씀해주세요.\n")
    recognized_text = voice.getVoice2Text()
    return "자비스" in recognized_text


def handle_conversation():
    """
    Handles a conversation session with the user.
    """
    global conversation_id

    print("자비스가 인식되었습니다. 대화를 시작합니다.\n")
    # 대화 시작

    response_count = 0

    try:
        with MS.MicrophoneStream(RATE, CHUNK) as stream:
            if not conversation_id:
                conversation_id = start_conversation()
                if not conversation_id:
                    return "대화를 시작하는 데 실패했습니다."

                # 대화가 성공적으로 시작된 경우, 첫 Kafka 응답 처리 및 TTS 재생
                ai_response = fetch_kafka_response(conversation_id)
                if ai_response:
                    try:
                        # TTS 변환 및 재생
                        query.tts.getText2VoiceStream(ai_response, "response_message.wav")
                        MS.play_file("response_message.wav")
                    except Exception as e:
                        print(f"TTS 처리 중 오류 발생: {e}")
            while response_count < 4:
                print("질문을 기다리고 있습니다...")
                print(response_count)
                user_query = voice.getVoice2Text()
                if user_query:
                    print(f"질문 내용: {user_query}")
                    ai_response = call_custom_ai_api(user_query)
                    print(f"AI 응답: {ai_response}")
                    try:
                        query.tts.getText2VoiceStream(ai_response, "response_message.wav")
                        MS.play_file("response_message.wav")
                    except Exception as e:
                        print(f"TTS 재생 중 오류 발생: {e}")
                    finally:
                        # 메모리 정리
                        ai_response = None
                        gc.collect()
                    response_count += 1
                else:
                    print("질문 인식 실패. 다시 시도하세요.")
    except Exception as e:
        print(f"마이크 스트림 관리 중 오류 발생: {e}")
    finally:
        cleanup_conversation()




def cleanup_conversation():
    """
    Cleans up resources after conversation.
    """
    global conversation_id
    conversation_id = None


def main():
    """
    프로그램 시작 시 Kafka Consumer 초기화 및 주요 기능 실행.
    """
    create_kafka_consumer()  # Kafka Consumer 초기화
    button_thread = threading.Thread(target=monitor_button, daemon=True)
    button_thread.start()

    while True:
        try:
            if wait_for_keyword():
                handle_conversation()
            else:
                print("자비스가 인식되지 않았습니다. 다시 말씀해주세요.")
        except Exception as e:
            print(f"메인 루프에서 오류 발생: {e}")


if __name__ == '__main__':
    main()

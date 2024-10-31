
from test_conversation import ConversationTester
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    tester = ConversationTester()
    
    try:
        while True:
            print("\n==== 노인 케어 대화 시스템 테스트 ====")
            print("1. 음성 녹음 및 대화")
            print("2. 대화 기록 조회")
            print("3. 종료")
            
            choice = input("선택하세요: ")
            
            if choice == "1":
                result = tester.record_and_process()
                if result:
                    print("\n=== 대화 결과 ===")
                    print(f"사용자: {result['input']}")
                    print(f"시스템: {result['response']}")
                    
            elif choice == "2":
                history = tester.get_conversation_history()
                if history:
                    print("\n=== 대화 기록 ===")
                    for idx, conv in enumerate(history, 1):
                        print(f"\n대화 {idx}")
                        print(f"사용자: {conv['input']}")
                        print(f"시스템: {conv['response']}")
                else:
                    print("저장된 대화 기록이 없습니다.")
                    
            elif choice == "3":
                print("테스트를 종료합니다.")
                break
                
            else:
                print("잘못된 선택입니다.")
                
    except KeyboardInterrupt:
        print("\n프로그램이 중단되었습니다.")
    except Exception as e:
        logger.error(f"프로그램 실행 중 오류 발생: {str(e)}")

if __name__ == "__main__":
    main()
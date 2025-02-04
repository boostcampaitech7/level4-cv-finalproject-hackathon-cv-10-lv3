from Project.APIs.input_utils.clova_speech import ClovaSpeechClient
from APIs.input_utils.record import record_audio


def get_user_input():
    print("입력 형식을 알려주세요.")
    print("텍스트는 't', 음성은 'v'를 입력하세요.")
    input_type = input().strip().lower()

    input_message = None

    if input_type == "t":
        print("텍스트를 입력하세요:")
        input_message = input().strip()

    elif input_type == "v":
        audio_file = record_audio()
        print("음성 파일을 처리합니다...")
        stt_client = ClovaSpeechClient()
        vtt = stt_client.req_upload(file=audio_file, completion="sync")

        if vtt.status_code == 200:
            result = vtt.json()
            print(result)
            voice_input = result.get("text", "")
            print(f"입력된 오디오:\n{voice_input}")
            print("입력된 오디오가 맞나요? [y/n]")
            retry = input().strip().lower()

            if retry == "y":
                input_message = voice_input
            else:
                print("수정된 문장을 입력하세요.")
                input_message = input()

        else:
            print(f"STT 요청 실패: {vtt.status_code} - {vtt.text}")
            input_message = None
            
    else:
        print("잘못된 입력입니다.")

    return input_message


if __name__ == "__main__":
    user_input = get_user_input()
    while user_input == None:
        user_input = get_user_input()
    print(f"최종 입력: {user_input}")

import os
import json
import pygame
from APIs.UserInput import userInput
from APIs.ClovaVoice import naver_tts


def play_voice(voice_file):
    """
    음성 파일을 재생합니다.
    """
    pygame.mixer.init()
    pygame.mixer.music.load(voice_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # 재생 중이면 대기
        continue
    pygame.mixer.quit()


def dictation_mode(input_json='extracted.json', output_folder='saves/voices'):
    """
    유저가 문장을 선택하여 듣고, 입력 및 정답을 확인하는 Dictation 모드.

    Args:
        input_json (str): JSON 파일 경로 (변환할 문장 포함)
        output_folder (str): 음성 파일 저장 폴더
    """
    # JSON 파일 로드
    with open(input_json, 'r', encoding='utf-8') as f:
        sentences = json.load(f)

    # 문장 목록 출력
    print("\n--- Sentence List ---")
    for idx, sentence in enumerate(sentences, start=1):
        print(f"{idx}. {sentence}")
    print("----------------------")

    # 유저가 문장 선택
    while True:
        try:
            sentence_num = int(input("\n듣고 싶은 문장의 번호를 입력하세요 (종료하려면 0 입력): ").strip())
            if sentence_num == 0:
                print("Dictation 모드를 종료합니다.")
                break
            if not (1 <= sentence_num <= len(sentences)):
                print("유효한 번호를 입력하세요.")
                continue

            # 선택한 문장 정보
            selected_sentence = sentences[sentence_num - 1]
            print(f"\n선택한 문장: {selected_sentence}")

            # 음성 파일 경로 설정
            voice_file = os.path.join(output_folder, f"voice_{sentence_num}.mp3")
            if not os.path.exists(voice_file):
                print("해당 문장의 음성 파일이 존재하지 않습니다. 음성을 생성 중입니다...")
                naver_tts(input_json=input_json, output_folder=output_folder)
                if not os.path.exists(voice_file):
                    print("음성 파일 생성에 실패했습니다. 다시 시도하세요.")
                    continue

            # 음성 재생
            print("문장을 재생합니다...")
            play_voice(voice_file)

            # 유저 입력 받기
            print("\n문장에 대한 Dictation을 작성하세요.")
            user_input = userInput()

            # 결과 출력
            print("\n--- Result ---")
            print(f"Original Sentence: {selected_sentence}")
            print(f"Your Input: {user_input}")
            print("----------------")

            # 유저 선택에 따라 반복 진행
            print("Press [R] to replay the voice, [N] to select a new sentence, [Q] to quit.")
            user_choice = input("Your choice: ").strip().lower()
            if user_choice == 'r':
                print("Replaying the voice...")
                play_voice(voice_file)
            elif user_choice == 'q':
                print("Exiting dictation mode.")
                break
            elif user_choice == 'n':
                print("Returning to sentence selection...")
            else:
                print("Invalid input. Returning to sentence selection.")

        except ValueError:
            print("숫자를 입력하세요.")

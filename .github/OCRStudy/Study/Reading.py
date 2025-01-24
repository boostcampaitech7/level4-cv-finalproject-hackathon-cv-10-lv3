import json
import pygame
import os

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


def reading(timestamp, voice_folder='saves/voices'):
    translation_path = f'saves/save4_tunning{timestamp}.json'
    words_path = f'saves/save5_words{timestamp}.json'
    
    
    with open(translation_path, 'r', encoding='utf-8') as f:
        translation = json.load(f)

    with open(words_path, 'r', encoding='utf-8') as f:
        words = json.load(f)

    idx = 0
    length = len(translation)
    print(idx+1,"/", length,":", translation[idx]["original"])

    while True:
        print("이전 문장으로 이동[B] 듣기[L] 번역 보기[T] 단어장 확인[W] 다음 문장으로 이동[N] 학습 종료[Q]")

        user = input().strip().lower()
        if user=='l':
            voice_file = os.path.join(voice_folder, f"voice_{idx+1}.mp3")
            print("문장을 재생합니다...")
            play_voice(voice_file)
        elif user=='t':
            print(translation[idx]["translation"])
        elif user=='w':
            dictionary= words[idx]["words"]
            for dic in dictionary:
                print("word:", dic["word"])
                print("mean:", dic["mean"])
                print("example", dic["example"])
                print("translation:", dic["trans"])
                print()
        elif user=='n':
            if idx+1>=length:
                print("다음 문장이 없습니다.")
            else:
                idx+=1
                print(idx+1,"/", length,":",translation[idx]["original"])
        elif user=='b':
            if idx-1<0:
                print("이전 문장이 없습니다.")
            else:
                idx-=1
                print(idx+1,"/", length,":",translation[idx]["original"])
        elif user=='q':
            break
        else:
            print("잘못된 입력입니다.")
    print("읽기 학습을 종료합니다")
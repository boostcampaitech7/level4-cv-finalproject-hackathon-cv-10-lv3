from datetime import datetime
import math
from APIs.clova_OCR import OCR
from Project.APIs.clova_papago import Translate
from APIs.HCXtunning import hcx_tunning
from APIs.HCXwords import make_words
from Study.dictation import dictation_mode
from Project.APIs.clova_voice import naver_tts
from Study.reading import reading
from Study.writing import writing_mode


timestamp = str(math.floor(datetime.now().timestamp()))


# 1.문학/비문학 선택
print("문학일 경우 1, 비문학일 경우 2를 입력하세요.")
TextType = input().strip()

# 2.image 촬영/불러오기
ImagePath = "testimage/image5.jpg"

# 3.OCR
OCR(ImagePath, timestamp)

# 4.번역
Translate(timestamp)

# 5.번역 튜닝
if TextType == "1":
    hcx_tunning(timestamp)
elif TextType == "2":
    hcx_tunning(timestamp)

# 6.단어장 만들기
make_words(timestamp)

# 7. 음성 파일 생성 (필요 시)
naver_tts(
    input_json=f"saves/save2_extracted{timestamp}.json", output_folder="saves/voices"
)

# 8.학습선택
while True:
    print("학습 방법을 선택하세요.")
    print("읽기-R, 듣기-L, 쓰기-W, 종료-Q")
    StudyType = input().strip().lower()

    if StudyType == "r":
        reading(timestamp, voice_folder="saves/voices")
    elif StudyType == "l":
        # Dictation 모드 실행
        dictation_mode(
            input_json=f"saves/save2_extracted{timestamp}.json",
            output_folder="saves/voices",
        )
    elif StudyType == "w":
        writing_mode(timestamp)
    elif StudyType == "q":
        print("학습을 종료합니다.")
        break
    else:
        print("잘못된 입력입니다.")

# 📸 SnapEng 
## 일상의 순간이 영어 공부로 변하는 하루 한 장의 기적
> SnapEng은 영어 원서, 칼럼, 일상 속 사진을 활용하여 쉽고 재미있게 영어를 학습할 수 있도록 돕는 플랫폼입니다.
OCR 기술을 활용하여 사용자가 사진을 업로드하면 텍스트를 추출하고, AI가 문법 피드백과 학습 보조 기능을 제공하여 효과적인 영어 학습을 지원합니다.

## 📌 01 | 주요 기능
✅ OCR 기반 학습 Mode   
	- 사용자가 업로드한 이미지에서 영어 텍스트를 자동으로 감지하고 변환   
    - 사용자의 이미지를 바탕으로 영어 듣기/말하기/쓰기/읽기 종합적 학습   

✅ Chat Mode   
    - 원어민 친구와 자연스러운 대화를 하는 것처럼  연습이 가능한 챗봇 탑제   
	- 사용자의 영어 글을 분석하여 문법, 어휘, 표현 개선점을 제공   

✅ Diary Mode   
	- 하루 한 장, 사진 영어 일기를 작성하고 AI의 피드백을 제공   


✅ 익숙한 UI & 사용자 친화적 경험   
	- 웹에서 간편하게 사용할 수 있는 직관적인 인터페이스   

## 👀 02 | IA (Information Architecture)
![ia](https://github.com/user-attachments/assets/9606c1f0-a0a2-40cc-aa2f-b4745969cafb)



## 🛠️ 03 | 기술 아키텍쳐
|분류|구조도|
|------|---|
|OCR 학습|<img width="812" alt="image" src="https://github.com/user-attachments/assets/e6ea2014-98e9-4500-b744-2fc03b8729e9" />|
|일상 이미지 기반 학습|<img width="794" alt="image" src="https://github.com/user-attachments/assets/cdad4775-4364-497e-82bb-7ff0a883b9cf" />|


## 🚀 04 | 설치 및 실행 방법

1️⃣ 백엔드 서버 실행
➡️ Python 가상환경 설정 (선택 사항)
```
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows
```
➡️ 필요한 패키지 설치
```
pip install -r requirements.txt
```

2️⃣ Streamlit 웹 애플리케이션 실행
```
cd Project # Project root로 이동
streamlit run main_front.py
```

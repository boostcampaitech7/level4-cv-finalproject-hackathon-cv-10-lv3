import streamlit as st
import random
import os
from datetime import datetime
from PIL import Image

from streamlit_config import set_global_config  # 설정 파일에서 설정을 가져오기
from footer import footer

# 글로벌 설정 호출
set_global_config()

# 서비스 소개
st.title("📷 스내핑 (SnapEng)")
st.markdown("#### 🖼️ 일상의 순간이 나만의 영어 공부로 변하는 하루 한 장의 기적")
st.markdown("내 일상을, 내 관심사를 바탕으로 영어를 보다 가볍게 가까이서 배워보아요.")

st.divider()

# OCR 학습 & 이미지 학습 소개
st.markdown("### 📌 학습 방식 소개")
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔍 OCR 학습")
    st.markdown(
        "- **관심 있는 콘텐츠**(소설, 뉴스, 칼럼 등)를 직접 선택해 학습해봐요 📖\n"
        "- **텍스트 인식**을 통해 **읽기, 쓰기, 듣기, 말하기, 어휘 학습** 한 번에!☝🏻 \n"
        "- 영어 답안 작성은 글과 음성 두 가지 방식 모두 가능해요"
    )
    if st.button("🔍 OCR 학습 시작하기", use_container_width=True):
        st.switch_page("pages/OCR_front.py")  # OCR 학습 페이지로 이동

with col2:
    st.subheader("🖼️ 이미지 주제 학습")
    st.markdown(
        "- **직접 찍은 사진**으로 AI와 자유롭게 대화해봐요 💬\n"
        "- 오늘 있었던 일을 사진과 함께 기록할 수 있고, **AI가 피드백도 제공해요** 📝\n"
        "- 원어민 친구처럼 **일상 회화를 연습**하고 **꾸준한 학습 습관 형성까지** 🎙️"
    )
    if st.button("🖼️ 이미지 학습 시작하기", use_container_width=True):
        st.switch_page("pages/Image_front.py")  # 이미지 학습 페이지로 이동

st.divider()

# 🔥 오늘의 영어 명언 (랜덤 추천)
quotes = [
    ('"The secret of getting ahead is getting started." - Mark Twain', 
     "앞서 나가는 비결은 시작하는 것이다."),
    ('"Do what you can, with what you have, where you are." - Theodore Roosevelt', 
     "할 수 있는 일을, 가진 것으로, 있는 곳에서 시작하라."),
    ('"The best way to predict the future is to create it." - Peter Drucker', 
     "미래를 예측하는 가장 좋은 방법은 그것을 창조하는 것이다."),
    ('"Mistakes are proof that you are trying." - Jennifer Lim', 
     "실수는 당신이 노력하고 있다는 증거다."),
    ('"Don’t watch the clock; do what it does. Keep going." - Sam Levenson', 
     "시계를 보지 말고, 시계처럼 계속 나아가라."),
]

quote, translation = random.choice(quotes)

st.markdown("### 💡 오늘의 영어 명언")
st.info(f"{quote}\n\n📢 **해석\:** {translation}")

st.markdown("✅ 오늘의 목표: **이 문장을 소리 내어 3번 읽어보아요** 🗣️🔥")

st.divider()

# 오늘의 일기 (가장 최신 파일 불러오기)
today_date = datetime.today().strftime("%y년 %m월 %d일")  # 오늘 날짜 가져오기
st.markdown(f"### 📝 오늘의 일기, {today_date}")  # 날짜 포함
feedback_folder = "saves/feedbacks"
image_folder = "uploads"

# 가장 최신 timestamp 찾기
if os.path.exists(feedback_folder):
    feedback_files = sorted(os.listdir(feedback_folder), reverse=True)  # 최신 파일 기준 정렬
    if feedback_files:
        latest_timestamp = feedback_files[0].split(".")[0]  # 파일명에서 timestamp 추출
        feedback_path = os.path.join(feedback_folder, feedback_files[0])
        image_path = os.path.join(image_folder, f"image_{latest_timestamp}.jpg")

        # 일기 피드백 내용 읽기
        with open(feedback_path, "r", encoding="utf-8") as f:
            feedback_content = f.read()

        # "수정된 문장:" 이후의 텍스트만 추출
        if "수정된 문장:" in feedback_content:
            feedback_content = feedback_content.split("수정된 문장:")[1].split("설명:")[0].strip()  # 설명 부분 제거

        # 이미지 & 일기 피드백 표시
        col1, col2 = st.columns([1, 2])

        with col1:
            if os.path.exists(image_path):
                # 이미지 불러오기
                img = Image.open(image_path)
                width, height = img.size

                # 정사각형 크롭: 중심을 기준으로 자르기
                min_dim = min(width, height)
                box = ((width - min_dim) // 2, (height - min_dim) // 2, 
                    (width + min_dim) // 2, (height + min_dim) // 2)
                img_cropped = img.crop(box)  # 정사각형 크롭

                st.image(img_cropped, caption="📸 오늘의 순간", use_container_width=True)
            else:
                st.info("📷 오늘의 이미지를 찾을 수 없습니다.")

        with col2:
            st.markdown("**🍀 당신이 기록한 오늘 하루는요.**")
            st.markdown(
                f"""
                <div style="
                    background-color: #f0f8ff;
                    padding: 15px;
                    border-radius: 10px;
                    border-left: 5px solid #007BFF;
                ">
                    {feedback_content}
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("📌 아직 저장된 일기가 없습니다. 오늘의 순간을 기록해보세요!")
else:
    st.info("📌 아직 저장된 일기가 없습니다. 오늘의 순간을 기록해보세요!")

footer()  # footer 출력
import streamlit as st
import random

# 서비스 소개
st.title("📷 스내핑 (SnapEng)")
st.markdown("#### 📢 일상의 순간이 영어 공부로 변신하는 하루 한 장의 기적")
st.markdown("**🎯 키워드:** 영어 학습, 하루 한 장, 개인화된 학습 컨텐츠")

st.divider()

# OCR 학습 & 이미지 학습 소개
st.markdown("### 🧐 학습 방식 소개")
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔍 OCR 학습")
    st.markdown(
        "- **사용자가 관심 있는 콘텐츠**(소설, 뉴스, 칼럼 등)를 직접 선택해 학습 📖\n"
        "- OCR 기반 **텍스트 인식**을 통해 **읽기, 쓰기, 듣기, 말하기, 어휘 학습** 한 번에! ✍️👂🗣️\n"
        "- 영어 답안 작성은 텍스트/음성 두 가지 방식으로 가능 🎯"
    )
    if st.button("🔍 OCR 학습 시작하기", use_container_width=True):
        st.switch_page("pages/OCR_front.py")  # OCR 학습 페이지로 이동

with col2:
    st.subheader("🖼️ 이미지 주제 학습")
    st.markdown(
        "- **직접 찍은 사진**으로 AI와 자유로운 대화 🤖💬\n"
        "- 오늘 하루 있었던 일을 사진과 함께 기록하고 **AI가 피드백 제공** 📝\n"
        "- 원어민 친구처럼 **일상 회화를 연습**하고 **꾸준한 학습 습관 형성** 🎙️📔"
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
st.info(f"{quote}\n\n📢 **한국어 해석:** {translation}")

footer()  # footer 출력
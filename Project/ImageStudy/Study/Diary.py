import streamlit as st
import os
import time
from APIs.feedback import feedback, feedback_review

def diary(timestamp):
    st.title("📖 Diary Mode")
    
    # 학습을 새로 시작할 때 상태 초기화
    if "Diary_change_mode" in st.session_state and st.session_state.Diary_change_mode:
        st.session_state.Diary_change_mode = False
        st.session_state.Diary_is_finished = False
    
    # 상태 초기화
    if "Diary_change_mode" not in st.session_state:
        st.session_state.Diary_change_mode = False
    if "Diary_is_finished" not in st.session_state:
        st.session_state.Diary_is_finished = False
    
    if "current_step" in st.session_state:
        st.session_state.current_step = 4
        
    # 학습 종료 상태 처리
    if st.session_state.Diary_is_finished:
        review_text = feedback_review(timestamp)
        st.markdown(
                f"""
                <div style="
                    background-color: #f0f8ff;
                    padding: 15px;
                    border-radius: 10px;
                    border-left: 5px solid #007BFF;
                ">
                    <b>📘 Review</b><br>
                    {review_text}
                </div>
                """,
                unsafe_allow_html=True
            )
        st.success("🎉 학습이 종료되었습니다. 오늘도 수고하셨습니다!")
        return  # 학습이 완전히 종료되었으므로 더 이상 실행하지 않음
    
    st.write("오늘 하루를 영어로 기록해보세요! ✍️")

    # 영어 일기 확인 및 수정
    image_path = f"uploads/image_{timestamp}.jpg"
    diary_path = f'saves/diary/{timestamp}.txt'
    os.makedirs(os.path.dirname(diary_path), exist_ok=True)

    if os.path.exists(image_path):
        st.image(image_path, width=400)
    else:
        st.write("🥲 이미지 파일을 찾을 수 없습니다.")

    if os.path.exists(diary_path):
        with open(diary_path, "r", encoding="utf-8") as f:
            diary_text = f.read()
    else:
        diary_text = f"[{time.strftime('%Y-%m-%d')}]"

    # 사용자가 수정할 수 있도록 text_area 제공
    #edited_text = st.text_area("**📓 오늘의 일기**", diary_text, height=500)
    # CSS 로드
    # CSS 스타일 적용
    st.markdown(
        """
        <style>
        @font-face {
            font-family: 'GangwonEduSaeeum_OTFMediumA';
            src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_2201-2@1.0/GangwonEduSaeeum_OTFMediumA.woff') format('woff');
            font-weight: normal;
            font-style: normal;
        }
        div[data-testid="stTextArea"] textarea {
            background-color: #f9f5e6; 
            font-family: 'GangwonEduSaeeum_OTFMediumA'; 
            border: 2px solid #d1b7a1; 
            border-radius: 8px;
            padding: 15px; 
            font-size: 18px; 
            color: #5c4033; 
        }
        div[data-testid="stTextArea"] label {
            font-weight: bold;
            font-size: 25px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # 다이어리 텍스트 입력
    edited_text = st.text_area("**📓 오늘의 일기**", diary_text, height=350)



    # 저장 버튼
    if st.button("💾 저장하기", use_container_width=True):
        with open(diary_path, "w", encoding="utf-8") as f:
            f.write(edited_text)
        st.success("✅ 일기가 성공적으로 저장되었습니다!")

    # 피드백 버튼
    if st.button("🧑‍🏫 AI 튜터의 피드백 확인하기", use_container_width=True):
        if edited_text:
            request_text = edited_text.replace('\n', ' ')
            feedback_response = feedback(request_text, save=True, timestamp=timestamp)  # AI 피드백 생성
            st.markdown(
                f"""
                <div style="
                    background-color: #f0f8ff;
                    padding: 15px;
                    border-radius: 10px;
                    border-left: 5px solid #007BFF;
                ">
                    <b>📘 AI 피드백:</b><br>
                    {feedback_response}
                </div>
                <br>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning("일기를 입력해주세요!")

    # 종료 & 모드 변경 버튼
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🖼️ 학습 모드로 돌아가기", use_container_width=True):
            st.session_state.Diary_change_mode = True
            st.session_state.current_step = 2
            st.rerun()
    with col2:
        if st.button("❌ 학습 종료", use_container_width=True):
            st.session_state.Diary_is_finished = True
            st.rerun()

    # 메인 페이지로 돌아가는 버튼
    st.divider()
    if st.button("⬅️ 홈 화면으로 돌아가기", use_container_width=True):
        st.session_state.current_step = 1
        st.session_state.Diary_change_mode = False
        st.session_state.Diary_is_finished = False
        st.session_state.uploaded_image = None
        st.session_state.timestamp = None
        st.session_state.image_path = None
        st.switch_page("main_front.py")


# CSS 스타일 적용
def load_css():
    css = """
    <style>
        @import url('https://fonts.googleapis.com/css?family=Shadows+Into+Light+Two');
        body {
            color: #484448;
            font-size: 18px;
            font-family: 'Shadows Into Light Two', cursive;
            text-align: center;
        }
        .journal {
            width: 350px;
            min-height: 275px;
            padding: 20px;
            display: inline-block;
            text-align: left;
            background-image:
                linear-gradient(180deg, white 3rem, #F0A4A4 calc(3rem), #F0A4A4 calc(3rem + 2px), transparent 1px),
                repeating-linear-gradient(0deg, transparent, transparent 1.5rem, #DDD 1px, #DDD calc(1.5rem + 1px));
            box-shadow: 1px 1px 3px rgba(0,0,0,.25);
            border-radius: 10px;
        }
        .title {
            text-align: center;
            margin-bottom: 10px;
        }
        .stTextArea>div>textarea {
            background-color: #fff8e1;
            border: 2px solid #f4a261;
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
            font-family: 'Shadows Into Light Two', cursive;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
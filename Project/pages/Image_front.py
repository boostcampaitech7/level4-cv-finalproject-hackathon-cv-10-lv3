import streamlit as st
import math
import os
from datetime import datetime
from ImageStudy.Study.Chat import chat
from ImageStudy.Study.Diary import diary

# Step 상태 초기화
if "current_step" not in st.session_state:
    st.session_state.current_step = 1
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None
if "timestamp" not in st.session_state:
    st.session_state.timestamp = None
if "image_path" not in st.session_state:
    st.session_state.image_path = None
    
# Chat 상태 초기화 추가
if "Chat_change_mode" not in st.session_state:
    st.session_state.Chat_change_mode = False
if "Chat_is_finished" not in st.session_state:
    st.session_state.Chat_is_finished = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "retry" not in st.session_state:
    st.session_state.retry = False
if "chat_turns" not in st.session_state:
    st.session_state.chat_turns = 0  # 대화 횟수

# Diary 상태 초기화 추가
if "Diary_change_mode" not in st.session_state:
    st.session_state.Diary_change_mode = False
if "Diary_is_finished" not in st.session_state:
    st.session_state.Diary_is_finished = False
if "diary_entries" not in st.session_state:
    st.session_state.diary_entries = []  # 사용자의 일기 목록 저장
if "diary_feedback" not in st.session_state:
    st.session_state.diary_feedback = []  # AI 피드백 저장


def main():
    st.title("🖼️ Image Study")

    # Step 1: 이미지 업로드
    if st.session_state.current_step == 1:
        st.header("1. 학습할 이미지 업로드")
        uploaded_image = st.file_uploader("이미지를 업로드하세요.", type=["jpg", "jpeg", "png"])
        if uploaded_image:
            timestamp = str(math.floor(datetime.now().timestamp()))
            image_path = f"uploads/image_{timestamp}.jpg"
            
            # ✅ uploads 폴더가 없으면 생성
            os.makedirs("uploads", exist_ok=True)
            
            # 이미지 저장
            with open(image_path, "wb") as f:
                f.write(uploaded_image.getbuffer())
            
            st.session_state.uploaded_image = uploaded_image
            st.session_state.timestamp = timestamp
            st.session_state.image_path = image_path
            st.success(f"이미지가 업로드되었습니다: {image_path}")
        
        if st.session_state.uploaded_image and st.button("다음 단계"):
            st.session_state.current_step += 1

    # Step 2: 학습 모드 선택
    if st.session_state.current_step == 2:
        st.header("2. 학습 모드 선택")
        study_type = st.radio("학습 모드를 선택하세요.", ("Chat Mode", "Diary Mode"))
        if st.button("학습 시작"):
            if study_type == "Chat Mode":
                st.session_state.current_step = 3
                chat(st.session_state.timestamp)
            elif study_type == "Diary Mode":
                st.session_state.current_step = 4
                diary()

    elif st.session_state.current_step == 3:
        chat(st.session_state.timestamp)
    elif st.session_state.current_step == 4:
        diary()
    
if __name__ == "__main__":
    main()
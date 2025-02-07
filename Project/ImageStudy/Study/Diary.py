import streamlit as st
import time
from APIs.feedback import feedback_for_diary
from APIs.user_input import userInput

def diary():
    st.title("📖 Diary Mode")
    
    # ✅ 학습을 새로 시작할 때 상태 초기화
    if "Diary_change_mode" in st.session_state and st.session_state.Diary_change_mode:
        st.session_state.Diary_change_mode = False
        st.session_state.Diary_is_finished = False
    
    # ✅ 상태 초기화
    if "Diary_change_mode" not in st.session_state:
        st.session_state.Diary_change_mode = False
    if "Diary_is_finished" not in st.session_state:
        st.session_state.Diary_is_finished = False
    
    if "current_step" in st.session_state:
        st.session_state.current_step = 4
        
    # ✅ 학습 종료 상태 처리
    if st.session_state.Diary_is_finished:
        st.success("🎉 학습이 종료되었습니다. 오늘도 수고하셨습니다!")
        return  # 학습이 완전히 종료되었으므로 더 이상 실행하지 않음
    
    st.write("오늘 하루를 기록해보세요! AI가 피드백을 제공합니다. ✍️")

    # ✅ 사용자 입력 (음성 & 텍스트 가능)
    user_input = userInput()  # 음성 또는 텍스트 입력

    # ✅ 피드백 버튼
    if st.button("💬 피드백 받기", use_container_width=True):
        if user_input.strip():
            feedback = feedback_for_diary(user_input)  # AI 피드백 생성
            st.write("**📢 AI 피드백:**", feedback)
        else:
            st.warning("일기를 입력해주세요!")

    # ✅ 종료 & 모드 변경 버튼
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

    # ✅ 메인 페이지로 돌아가는 버튼
    st.divider()
    if st.button("⬅️ 홈 화면으로 돌아가기", use_container_width=True):
        st.session_state.current_step = 2
        st.session_state.Diary_change_mode = False
        st.session_state.Diary_is_finished = False
        st.switch_page("main_front.py")
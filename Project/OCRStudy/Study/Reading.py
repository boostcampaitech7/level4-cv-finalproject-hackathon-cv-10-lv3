import os
import json
import streamlit as st

def reading(timestamp, voice_folder='saves/voices'):
    translation_path = f'saves/save3_translation{timestamp}.json'
    words_path = f'saves/save5_words{timestamp}.json'

    # 데이터 로드
    with open(translation_path, 'r', encoding='utf-8') as f:
        translation = json.load(f)
    with open(words_path, 'r', encoding='utf-8') as f:
        words = json.load(f)
        
    # ✅ 학습을 새로 시작할 때 상태 초기화
    if "Reading_change_mode" in st.session_state and st.session_state.Reading_change_mode:
        st.session_state.Reading_change_mode = False
        st.session_state.pop("current_idx", None)  # 문장 인덱스 초기화
        st.session_state.current_idx = 0
        st.session_state.Reading_is_finished = False

    # 상태 초기화
    if "current_idx" not in st.session_state:
        st.session_state.current_idx = 0
    if "Reading_change_mode" not in st.session_state:
        st.session_state.Reading_change_mode = False
    if "Reading_is_finished" not in st.session_state:
        st.session_state.Reading_is_finished = False

    # ✅ 학습 종료 후 다시 Reading 모드를 선택하면 정상적으로 동작하도록 설정
    if "current_step" in st.session_state:
        st.session_state.current_step = 9  # 9로 설정하여 학습 모드 선택 화면이 다시 안 뜨도록 함

    # ✅ 학습 종료 상태 처리
    if st.session_state.Reading_is_finished:
        st.success("🎉 학습이 종료되었습니다. 오늘도 수고하셨습니다!")
        return  # 학습이 완전히 종료되었으므로 더 이상 실행하지 않음
            
    # ✅ 읽기 모드 UI
    st.title("Reading Mode")

    length = len(translation)
    current_sentence = translation[st.session_state.current_idx]["original"]

    # 문장 상태 출력
    st.subheader(f"{st.session_state.current_idx + 1} / {length}: {current_sentence}")

    # 버튼 클릭 이벤트 처리
    col1, col2, col3 = st.columns([1, 1, 1])

    # 이전 문장 버튼
    with col1:
        if st.button("⬅️ 이전 문장", use_container_width=True):
            if st.session_state.current_idx > 0:
                st.session_state.current_idx -= 1
                st.rerun()

    # 다음 문장 버튼
    with col2:
        if st.button("➡️ 다음 문장", use_container_width=True):
            if st.session_state.current_idx < length - 1:
                st.session_state.current_idx += 1
                st.rerun()

    # 문장 듣기 버튼
    with col3:
        if st.button("🔊 문장 듣기", use_container_width=True):
            voice_file = os.path.join(voice_folder, f"voice_{st.session_state.current_idx + 1}.mp3")
            if os.path.exists(voice_file):
                st.audio(voice_file)
            else:
                st.error("음성 파일이 없습니다.")

    # 번역 보기 버튼
    if st.button("🌍 번역 보기", use_container_width=True):
        st.write(translation[st.session_state.current_idx]["translation"])

    # 단어장 보기 버튼
    # OCR_front.py 단어장 생성 코드 아래 버튼에 옮기기 # 문장마다 단어장 생성하면 더 효율적? -> 일단 나중에 코드 구현해보기
    if st.button("📚 단어장 보기", use_container_width=True):
        dictionary = words[st.session_state.current_idx]["words"]
        for dic in dictionary:
            st.write(f"**Word:** {dic['word']}")
            st.write(f"**Mean:** {dic['mean']}")
            st.write(f"**Example:** {dic['example']}")
            st.write(f"**Translation:** {dic['trans']}")
            st.write("---")

    if st.button("🕵️ 학습 모드로 돌아가기", use_container_width=True):
        st.session_state.Reading_change_mode = True  
        st.session_state.current_step = 8  # 학습 모드 선택 화면으로 변경
        st.rerun()
    
    if st.button("❌ 학습 종료", use_container_width=True):
        st.session_state.Reading_is_finished = True
        st.rerun()  # 화면 즉시 갱신
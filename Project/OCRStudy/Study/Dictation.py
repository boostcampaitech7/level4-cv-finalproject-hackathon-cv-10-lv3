import os
import json
import streamlit as st
from APIs.clova_voice import naver_tts
from APIs.user_input import userInput

def dictation_mode(timestamp, voice_folder='saves/voices'):
    input_json = f'saves/save2_extracted{timestamp}.json'
    translation_path = f'saves/save3_translation{timestamp}.json'
    voice_folder='saves/voices'
    st.title("Dictation Mode")
    
    # JSON 파일 로드
    with open(input_json, 'r', encoding='utf-8') as f:
        sentences = json.load(f)

    # 번역본/harmful score 로드
    with open(translation_path, 'r', encoding='utf-8') as f:
        translation = json.load(f)

    # ✅ 학습을 새로 시작할 때 상태 초기화
    if "Dictation_change_mode" in st.session_state and st.session_state.Dictation_change_mode:
        st.session_state.Dictation_selected_sentence_idx = None
        st.session_state.Dictation_change_mode = False
        st.session_state.Dictation_is_finished = False
        
    # 상태 초기화
    if "Dictation_selected_sentence_idx" not in st.session_state:
        st.session_state.Dictation_selected_sentence_idx = None
    if "Dictation_change_mode" not in st.session_state:
        st.session_state.Dictation_change_mode = False  
    if "Dictation_is_finished" not in st.session_state:
        st.session_state.Dictation_is_finished = False
    
    if "current_step" in st.session_state:
        st.session_state.current_step = 5  # 학습 모드 선택 화면이 다시 안 뜨도록 함
    
    # ✅ 학습 종료 상태 처리
    if st.session_state.Dictation_is_finished:
        st.success("🎉 학습이 종료되었습니다. 오늘도 수고하셨습니다!")
        return  # 학습이 완전히 종료되었으므로 더 이상 실행하지 않음


    # ✅ 문장 선택이 아직 안 되었으면 리스트 출력
    if st.session_state.Dictation_selected_sentence_idx is None:
        sentence_list = [f"{idx+1}. {sentence}" for idx, sentence in enumerate(sentences)]
        
        # Markdown으로 출력
        st.markdown("### 문장 목록:")
        st.markdown("\n".join(sentence_list))
        
        selected_idx = st.selectbox("듣고 싶은 문장을 선택하세요:", options=range(len(sentence_list)), format_func=lambda x: sentence_list[x])
        
        if st.button("문장 선택"):
            st.session_state.Dictation_selected_sentence_idx = selected_idx
            st.success("✅ 문장 선택 완료! 잠시 후 음성이 재생됩니다.")
            st.rerun()  # UI 갱신

    # ✅ 문장이 선택된 경우, 리스트를 숨기고 음성 출력 + 받아쓰기 진행
    else:
        selected_sentence = sentences[st.session_state.Dictation_selected_sentence_idx]
        
        # 음성 재생
        voice_file = os.path.join(voice_folder, f"voice_{st.session_state.Dictation_selected_sentence_idx + 1}.mp3")
        if not os.path.exists(voice_file):
            naver_tts(input_json=input_json, output_folder=voice_folder)
        
        if os.path.exists(voice_file):
            st.audio(voice_file, format="audio/mp3")
        else:
            st.error("음성 파일 생성에 실패했습니다.")
        
        # 유해성 경고 문구
        harmful_score  = translation[st.session_state.Dictation_selected_sentence_idx]["harmful_score"]
        if harmful_score<=4:
            st.error("⚠️ 학습에 부적절한 내용을 포함하고 있습니다.") 
        
        # 사용자 입력
        st.markdown("### 문장에 대해 Dictation을 작성하세요.")
        user_input_text = userInput()
        
        if user_input_text:
            st.write("**Original Sentence:**", selected_sentence)
            st.write("**Your Input:**", user_input_text)
            # 번역 보기 버튼
            if st.button("🌍 번역 보기"):
                st.write(translation[st.session_state.Dictation_selected_sentence_idx]["translation"])


        # 버튼 기반 작업
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 새로운 문장 선택", use_container_width=True):
                st.session_state.Dictation_selected_sentence_idx = None
                st.rerun()
        with col2:
            if st.button("🕵️ 학습 모드로 돌아가기", use_container_width=True):
                st.session_state.Dictation_change_mode = True  
                st.session_state.current_step = 3  # 학습 모드 선택 화면으로 변경
                st.rerun()
        with col3:
            if st.button("❌ 학습 종료", use_container_width=True):
                st.session_state.Dictation_is_finished = True
                st.rerun()

        # 📌 메인 페이지로 돌아가는 버튼 추가
        st.divider()
        if st.button("⬅️ 홈 화면으로 돌아가기", use_container_width=True):
            st.session_state.current_step = 3  # OCR 학습 모드 선택 화면으로 가게 함
            st.session_state.Dictation_selected_sentence_idx = None
            st.session_state.Dictation_change_mode = False
            st.session_state.Dictation_is_finished = False
            
            st.switch_page("main_front.py")  # 메인 페이지로 이동
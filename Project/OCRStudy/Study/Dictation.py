import os
import json
import random
import streamlit as st
from APIs.clova_voice import naver_tts
from APIs.user_input import userInput
from APIs.easy_mode import easymode

def dictation_mode(timestamp, voice_folder='saves/voices'):
    input_json = f'saves/save2_extracted{timestamp}.json'
    translation_path = f'saves/save3_translation{timestamp}.json'
    easy_json = f"saves/save4_easy{timestamp}.json"
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
        st.session_state.Easy_Hard = "Hard"
        
    # 상태 초기화
    if "Dictation_selected_sentence_idx" not in st.session_state:
        st.session_state.Dictation_selected_sentence_idx = None
    if "Dictation_change_mode" not in st.session_state:
        st.session_state.Dictation_change_mode = False  
    if "Dictation_is_finished" not in st.session_state:
        st.session_state.Dictation_is_finished = False
    if "Easy_Hard" not in st.session_state:
        st.session_state.Easy_Hard = "Hard"

    if "current_step" in st.session_state:
        st.session_state.current_step = 5  # 학습 모드 선택 화면이 다시 안 뜨도록 함
    
    # ✅ 학습 종료 상태 처리
    if st.session_state.Dictation_is_finished:
        st.success("🎉 학습이 종료되었습니다. 오늘도 수고하셨습니다!")
        return  # 학습이 완전히 종료되었으므로 더 이상 실행하지 않음


    # ✅ 문장 선택이 아직 안 되었으면 리스트 출력
    if st.session_state.Dictation_selected_sentence_idx is None:
        sentence_list = [f"{idx+1}. {sentence}" for idx, sentence in enumerate(sentences)]
        
        # 이지모드/하드모드 선택
        st.markdown("### 현재 난이도:")
        if st.session_state.Easy_Hard == "Easy":
            st.markdown("### EASY")
        elif st.session_state.Easy_Hard == "Nomal":
            st.markdown("### Nomal")
        else:
            st.markdown("### HARD")
        col1, col2, col3= st.columns(3)
        with col1:
            if st.button("EASY 모드로 실행"):
                st.session_state.Easy_Hard = "Easy"
                st.rerun()
        with col2:
            if st.button("NOMAL 모드로 실행"):
                st.session_state.Easy_Hard = "Nomal"
                st.rerun()
        with col3:
            if st.button("HARD 모드로 실행"):
                st.session_state.Easy_Hard = "Hard"
                st.rerun()
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
        selected_idx=st.session_state.Dictation_selected_sentence_idx
        # 음성 재생
        voice_file = os.path.join(voice_folder, f"voice_{selected_idx + 1}.mp3")
        if not os.path.exists(voice_file):
            naver_tts(input_json=input_json, output_folder=voice_folder)
        
        if os.path.exists(voice_file):
            st.audio(voice_file, format="audio/mp3")
        else:
            st.error("음성 파일 생성에 실패했습니다.")
        
        # 유해성 경고 문구
        harmful_score  = translation[selected_idx]["harmful_score"]
        if harmful_score<=4:
            st.error("⚠️ 학습에 부적절한 내용을 포함하고 있습니다.") 
        
        # 사용자 입력
        st.markdown("### 문장에 대해 Dictation을 작성하세요.")
        if st.session_state.Easy_Hard=="Easy":
            if os.path.exists(easy_json):
                with open(easy_json, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if str(selected_idx) in data:
                        hint=data[str(selected_idx)]
                    else:
                        hint=easymode(selected_sentence)
            else:
                hint=easymode(selected_sentence)
                data={}
            #힌트 출력
            st.write(hint)
            st.markdown("📌 빈칸을 채워봅시다.")

            # 새 데이터를 리스트에 추가
            data[str(selected_idx)]=hint

            # JSON 파일에 저장
            with open(easy_json, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

        elif st.session_state.Easy_Hard=="Nomal":
            words = selected_sentence.split()
            random.shuffle(words)
            st.write(f"**{', '.join(words)}**")
            st.markdown("📌 순서를 맞춰봅시다.")
        user_input_text = userInput()
        col1 = st.columns(1)[0]
        with col1:
            if st.button("Send"):
                st.write("**Original Sentence:**", selected_sentence)
                st.write("**Your Input:**", user_input_text)
                st.write("**Translated Sentence:**", translation[selected_idx]["translation"])


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
            st.session_state.current_step = 1  # OCR 첨부터 해야함.
            st.session_state.Dictation_selected_sentence_idx = None
            st.session_state.Dictation_change_mode = False
            st.session_state.Dictation_is_finished = False
            st.session_state.uploaded_image = None
            st.session_state.timestamp = None
            st.session_state.image_path = None
            st.session_state.uploaded_image_path = None  # 이미지 경로 초기화
            st.session_state.rotation_angle = 0  # 회전 각도 (초기값 0)
            st.session_state.flip_horizontal = False
            st.switch_page("main_front.py")  # 메인 페이지로 이동
import os
import json
import streamlit as st
from APIs.feedback import feedback
from APIs.user_input import userInput

def writing_mode(timestamp):
    input_json = f"saves/save2_extracted{timestamp}.json"
    output_json = f"saves/save3_translation{timestamp}.json"

    st.title("Writing Mode")
    
    # ✅ 학습을 새로 시작할 때 상태 초기화
    if "Writing_change_mode" in st.session_state and st.session_state.Writing_change_mode:
        st.session_state.Writing_selected_sentence_idx = None
        st.session_state.Writing_change_mode = False
        st.session_state.Writing_is_finished = False
    
    # 상태 초기화
    if "Writing_selected_sentence_idx" not in st.session_state:
        st.session_state.Writing_selected_sentence_idx = None
    if "Writing_change_mode" not in st.session_state:
        st.session_state.Writing_change_mode = False  
    if "Writing_is_finished" not in st.session_state:
        st.session_state.Writing_is_finished = False
        
    if "current_step" in st.session_state:
        st.session_state.current_step = 6
    
    # ✅ 학습 종료 상태 처리
    if st.session_state.Writing_is_finished:
        st.success("🎉 학습이 종료되었습니다. 오늘도 수고하셨습니다!")
        return  # 학습이 완전히 종료되었으므로 더 이상 실행하지 않음

    # 번역된 문장 목록 로드
    if not os.path.exists(output_json):
        st.error(f"{output_json} 파일이 존재하지 않습니다.")
        return

    with open(output_json, "r", encoding="utf-8") as f:
        translations = json.load(f)
    
    # ✅ 문장 선택이 아직 안 되었으면 리스트 출력
    if st.session_state.Writing_selected_sentence_idx is None:
        sentence_list = [f"{idx+1}. {item['translation']}" for idx, item in enumerate(translations)]
        
        # Markdown으로 출력
        st.markdown("### 문장 목록:")
        st.markdown("\n".join(sentence_list))
        
        selected_idx = st.selectbox("원하는 문장을 선택하세요:", options=range(len(sentence_list)), format_func=lambda x: sentence_list[x])

        if st.button("문장 선택"):
            st.session_state.Writing_selected_sentence_idx = selected_idx
            st.success("✅ 문장 선택 완료! 잠시 후 입력 창이 나타납니다.")
            st.rerun()  # UI 갱신

    # ✅ 문장이 선택된 경우, 리스트를 숨기고 사용자 입력 진행
    else:
        selected_translation = translations[st.session_state.Writing_selected_sentence_idx]
        st.markdown(f"##### 선택된 문장: {selected_translation['translation']}")

        # 유해성 경고 문구
        harmful_score  = translations[st.session_state.Writing_selected_sentence_idx]["harmful_score"]
        if harmful_score<=4:
            st.error("⚠️ 학습에 부적절한 내용을 포함하고 있습니다.") 
            
        st.write("📌 선택된 문장에 대해 영어로 답변을 작성하세요.")
        user_answer = userInput()
        
        # ✅ 사용자의 답변을 입력한 후 원문 영어 문장을 보여줌
        if user_answer:
            st.write("**Your Answer:**", user_answer)

            # 원문 영어 문장 출력
            if os.path.exists(input_json):
                with open(input_json, "r", encoding="utf-8") as f:
                    original_sentences = json.load(f)

                if st.session_state.Writing_selected_sentence_idx < len(original_sentences):
                    original_sentence = original_sentences[st.session_state.Writing_selected_sentence_idx]
                    st.write(f"**Original Sentence:** {original_sentence}")
                else:
                    st.error("원문 영어 문장을 찾을 수 없습니다.")
            else:
                st.error(f"\n'{input_json}' 파일이 존재하지 않습니다.")

        # ✅ 피드백 버튼
        # 피드백도 saves 폴더에 feedback으로 저장해둬서 feedback 누를 때마다 바뀌지 않도록 수정 # 비즈니스 관점으로 볼 때 request를 한 번만 보내는게 좋음 속도측면으로도
        if st.button("💬 피드백 받기", use_container_width=True):
            feedback_message = feedback(user_answer)
            st.write("**Feedback:**", feedback_message)
        
        # 버튼 기반 작업
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 새로운 문장 선택", use_container_width=True):
                st.session_state.Writing_selected_sentence_idx = None
                st.rerun()
        with col2:
            if st.button("🕵️ 학습 모드로 돌아가기", use_container_width=True):
                st.session_state.Writing_change_mode = True  
                st.session_state.current_step = 3  # 학습 모드 선택 화면으로 변경
                st.rerun()
        with col3:
            if st.button("❌ 학습 종료", use_container_width=True):
                st.session_state.Writing_is_finished = True
                st.rerun()
                
        # 📌 메인 페이지로 돌아가는 버튼 추가
        st.divider()
        if st.button("⬅️ 홈 화면으로 돌아가기", use_container_width=True):
            st.session_state.current_step = 1  # OCR 학습 모드 선택 화면으로 가게 함
            st.session_state.Writing_selected_sentence_idx = None
            st.session_state.Writing_change_mode = False
            st.session_state.Writing_is_finished = False
            st.session_state.uploaded_image = None
            st.session_state.timestamp = None
            st.session_state.image_path = None
            st.session_state.uploaded_image_path = None  # 이미지 경로 초기화
            st.session_state.rotation_angle = 0  # 회전 각도 (초기값 0)
            st.session_state.flip_horizontal = False  
            st.switch_page("main_front.py")  # 메인 페이지로 이동
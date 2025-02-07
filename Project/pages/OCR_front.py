import streamlit as st
from datetime import datetime
import math
from APIs.clova_OCR import OCR
from APIs.clova_papago import translate
from APIs.HCXtunning import hcx_tunning
from APIs.HCXwords import make_words
from APIs.clova_voice import naver_tts
from OCRStudy.Study.Dictation import dictation_mode
from OCRStudy.Study.Reading import reading
from OCRStudy.Study.Writing import writing_mode
from footer import footer
from streamlit_config import set_global_config  # 설정 파일에서 설정을 가져오기

# 글로벌 설정 호출
set_global_config()

# Step 상태 초기화
if "current_step" not in st.session_state:
    st.session_state.current_step = 1
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None
if "timestamp" not in st.session_state:
    st.session_state.timestamp = None
if "image_path" not in st.session_state:  # image_path도 상태로 관리
    st.session_state.image_path = None
    
# Reading 상태 초기화 추가
if "current_idx" not in st.session_state:
    st.session_state.current_idx = 0
if "Reading_change_mode" not in st.session_state:
    st.session_state.Reading_change_mode = False
if "Reading_is_finished" not in st.session_state:
    st.session_state.Reading_is_finished = False

# Dictation 상태 초기화 추가
if "Dictation_selected_sentence_idx" not in st.session_state:
    st.session_state.Dictation_selected_sentence_idx = None
if "Dictation_change_mode" not in st.session_state:
    st.session_state.Dictation_change_mode = False
if "Dictation_is_finished" not in st.session_state:
    st.session_state.Dictation_is_finished = False
    
# Writing 상태 초기화 추가
if "Writing_selected_sentence_idx" not in st.session_state:
    st.session_state.Writing_selected_sentence_idx = None
if "Writing_change_mode" not in st.session_state:
    st.session_state.Writing_change_mode = False
if "Writing_is_finished" not in st.session_state:
    st.session_state.Writing_is_finished = False

def main():
    st.title("🕵️ OCR 기반 영어 학습 도구")

    # Step 1: 문학/비문학 선택
    if st.session_state.current_step == 1:
        st.header("1. 학습 유형 선택")
        text_type = st.radio("문학 또는 비문학을 선택하세요.", ("문학", "비문학"))
        st.session_state.text_type_code = '1' if text_type == "문학" else '2'
        if st.button("다음 단계"):
            st.session_state.current_step += 1

    # Step 2: 이미지 업로드
    if st.session_state.current_step == 2:
        st.header("2. 학습할 이미지 업로드")
        uploaded_image = st.file_uploader("이미지를 업로드하세요.", type=["jpg", "jpeg", "png"])
        if uploaded_image:
            timestamp = str(math.floor(datetime.now().timestamp()))
            image_path = f"uploads/image_{timestamp}.jpg"
            
            # 이미지 저장
            with open(image_path, "wb") as f:
                f.write(uploaded_image.getbuffer())
            
            st.session_state.uploaded_image = uploaded_image
            st.session_state.timestamp = timestamp
            st.session_state.image_path = image_path  # image_path를 상태에 저장
            st.success(f"이미지가 업로드되었습니다: {image_path}")
        
        if st.session_state.uploaded_image and st.button("다음 단계"):
            st.session_state.current_step += 1

    # Step 3~7: OCR 처리 및 음성 파일 생성
    if st.session_state.current_step in [3, 4, 5, 6, 7]:
        if st.session_state.current_step == 3:
            st.header("3. OCR 처리")
            with st.spinner("OCR을 수행 중입니다..."):
                OCR(st.session_state.image_path, st.session_state.timestamp)  # image_path 사용
            st.success("OCR 처리가 완료되었습니다!")
            st.session_state.current_step += 1

        if st.session_state.current_step == 4:
            st.header("4. 번역")
            with st.spinner("텍스트 번역 중..."):
                Translate(st.session_state.timestamp)
            st.success("번역이 완료되었습니다!")
            st.session_state.current_step += 1

        if st.session_state.current_step == 5:
            st.header("5. 번역 튜닝")
            with st.spinner("번역 튜닝 중..."):
                hcx_tunning(st.session_state.timestamp)
            st.success("번역 튜닝이 완료되었습니다!")
            st.session_state.current_step += 1

        if st.session_state.current_step == 6:
            st.header("6. 단어장 생성")
            with st.spinner("단어장을 생성 중입니다..."):
                make_words(st.session_state.timestamp)
            st.success("단어장이 생성되었습니다!")
            st.session_state.current_step += 1

        if st.session_state.current_step == 7:
            st.header("7. 음성 파일 생성")
            with st.spinner("음성 파일을 생성 중입니다..."):
                naver_tts(input_json=f'saves/save2_extracted{st.session_state.timestamp}.json', output_folder='saves/voices')
            st.success("음성 파일 생성이 완료되었습니다!")
            st.session_state.current_step += 1

    # Step 8: 학습 모드 선택
    if st.session_state.current_step == 8:
        st.header("8. 학습 모드 선택")
        study_mode = st.radio("학습 모드를 선택하세요.", ("읽기 (Reading)", "듣기 (Dictation)", "쓰기 (Writing)"))
        if st.button("학습 시작"):
            if study_mode == "읽기 (Reading)":
                st.session_state.current_step = 9  # Reading 모드로 들어가면 9로 변경
                reading(st.session_state.timestamp, voice_folder='saves/voices')
            elif study_mode == "듣기 (Dictation)":
                st.session_state.current_step = 10  # Dictation 모드로 들어가면 10으로 변경
                dictation_mode(input_json=f'saves/save2_extracted{st.session_state.timestamp}.json', output_folder='saves/voices')
            elif study_mode == "쓰기 (Writing)":
                st.session_state.current_step = 11  # Writing 모드로 들어가면 11로 변경
                writing_mode(st.session_state.timestamp)
                
    elif st.session_state.current_step == 9:
        reading(st.session_state.timestamp, voice_folder='saves/voices')  # 학습 중에는 계속 reading 유지
    elif st.session_state.current_step == 10:
        dictation_mode(input_json=f'saves/save2_extracted{st.session_state.timestamp}.json', output_folder='saves/voices')
    elif st.session_state.current_step == 11:
        writing_mode(st.session_state.timestamp)
        
if __name__ == "__main__":
    main()


footer()
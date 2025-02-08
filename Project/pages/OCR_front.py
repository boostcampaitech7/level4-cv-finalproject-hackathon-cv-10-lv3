import streamlit as st
from datetime import datetime
from PIL import Image, ImageOps
import math
import time
from APIs.clova_OCR import OCR
from APIs.translation import translation
from APIs.clova_voice import naver_tts
from APIs.rotate import ProcessFile
from APIs.harmful import harmful
from OCRStudy.Study.Dictation import dictation_mode
from OCRStudy.Study.Reading import reading
from OCRStudy.Study.Writing import writing_mode
import os

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

    # Step 1: 이미지 업로드
    if "current_step" not in st.session_state:
        st.session_state.current_step = 1  # 초기값 설정
    if "uploaded_image_path" not in st.session_state:
        st.session_state.uploaded_image_path = None  # 이미지 경로 초기화
    if "rotation_angle" not in st.session_state:
        st.session_state.rotation_angle = 0  # 회전 각도 (초기값 0)
    if "flip_horizontal" not in st.session_state:
        st.session_state.flip_horizontal = False  # 좌우 반전 여부
    if "flip_vertical" not in st.session_state:
        st.session_state.flip_vertical = False  # 상하 반전 여부

    if st.session_state.current_step == 1:
        st.header("1. 학습할 이미지 업로드")
        uploaded_image = st.file_uploader("이미지를 업로드하세요.", type=["jpg", "jpeg", "png"])
        if uploaded_image:
            timestamp = str(math.floor(datetime.now().timestamp()))

            # 저장할 폴더 경로 설정
            upload_folder = "uploads"
            os.makedirs(upload_folder, exist_ok=True)  # 폴더가 없으면 생성

            image_path = os.path.join(upload_folder, f"image_{timestamp}.jpg")
            
            # 이미지 임시 저장
            with open(image_path, "wb") as f:
                f.write(uploaded_image.getbuffer())
            st.session_state.uploaded_image_path = image_path  # 상태 저장

            # 이미지가 업로드되었을 경우 미리보기 및 조작 버튼 표시
        if st.session_state.uploaded_image_path:
            st.subheader("📷 업로드한 이미지 미리보기")
            
            # 이미지 불러오기
            img = Image.open(st.session_state.uploaded_image_path)

            # 회전 및 반전 적용
            img = img.rotate(st.session_state.rotation_angle, expand=True)
            if st.session_state.flip_horizontal:
                img = ImageOps.mirror(img)
            if st.session_state.flip_vertical:
                img = ImageOps.flip(img)

            # 이미지 표시
            st.image(img, caption="변환된 이미지", use_column_width=True)

            # 조작 버튼 (첫 번째 줄)
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("↪️ 왼쪽으로 회전", use_container_width=True):
                    st.session_state.rotation_angle = (st.session_state.rotation_angle + 90) % 360
                    st.rerun()
            with col2:
                if st.button("↩️ 오른쪽으로 회전", use_container_width=True):
                    st.session_state.rotation_angle = (st.session_state.rotation_angle + 270) % 360
                    st.rerun()
            with col3:
                if st.button("↔ 좌우 반전", use_container_width=True):
                    st.session_state.flip_horizontal = not st.session_state.flip_horizontal
                    st.rerun()

            # ✅ 완료 버튼 (두 번째 줄, 아래쪽으로 배치)
            col_refresh, col_done = st.columns(2)
            with col_refresh:
                if st.button("♻ 초기화", use_container_width=True):
                    st.session_state.rotation_angle = 0
                    st.session_state.flip_horizontal = False
                    st.session_state.flip_vertical = False
                    st.rerun()
            with col_done:
                if st.button("✅ 완료", use_container_width=True):  # 버튼을 넓게 표시
                    img.save(st.session_state.uploaded_image_path)
                    # 이미지 미세조정 후 저장
                    img=ProcessFile(image_path, image_path)

                    st.success("변환된 이미지가 저장되었습니다! 🚀")
                    st.session_state.uploaded_image = img
                    st.session_state.timestamp = timestamp
                    st.session_state.image_path = image_path
                    st.session_state.current_step += 1


    # Step 2: OCR 처리 및 음성 파일 생성
    if st.session_state.current_step == 2:
        st.header("2. OCR 처리")
        with st.spinner("OCR을 수행 중입니다..."):
            OCR_result = OCR(st.session_state.image_path, st.session_state.timestamp)  # image_path 사용
        if OCR_result!='success':
            st.error("⚠️ Text 인식에 실패했습니다. 다른 이미지를 사용해주세요. 메인화면으로 돌아갑니다.")  # 팝업 메시지 표시
            time.sleep(3)
            st.session_state.current_step = 1
            st.session_state.uploaded_image = None
            st.session_state.timestamp = None
            st.session_state.image_path = None
            st.switch_page("main_front.py")  #값 초기화 후 메인으로 이동

        st.success("OCR 처리가 완료되었습니다!")
        
        st.header("3. 번역")
        with st.spinner("텍스트 번역 중..."):
            translation(st.session_state.timestamp)
        st.success("번역이 완료되었습니다!")

        st.header("4. 음성 파일 생성")
        with st.spinner("음성 파일을 생성 중입니다..."):
            naver_tts(input_json=f'saves/save2_extracted{st.session_state.timestamp}.json', output_folder='saves/voices')
        st.success("음성 파일 생성이 완료되었습니다!")
        st.session_state.current_step += 1

    # Step 3: 학습 모드 선택
    if st.session_state.current_step == 3:
        st.header("5. 학습 모드 선택")
        study_mode = st.radio("학습 모드를 선택하세요.", ("읽기 (Reading)", "듣기 (Dictation)", "쓰기 (Writing)"))
        if st.button("학습 시작"):
            if study_mode == "읽기 (Reading)":
                st.session_state.current_step = 4  # Reading 모드로 들어가면 4로 변경
                reading(st.session_state.timestamp, voice_folder='saves/voices')
            elif study_mode == "듣기 (Dictation)":
                st.session_state.current_step = 5  # Dictation 모드로 들어가면 5으로 변경
                dictation_mode(input_json=f'saves/save2_extracted{st.session_state.timestamp}.json', output_folder='saves/voices')
            elif study_mode == "쓰기 (Writing)":
                st.session_state.current_step = 6  # Writing 모드로 들어가면 6로 변경
                writing_mode(st.session_state.timestamp)
            st.rerun()
    elif st.session_state.current_step == 4:
        reading(st.session_state.timestamp, voice_folder='saves/voices')  # 학습 중에는 계속 reading 유지
    elif st.session_state.current_step == 5:
        dictation_mode(input_json=f'saves/save2_extracted{st.session_state.timestamp}.json', output_folder='saves/voices')
    elif st.session_state.current_step == 6:
        writing_mode(st.session_state.timestamp)
        
if __name__ == "__main__":
    main()
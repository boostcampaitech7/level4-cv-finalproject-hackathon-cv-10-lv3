import streamlit as st
from streamlit_mic_recorder import mic_recorder
import tempfile
import os
import wave
import numpy as np
from APIs.input_utils.clova_speech import ClovaSpeechClient

def convert_webm_to_wav(webm_bytes, output_path):
    """ WebM 파일을 WAV로 변환하는 함수 """
    temp_webm = tempfile.NamedTemporaryFile(delete=False, suffix=".webm")
    temp_wav = output_path

    try:
        # WebM 파일 저장
        with open(temp_webm.name, "wb") as f:
            f.write(webm_bytes)

        # FFmpeg을 사용하여 변환 (FFmpeg이 설치되어 있어야 함)
        os.system(f"ffmpeg -i {temp_webm.name} -ac 1 -ar 16000 {temp_wav} -y")
        
        return temp_wav
    except Exception as e:
        st.error(f"오디오 변환 오류: {e}")
        return None
    finally:
        os.remove(temp_webm.name)

def userInput():
    st.write("📌 텍스트 입력 또는 음성 녹음을 통해 입력하세요.")
    input_type = st.radio("입력 형식을 선택하세요:", ["텍스트 입력", "음성 녹음"])

    if input_type == "텍스트 입력":
        return st.text_area("텍스트를 입력하세요:")

    elif input_type == "음성 녹음":
        st.write("🎤 음성을 녹음한 후 자동으로 변환됩니다.")
        audio = mic_recorder(
            start_prompt="🎙️ 녹음 시작",
            stop_prompt="⏹️ 녹음 중지",
            format="webm",  # webm으로 저장 후 변환
            key="recorder"
        )

        if audio:
            st.audio(audio["bytes"], format="audio/webm")

            # WebM → WAV 변환
            temp_wav_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
            wav_path = convert_webm_to_wav(audio["bytes"], temp_wav_path)

            if wav_path:
                st.session_state["audio_file_path"] = wav_path

                # ClovaSpeech API 요청
                st.write("📝 음성을 텍스트로 변환 중...")
                stt_client = ClovaSpeechClient()
                vtt = stt_client.req_upload(file=wav_path, completion="sync")

                if vtt.status_code == 200:
                    result = vtt.json()
                    voice_input = result.get("text", "")
                    st.write(f"✅ STT 결과: {voice_input}")

                    # 확인 및 수정 옵션 제공
                    retry = st.radio("입력된 텍스트가 맞습니까?", ["네", "아니요"])
                    if retry == "네":
                        return voice_input
                    else:
                        return st.text_area("수정된 텍스트를 입력하세요:")
                else:
                    st.error(f"STT 요청 실패: {vtt.status_code} - {vtt.text}")

    return None
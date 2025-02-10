import os
import streamlit as st

from APIs.image_alt import img_alt
from APIs.HCXexecutor import CompletionExecutor
from APIs.user_input import userInput
from APIs.feedback import feedback, feedback_review
from APIs.summary import generate_diary
from APIs.clova_voice import naver_tts_for_chat
from ImageStudy.Study.Diary import diary

MAX_TURNS = 11  # 대화 횟수 제한

def chat(timestamp):
    if "current_step" in st.session_state and st.session_state.current_step == 4:
        diary(timestamp)
        st.stop()  # 이후 코드 실행 방지

    st.title("🖼️ Chat Mode")
    
    # 학습을 새로 시작할 때 상태 초기화
    if "Chat_change_mode" in st.session_state and st.session_state.Chat_change_mode:
        st.session_state.Chat_change_mode = False
        st.session_state.Chat_is_finished = False
        st.session_state.retry = False
        st.session_state.chat_history = []
        st.session_state.chat_turns = 0
        st.session_state.preset_text = [
            {"role":"system","content":"사용자의 가장 처음 입력으로 이미지의 대체 텍스트가 들어옵니다. 시스템은 해당 설명을 바탕으로 이미지를 보고 친구와 이야기하는 것처럼 대화를 시작합니다. 이미지는 사용자가 오늘 보낸 하루와 관련이 있습니다. 적절한 질문을 제시하고, 사용자의 답변에 반응하시오. 대화는 영어로 진행합니다. 줄바꿈을 사용하지 말고 한 문단으로 대화하시오."},
            {"role": "user", "content": None}
        ]
    
    # 상태 초기화
    if "Chat_change_mode" not in st.session_state:
        st.session_state.Chat_change_mode = False
    if "Chat_is_finished" not in st.session_state:
        st.session_state.Chat_is_finished = False
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "chat_turns" not in st.session_state:
        st.session_state.chat_turns = 0
    if "retry" not in st.session_state:
        st.session_state.retry = False
    
    if "preset_text" not in st.session_state:
        st.session_state.preset_text = [
            {"role":"system","content":"사용자의 가장 처음 입력으로 이미지의 대체 텍스트가 들어옵니다. 시스템은 해당 설명을 바탕으로 이미지를 보고 친구와 이야기하는 것처럼 대화를 시작합니다. 이미지는 사용자가 오늘 보낸 하루와 관련이 있습니다. 적절한 질문을 제시하고, 사용자의 답변에 반응하시오. 대화는 영어로 진행합니다. 줄바꿈을 사용하지 말고 한 문단으로 대화하시오."},
            {"role": "user", "content": None}
        ]

    if "current_step" in st.session_state:
        st.session_state.current_step = 3

    if st.session_state.Chat_is_finished:
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
        return
    
    preset_text = st.session_state.preset_text

    request_data = {
    'messages': preset_text,
    'topP': 0.8,
    'topK': 0,
    'maxTokens': 100,
    'temperature': 0.6,
    'repeatPenalty': 5.0,
    'stopBefore': [],
    'includeAiFilters': True
}

    completion_executor = CompletionExecutor()

    image_alt_path = f"uploads/image_{timestamp}_alt_text.txt"
    image_path = f"uploads/image_{timestamp}.jpg"

    # 이미지 대체 텍스트 가져오기
    if os.path.isfile(image_alt_path):
        with open(image_alt_path, 'r', encoding='utf-8') as f:
            initial_input = f.read()
    else:
        initial_input = img_alt(timestamp)

    preset_text[1]['content'] = initial_input

    # 첫 대화 시작: 챗봇이 먼저 반응
    if not st.session_state.chat_history:
        st.session_state.chat_history.append(("📷 Image:", image_path))

        response = completion_executor.execute(request_data)
        preset_text.append({"role": "assistant", "content": response})
        st.session_state.chat_history.append(("🤖 Chatbot:", response))

    # UI에 대화 내역 출력 준비
    # Font Awesome CDN
    st.markdown(
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">',
        unsafe_allow_html=True
    )
    st.markdown("""
        <style>
            .chat-container {
                width: 100%;
                max-width: 600px;
                margin: auto;
                font-family: Arial, sans-serif;
            }
            
            .chat1, .chat2 {
                display: flex;
                align-items: center;
                margin-bottom: 10px;
            }

            .chat1 .perso-mess, .chat2 .perso-mess {
                padding: 10px 15px;
                border-radius: 15px;
                font-size: 14px;
                max-width: 70%;
                display: flex;
                align-items: center;
            }

            /* 로봇 채팅 (왼쪽) */
            .chat1 {
                justify-content: flex-start;
            }

            .chat1 .perso-mess {
                background: #dfdbdb;
                border-radius: 15px;
            }

            .chat1 .emoji {
                font-size: 24px;
                margin-right: 10px;
            }

            /* 사용자 채팅 (오른쪽) */
            .chat2 {
                justify-content: flex-end;
            }

            .chat2 .perso-mess {
                background: #7cbf3c;
                color: white;
                text-align: right;
                border-radius: 15px;
                flex-direction: column;
                align-items: flex-end;
            }

            .chat2 .emoji {
                font-size: 24px;
                margin-left: 10px;
            }

            .chat2 .image-content img {
                max-width: 150px;
                border-radius: 10px;
                margin-top: 5px;
            }

        </style>
    """, unsafe_allow_html=True)
    
    for role, content in st.session_state.chat_history:
        if role == "📷 Image:":
            col1, col2, col3 = st.columns([1, 1, 3])
            with col3:
                col1, col2 = st.columns([9, 1])

                with col1:
                    st.image(content, width=400)

                with col2:
                    st.markdown(
                        """
                        <div style="
                            display: flex;
                            align-items: flex-end;
                            height: 100%;
                        ">
                            <p style="font-size: 25px;">🧑</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


        elif role == "🤖 Chatbot:":
            chat1(content)
        else:
            chat2(content)

    # 대화 횟수 제한 체크
    if st.session_state.chat_turns >= MAX_TURNS:
        st.success("🔚 대화가 10번을 초과하여 자동 종료되었습니다.")
        st.session_state.Chat_is_finished = True
        return

    # 사용자 입력 받기
    user_input = userInput()

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Send", use_container_width=True):
            if user_input.strip():
                preset_text.append({"role": "user", "content": user_input})
                st.session_state.chat_history.append(("🙋 You:", user_input))
                
                response = completion_executor.execute(request_data)
                preset_text.append({"role": "assistant", "content": response})
                st.session_state.chat_history.append(("🤖 Chatbot:", response))

                st.session_state.chat_turns += 1
                st.rerun()

    with col2:
        if st.button("🔄️ 채팅 재생성", use_container_width=True):
            if st.session_state.chat_history:
                preset_text.pop()
                st.session_state.chat_history.pop()  # 마지막 챗봇 응답 제거

                response = completion_executor.execute(request_data)
                preset_text.append({"role": "assistant", "content": response})
                st.session_state.chat_history.append(("🤖 Chatbot:", response))
                st.rerun()

    with col3:
        if st.button("🔊 음성 듣기", use_container_width=True):
            chat_turn = st.session_state.chat_turns
            tts_file_name = f'chat{timestamp}_response{chat_turn}.mp3'
            tts_file_path = os.path.join('saves/voices/', tts_file_name)

            if not os.path.isfile(tts_file_path):
                last_response = st.session_state.chat_history[-1][1] if st.session_state.chat_history else "No response yet"
                tts_file_path = naver_tts_for_chat(last_response, output_file_name=tts_file_name)
            st.audio(tts_file_path, format='audio/mp3')

    col1 = st.columns(1)[0]
    with col1:
        if st.button("🧑‍🏫 AI 튜터의 피드백 확인하기", use_container_width=True):
            if user_input:
                request_data = user_input
            elif st.session_state.chat_history:
                request_data = preset_text[len(preset_text) - 2]["content"]
            feedback_text = feedback(request_data, save=True, timestamp=timestamp)

            # 문자열 변환
            feedback_text = feedback_text.strip()
            feedback_text = feedback_text.replace("\n", "<br>")
            feedback_text = feedback_text.replace("수정된 문장", "<span style='color: #007BFF; font-weight: bold;'>수정된 문장</span>")
            feedback_text = feedback_text.replace("설명", "<span style='color: #007BFF; font-weight: bold;'>설명</span>")

            st.markdown(
                f"""
                    <div style="
                        background-color: #f0f8ff;
                        padding: 15px;
                        border-radius: 10px;
                        border-left: 5px solid #007BFF;
                        white-space: pre-line;
                    "><strong>📘 AI 피드백</strong><br>
                    <span style="margin: 0;">{feedback_text}</span></div>
                    <br>
                """,
                unsafe_allow_html=True
            )
    
    # 영어 일기 생성하기
    col1 = st.columns(1)[0]
    with col1:
        if st.button("📓 영어 일기 생성하기", use_container_width=True):
            chathist = st.session_state.chat_history
            diary_text = generate_diary(chathist[1:len(chathist) - 1], timestamp)

            # 생성된 일기 표시
            st.write("**✨ 영어 일기가 생성되었어요!**")
            st.markdown(
                f"""
                <div style="
                    background-color: #fff7dc;
                    padding: 15px;
                    border-radius: 10px
                ">
                    {diary_text.strip()}
                </div>
                <br>
                """,
                unsafe_allow_html=True
            )

    # 종료 버튼 추가
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🖼️ 학습 모드로 돌아가기", use_container_width=True):
            st.session_state.Chat_change_mode = True
            st.session_state.current_step = 2
            st.rerun()
    with col2:
        if st.button("❌ 학습 종료", use_container_width=True):
            st.session_state.Chat_is_finished = True
            st.rerun()

    # 홈 화면 버튼
    st.divider()
    if st.button("⬅️ 홈 화면으로 돌아가기", use_container_width=True):
        st.session_state.current_step = 1
        st.session_state.Chat_change_mode = False
        st.session_state.Chat_is_finished = False
        st.session_state.uploaded_image = None
        st.session_state.timestamp = None
        st.session_state.image_path = None
        st.session_state.retry = False
        st.session_state.chat_history = []
        st.session_state.chat_turns = 0
        st.switch_page("main_front.py")

# chatbot 메세지 디자인
def chat1(message):
    chat_html = f"""
    <div class="chat1">
        <span class="emoji">🤖</span>
        <div class="perso-mess">{message}</div>
    </div>
    """
    st.markdown(chat_html, unsafe_allow_html=True)


# 사용자 메세지 디자인
def chat2(message):
    chat_html = f"""
        <div class="chat2">
            <div class="perso-mess">
                {message}
            </div>
        <span class="emoji">🧑</span>
        </div>
        """
    st.markdown(chat_html, unsafe_allow_html=True)

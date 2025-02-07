## 코드 1 ## 

# import time
# import os
# import yaml
# import streamlit as st

# from APIs.image_alt import img_alt
# from APIs.HCXexecutor import CompletionExecutor
# from APIs.user_input import userInput
# from APIs.feedback import feedback

# # 설정 로드
# with open('config.yaml', 'r') as f:
#     config = yaml.full_load(f)
# HOST = config["HCX_host"]
# API_KEY = config["HCX_api_key"]
# REQUEST_ID = config["HCX_request_id"]

# MAX_TURNS = 10  # 대화 횟수 제한

# def chat(timestamp):
#     st.title("🖼️ Chat Mode")
    
#     # ✅ 학습을 새로 시작할 때 상태 초기화
#     if "Chat_change_mode" in st.session_state and st.session_state.Chat_change_mode:
#         st.session_state.Chat_change_mode = False
#         st.session_state.Chat_is_finished = False
#         st.session_state.retry = False
#         st.session_state.chat_history = []
#         st.session_state.chat_turns = 0
        
#     # ✅ 상태 초기화
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = []
#     if "retry" not in st.session_state:
#         st.session_state.retry = False
#     if "chat_turns" not in st.session_state:
#         st.session_state.chat_turns = 0  # 대화 횟수
#     if "Chat_is_finished" not in st.session_state:
#         st.session_state.Chat_is_finished = False  
#     if "Chat_change_mode" not in st.session_state:
#         st.session_state.Chat_change_mode = False
    
#     if "current_step" in st.session_state:
#         st.session_state.current_step = 3
    
#     if st.session_state.Chat_is_finished:
#         st.success("🎉 학습이 종료되었습니다. 오늘도 수고하셨습니다!")
#         return
    
#     completion_executor = CompletionExecutor(
#         host=HOST,
#         api_key=API_KEY,
#         request_id=REQUEST_ID
#     )
    
#     image_alt_path = f"uploads/image_{timestamp}_alt_text.txt"
    
#     preset_text = [{"role":"system","content":"사용자의 가장 처음 입력으로 이미지의 대체 텍스트가 들어옵니다. 시스템은 해당 설명을 바탕으로 이미지를 보고 친구와 이야기하는 것처럼 대화를 시작합니다. 이미지는 사용자가 오늘 보낸 하루와 관련이 있습니다. 적절한 질문을 제시하고, 사용자의 답변에 반응하시오. 대화는 영어로 진행합니다. 줄바꿈을 사용하지 말고 한 문단으로 대화하시오."},{"role":"user","content":None}]
    
    
#     # **이미지 대체 텍스트 가져오기**
#     if os.path.isfile(image_alt_path):
#         with open(image_alt_path, 'r', encoding='utf-8') as f:
#             initial_input = f.read()
#     else:
#         initial_input = img_alt(timestamp)  # 자동 생성
    
#     # ✅ 첫 대화 시작: 챗봇이 먼저 반응
#     if not st.session_state.chat_history:
#         st.session_state.chat_history.append(("📷 Image Description:", initial_input))
#         preset_text[1]["content"] = initial_input
#         request_data = {
#             'messages': preset_text,
#             'topP': 0.8,
#             'topK': 0,
#             'maxTokens': 100,
#             'temperature': 0.6,
#             'repeatPenalty': 5.0,
#             'stopBefore': [],
#             'includeAiFilters': True
#         }

#         # 챗봇이 먼저 대화를 시작
#         chatbot_response = completion_executor.execute(request_data)
#         st.session_state.chat_history.append(("🤖 Chatbot:", chatbot_response))

#     # ✅ UI에 대화 내역 출력
#     for role, text in st.session_state.chat_history:
#         st.write(f"**{role}**: {text}")

#     # ✅ 대화 횟수 제한 체크
#     if st.session_state.chat_turns >= MAX_TURNS:
#         st.success("🔚 대화가 10번을 초과하여 자동 종료되었습니다.")
#         st.session_state.Chat_is_finished = True
#         return

#     # ✅ 사용자 입력 받기
#     user_input = userInput()

#     col1, col2, col3 = st.columns(3)
#     with col1:
#         if st.button("Send"):
#             if user_input.strip():
#                 st.session_state.chat_history.append(("🙋 You:", user_input))
#                 preset_text.append({"role": "user", "content": user_input})
                
#                 # 챗봇 응답
#                 request_data = {
#                     'messages': preset_text,
#                     'topP': 0.8,
#                     'topK': 0,
#                     'maxTokens': 100,
#                     'temperature': 0.6,
#                     'repeatPenalty': 5.0,
#                     'stopBefore': [],
#                     'includeAiFilters': True
#                 }
#                 response = completion_executor.execute(request_data)
#                 st.session_state.chat_history.append(("🤖 Chatbot:", response))
#                 st.session_state.chat_turns += 1
#                 st.rerun()

#     with col2:
#         if st.button("Retry"):
#             if st.session_state.chat_history:
#                 last_user_input = st.session_state.chat_history[-2][1]
#                 preset_text.append({"role": "user", "content": last_user_input})
                
#                 # 챗봇 재응답
#                 response = completion_executor.execute(request_data)
#                 st.session_state.chat_history[-1] = ("🤖 Chatbot:", response)
#                 st.rerun()

#     with col3:
#         if st.button("Feedback"):
#             last_bot_response = st.session_state.chat_history[-1][1] if st.session_state.chat_history else ""
#             feedback_text = feedback(user_input, last_bot_response)
#             st.write(f"📝 Feedback: {feedback_text}")

#     # ✅ 종료 버튼 추가
#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button("🖼️ 학습 모드로 돌아가기", use_container_width=True):
#             st.session_state.Chat_change_mode = True
#             st.session_state.current_step = 2
#             st.rerun()
#     with col2:
#         if st.button("❌ 학습 종료", use_container_width=True):
#             st.session_state.Chat_is_finished = True
#             st.rerun()

#     # 홈 화면 버튼
#     st.divider()
#     if st.button("⬅️ 홈 화면으로 돌아가기", use_container_width=True):
#         st.session_state.current_step = 2
#         st.session_state.Chat_change_mode = False
#         st.session_state.Chat_is_finished = False
#         st.session_state.retry = False
#         st.session_state.chat_history = []
#         st.session_state.chat_turns = 0
#         st.switch_page("main_front.py")

## 코드 2 ## 
import time
import os
import yaml
import streamlit as st

from APIs.image_alt import img_alt
from APIs.HCXexecutor import CompletionExecutor
from APIs.user_input import userInput
from APIs.feedback import feedback

# 설정 로드
with open('config.yaml', 'r') as f:
    config = yaml.full_load(f)
HOST = config["HCX_host"]
API_KEY = config["HCX_api_key"]
REQUEST_ID = config["HCX_request_id"]

MAX_TURNS = 10  # 대화 횟수 제한

def chat(timestamp):
    st.title("🖼️ Chat Mode")
    
    # ✅ 학습을 새로 시작할 때 상태 초기화
    if "Chat_change_mode" in st.session_state and st.session_state.Chat_change_mode:
        st.session_state.Chat_change_mode = False
        st.session_state.Chat_is_finished = False
        st.session_state.retry = False
        st.session_state.chat_history = []
        st.session_state.chat_turns = 0
    
    # ✅ 상태 초기화
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

    if "current_step" in st.session_state:
        st.session_state.current_step = 3

    if st.session_state.Chat_is_finished:
        st.success("🎉 학습이 종료되었습니다. 오늘도 수고하셨습니다!")
        return
    
    completion_executor = CompletionExecutor(
        host=HOST,
        api_key=API_KEY,
        request_id=REQUEST_ID
    )

    image_alt_path = f"uploads/image_{timestamp}_alt_text.txt"

    # **이미지 대체 텍스트 가져오기**
    if os.path.isfile(image_alt_path):
        with open(image_alt_path, 'r', encoding='utf-8') as f:
            initial_input = f.read()
    else:
        initial_input = img_alt(timestamp)  # 자동 생성

    # ✅ 첫 대화 시작: 챗봇이 먼저 반응
    if not st.session_state.chat_history:
        st.session_state.chat_history.append(("📷 Image Description:", initial_input))

        preset_text = [{"role":"system","content":"사용자의 가장 처음 입력으로 이미지의 대체 텍스트가 들어옵니다. 시스템은 해당 설명을 바탕으로 이미지를 보고 친구와 이야기하는 것처럼 대화를 시작합니다. 이미지는 사용자가 오늘 보낸 하루와 관련이 있습니다. 적절한 질문을 제시하고, 사용자의 답변에 반응하시오. 대화는 영어로 진행합니다. 줄바꿈을 사용하지 말고 한 문단으로 대화하시오."},{"role": "user", "content": initial_input}]
        
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

        chatbot_response = completion_executor.execute(request_data)
        st.session_state.chat_history.append(("🤖 Chatbot:", chatbot_response))

    # ✅ UI에 대화 내역 출력
    for role, text in st.session_state.chat_history:
        st.write(f"**{role}**: {text}")

    # ✅ 대화 횟수 제한 체크
    if st.session_state.chat_turns >= MAX_TURNS:
        st.success("🔚 대화가 10번을 초과하여 자동 종료되었습니다.")
        st.session_state.Chat_is_finished = True
        return

    # ✅ 사용자 입력 받기
    user_input = userInput()

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Send"):
            if user_input.strip():
                st.session_state.chat_history.append(("🙋 You:", user_input))

                preset_text = [{"role": "user", "content": user_input}]
                
                # 챗봇 응답 요청
                request_data = {
                    'messages': [{"role": role.lower(), "content": text} for role, text in st.session_state.chat_history],
                    'topP': 0.8,
                    'topK': 0,
                    'maxTokens': 100,
                    'temperature': 0.6,
                    'repeatPenalty': 5.0,
                    'stopBefore': [],
                    'includeAiFilters': True
                }
                
                response = completion_executor.execute(request_data)
                st.session_state.chat_history.append(("🤖 Chatbot:", response))
                st.session_state.chat_turns += 1
                st.rerun()

    with col2:
        if st.button("Retry"):
            if st.session_state.chat_history:
                last_user_input = st.session_state.chat_history[-2][1]  # 마지막 사용자 입력
                st.session_state.chat_history.pop()  # 마지막 챗봇 응답 제거
                
                request_data = {
                    'messages': [{"role": role.lower(), "content": text} for role, text in st.session_state.chat_history],
                    'topP': 0.8,
                    'topK': 0,
                    'maxTokens': 100,
                    'temperature': 0.6,
                    'repeatPenalty': 5.0,
                    'stopBefore': [],
                    'includeAiFilters': True
                }

                response = completion_executor.execute(request_data)
                st.session_state.chat_history.append(("🤖 Chatbot:", response))
                st.rerun()

    with col3:
        if st.button("Feedback"):
            if st.session_state.chat_history:
                last_bot_response = st.session_state.chat_history[-1][1]
                feedback_text = feedback(last_bot_response)  # 인자 하나만 전달하도록 수정
                st.write(f"📝 Feedback: {feedback_text}")

    # ✅ 종료 버튼 추가
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
        st.session_state.current_step = 2
        st.session_state.Chat_change_mode = False
        st.session_state.Chat_is_finished = False
        st.session_state.retry = False
        st.session_state.chat_history = []
        st.session_state.chat_turns = 0
        st.switch_page("main_front.py")
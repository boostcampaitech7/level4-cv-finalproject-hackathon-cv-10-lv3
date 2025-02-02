import time
from APIs import img_alt
import os
import yaml

from APIs.HCXexecutor import CompletionExecutor
from Project.APIs.user_input import userInput
input = userInput

from APIs.feedback import feedback

log_path = "/data/ephemeral/home/level4-cv-finalproject-hackathon-cv-10-lv3/Project/ImageStudy/logfile/chatlog.txt"

with open('config.yaml', 'r') as f:
    config = yaml.full_load(f)
HOST = config["HCX_host"]
API_KEY = config["HCX_api_key"]
REQUEST_ID = config["HCX_request_id"]


def chat(image):
    with open(log_path, 'a', encoding='utf-8') as logfile:
        logfile.write('\n==================== ' + time.strftime('%Y.%m.%d - %H:%M:%S') + ' ====================\n')

    completion_executor = CompletionExecutor(
        host=HOST,
        api_key=API_KEY,
        request_id=REQUEST_ID
    )

    preset_text = [{"role":"system","content":"사용자의 가장 처음 입력으로 이미지의 대체 텍스트가 들어옵니다. 시스템은 해당 설명을 바탕으로 이미지를 보고 친구와 이야기하는 것처럼 대화를 시작합니다. 이미지는 사용자가 오늘 보낸 하루와 관련이 있습니다. 적절한 질문을 제시하고, 사용자의 답변에 반응하시오. 대화는 영어로 진행합니다. 줄바꿈을 사용하지 말고 한 문단으로 대화하시오."},{"role":"user","content":None}]
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
    image_name = image.split('/')[-1].split('.')[0]
    image_alt_path = f"/data/ephemeral/home/clova/img/{image_name}_alt_text.txt"

    for i in range(10):
        with open(log_path, 'a', encoding='utf-8') as logfile:
            if i:
                user_input = input()
                if len(user_input) > 1:
                    logfile.write(f"[{time.strftime('%X')}] feedback: {feedback(user_input)}\n")
                    
            elif os.path.isfile(image_alt_path):
                with open(image_alt_path, 'r', encoding='utf-8') as f:
                    user_input = f.read()
            else:
                user_input = img_alt(image_name)
            
            print(user_input)

            if user_input == 'E':
                logfile.write(f"> end\n")
                break
            elif user_input == 'R':
                logfile.write(f"> retry\n")

            else:
                preset_text[1]["content"] = user_input

                if i == 0:
                    logfile.write(f"[{time.strftime('%X')}] image: {user_input}\n")
                else:
                    logfile.write(f"[{time.strftime('%X')}] user: {user_input}\n")
        with open(log_path, 'a', encoding='utf-8') as logfile:
            logfile.write(f"[{time.strftime('%X')}] chatbot: {completion_executor.execute(request_data)}\n")
    
    with open(log_path, 'a', encoding='utf-8') as logfile:
        logfile.write('==================== chating closed ====================\n')
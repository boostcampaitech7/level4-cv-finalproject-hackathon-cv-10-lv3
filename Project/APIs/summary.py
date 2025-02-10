import os
import time

from APIs.HCXexecutor import CompletionExecutor

completion_executor = CompletionExecutor()

def generate_diary(chat_history, timestamp):
    """채팅 기록을 요약하여 일기 형식으로 변환하는 함수"""

    if not chat_history:
        return "No user responses to summarize."
    
    texts = ''
    for c in chat_history:
        texts += f'{c[0][2:]} {c[1]}\n'

    diary_prompt = f""" Rewrite the following chating history in natural diary-style lines:
        {texts}"""

    summary_prompt = [{
        "role": "system",
        "content": "You are an AI assistant who rewrites the conversation in a **English diary** format. The diary text should be in the first person and describe the day as if the user wrote it. Don't write a introduction like 'In my diary'. Focus more on the contents of **user** than the contents of chatbot."
    }, {
        "role": "user",
        "content": diary_prompt
    }]
    
    request_data = {
        'messages': summary_prompt,
        'topP': 0.8,
        'topK': 0,
        'maxTokens': 500,
        'temperature': 0.7,
        'repeatPenalty': 5.0,
        'stopBefore': [],
        'includeAiFilters': True
    }
    
    diary_text = completion_executor.execute(request_data)
    if not diary_text:
        return "사용자가 많아 요청을 처리할 수 없습니다. 다시 시도해주세요."
    
    diary_path = f'saves/diary/{timestamp}.txt'

    os.makedirs(os.path.dirname(diary_path), exist_ok=True)
    
    with open(diary_path, 'w', encoding='utf-8') as diary_file:
        diary_file.write(f'\n[{time.strftime("%Y-%m-%d")}]\n{diary_text}')
        diary_file.flush()
    
    print("Diary saved.")
    return diary_text

generate_diary
import yaml
import time

from APIs.HCXExecutor import CompletionExecutor

completion_executor = CompletionExecutor()

def generate_diary(chat_history):
    """사용자의 응답을 요약하여 일기 형식으로 변환하는 함수"""

    if not chat_history:
        return "No user responses to summarize."
    
    user_text = "\n".join(chat_history)

    diary_prompt = f""" Rewrite the following user responses in natural diary-style lines:
        {user_text}"""

    summary_prompt = [{
        "role": "system",
        "content": "You are an AI assistant who rewrites the conversation in a diary format. The diary entry should be in the first person and describe the day as if the user wrote it."
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
    
    diary_entry = completion_executor.execute(request_data)
    
    with open('diary.txt', 'a', encoding='utf-8') as diary_file:
        diary_file.write(f'\n[{time.strftime("%Y.%m.%d")}]\n{diary_entry}\n')
        diary_file.flush()
    
    print("==================== Diary entry saved. ====================")

generate_diary
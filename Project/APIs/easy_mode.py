from APIs.HCXexecutor import CompletionExecutor
import json
import random

def easymode(sent):
    # 클라이언트 초기화
    completion_executor = CompletionExecutor()

    #번역 요청
    preset_text = [{"role":"system",
                    "content":f"- 영단어 빈칸 퀴즈를 만드는 고등학교 선생님 역할입니다. - 입력 문장: {sent} -입력 문장에서 단어 하나를 [빈칸] 으로 대체합니다. - 학생들이 배워야하는 단어를 고릅니다. - 변경된 문장만 출력합니다."}]
        

    # 요청서 작성
    request_data = {
            'messages': preset_text,
            'topP': 0.8,
            'topK': 0,
            'maxTokens': 100,
            'temperature': 0.2,
            'repeatPenalty': 3.0,
            'stopBefore': ['###'],
            'includeAiFilters': True,
            'seed': 0
        }
    cnt=0
    response_text = completion_executor.execute(request_data)
    while('빈칸' not in response_text):
        response_text = completion_executor.execute(request_data)
        cnt+=1
        if cnt ==5:
            words = sent.split()
            change=random.randrange(0,len(words))
            words[change]='[빈칸]'
            response_text=' '.join(words)
            break
    return response_text



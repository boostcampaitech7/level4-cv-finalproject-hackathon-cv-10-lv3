from APIs.HCXexecutor import CompletionExecutor
import json

def easymode(sent):
    # 클라이언트 초기화
    completion_executor = CompletionExecutor()

    #번역 요청
    preset_text = [{"role":"system",
                    "content":f"- 빈칸 퀴즈를 만드는 고등학교 선생님 역할입니다. - 입력 문장: {sent} -입력 문장에서 단어 하나를 [빈칸] 으로 변경합니다. - 변경된 문장만 출력합니다."}]
        

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

    response_text = completion_executor.execute(request_data)
    return response_text



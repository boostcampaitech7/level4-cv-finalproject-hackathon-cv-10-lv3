from APIs.HCXexecutor import CompletionExecutor
from APIs.clova_papago import translate_by_papago
import json

def call_hcx(req):
    # 클라이언트 초기화
    completion_executor = CompletionExecutor()
    # 요청서 작성
    request_data = {
            'messages': req,
            'topP': 0.8,
            'topK': 0,
            'maxTokens': 1000,
            'temperature': 0.3,
            'repeatPenalty': 3.0,
            'stopBefore': ['###'],
            'includeAiFilters': True,
            'seed': 0
        }

    result = completion_executor.execute(request_data)
    return result

def harmful(timestamp):
    input_file = f"saves/save1_ocr{timestamp}.json" #input파일!


    with open(input_file, "r", encoding="utf-8") as f:
        sentences = json.load(f)

    req = [{"role":"system",
            "content":f"- 입력 text: {sentences} -입력 text가 해로운 내용을 포함한 경우, 해로움을 출력합니다."}]
    result=call_hcx(req)
    if result=='해로움':
        return "harmful"
    else:
        return "fine"
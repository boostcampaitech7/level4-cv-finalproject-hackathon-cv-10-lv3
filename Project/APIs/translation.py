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

    result, harmful_score = completion_executor.execute(request_data, score=True)
    return result, harmful_score


def translation(timestamp):
    input_file = f"saves/save2_extracted{timestamp}.json"
    output_file = f"saves/save3_translation{timestamp}.json"

    with open(input_file, "r", encoding="utf-8") as f:
        sentences = json.load(f)
    translated=[]
    for sentence in sentences:
        cnt=0
        result=''
        while(result==''):
            req = [{"role":"system",
                    "content":f"- 입력 문장: {sentence} -입력 문장을 한국어로 번역합니다. -번역된 문장만 출력합니다. "}]
            result, harmful_score =call_hcx(req)
            if cnt == 5:
                result=translate_by_papago(sentence)
                break
        translated.append({"original": sentence,
                            "translation": result,
                            "harmful_score": harmful_score
                            })

    # 저장하기
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(translated, f, ensure_ascii=False, indent=4)

    print("Translation completed. Results saved to", output_file)
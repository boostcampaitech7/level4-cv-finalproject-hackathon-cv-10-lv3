import yaml
import requests
import json

with open('config.yaml', 'r') as f:
    config = yaml.full_load(f)
HOST = config["HCX_host"]
API_KEY = config["HCX_api_key"]
REQUEST_ID = config["HCX_request_id"]

class CompletionExecutor:
    def __init__(self, host, api_key, request_id):
        self._host = host
        self._api_key = api_key
        self._request_id = request_id

    def execute(self, completion_request):
        headers = {
            'Authorization': self._api_key,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'text/event-stream'
        }

        with requests.post(self._host + '/testapp/v1/chat-completions/HCX-DASH-001',
                       headers=headers, json=completion_request, stream=True) as r:
            # 결과 저장할 부분
            result_content = ""
            # data: {} 형태로 입력이 들어옴. 
            # 토큰 단위로 들어오고 마지막 data:{"message":{~~,{"content"}}} 에 완성된 문장이 있는 형태임.
            for line in r.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8")

                    # "event:result"이 포함된 부분에서 데이터를 처리
                    if "data:" in decoded_line:
                        # "data:"뒷부분만 씀. 이렇게 안할경우 json형태로 인식 못함.
                        data_part = decoded_line.split("data:", 1)[1]
                        #json형태로 바꿈
                        parsed_data = json.loads(data_part)
                        # parsed_data["message"]와 parsed_data["message"]["content"] 존재하는지 확인. -> 없는 응답도 있음.
                        if "message" in parsed_data and "content" in parsed_data["message"]:
                            result_content = parsed_data["message"]["content"]
            # 최종적으로 마지막 parsed_data["message"]["content"] 가 return됨.
            return result_content

        
def read_json_file(file_path):
    # JSON 파일을 읽어 리스트 형태의 문장 반환
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        if isinstance(data, list):
            return data
        else:
            raise ValueError("The JSON file must contain a list of sentences.")

def save_json_file(file_path, data):
    # 리스트 데이터를 JSON 파일로 저장
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def hcx_tunning(timestamp):
    # 클라이언트 초기화
    completion_executor = CompletionExecutor(
        host=HOST,
        api_key=API_KEY,
        request_id=REQUEST_ID
    )

    # 번역할 JSON 파일 경로
    input_file = f"saves/save3_translation{timestamp}.json"
    output_file = f"saves/save4_tunning{timestamp}.json"

    # JSON 파일에서 문장 리스트 읽기
    sentences = read_json_file(input_file)

    # 한문장씩 번역 요청
    tunning_sentences = []
    print("Translation Tunning")
    for i, sentece_pair in enumerate(sentences):
        preset_text = [{"role":"system",
                        "content":f"- 1번 문장은 영어 문장입니다. - 2번 문장은 1번 문장을 한국어로 번역한 문장입니다. \n - 2번 문장의 한국어를 자연스럽게 수정해주세요. - 수정된 문장이 1번 문장과 의미가 같아야합니다. \n - 출력은 반드시 [original: 1번 문장, tunning: 수정된 2번 문장] 형태로 반환하세요.\n - 1번문장, {sentece_pair['original']} 2번 문장, {sentece_pair['translation']} \n"}]
        
        
        # 요청서 작성
        request_data = {
            'messages': preset_text,
            'topP': 0.8,
            'topK': 0,
            'maxTokens': 300,
            'temperature': 0.3,
            'repeatPenalty': 3.0,
            'stopBefore': ['###'],
            'includeAiFilters': True,
            'seed': 0
        }
        # 튜닝 요청
        tunning_text = completion_executor.execute(request_data)
        # 문자열 처리
        lines = tunning_text.strip().split("\n")
        data = {}
        for line in lines:
            if "original" in line:
                data["original"] = line.split(":")[1].strip()
            elif "tuning" in line:
                data["translation"] = line.split(":")[1].strip()
        # 결과를 translated_sentences에 추가
        tunning_sentences.append(data)


    # 번역 결과 리스트를 JSON으로 저장 
    save_json_file(output_file, tunning_sentences)
    print("Tunning completed. Results saved to",  output_file)

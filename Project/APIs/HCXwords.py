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

def make_words(timestamp):
    # 클라이언트 초기화
    completion_executor = CompletionExecutor(
        host=HOST,
        api_key=API_KEY,
        request_id=REQUEST_ID
    )

    # 번역할 JSON 파일 경로
    input_file = f"saves/save2_extracted{timestamp}.json"
    output_file = f"saves/save5_words{timestamp}.json"

    # JSON 파일에서 문장 리스트 읽기
    sentences = read_json_file(input_file)

    # 한문장씩 번역 요청
    print("Extract words!")
    word_list = []
    for i, sentence in enumerate(sentences):
        preset_text = [{"role":"system",
                        "content":f"- 영어 문장이 주어집니다. - 문장에서 영어 단어를 뽑아 단어장을 만드려고 합니다. \n - 단어 추출이 필요한 문장은 다음과 같습니다. {sentence} \n - 중학교 수준 이상의 단어를 뽑아주세요. - 단어장에는 영단어, 뜻, 영단어를 활용한 예문과 예문의 번역이 필요합니다. \n - 출력은 [word: 영단어, mean: 뜻, example: 영어 예문, trans: 영어 예문 번역] 형태로 반환하세요.\n - 출력시 다음 예시를 참고하세요. [word: apple, mean: 사과, example: Sling me an apple, will you?, trans: 나한테 사과 하나 던져 주겠니?]\n[word: railway, mean: 기찻길, example: The bridge over the railway., trans: 기찻길 위로 놓인 다리.]\n[word: parts, mean: 부분, example: The machine is made up of several parts., trans: 그 기계는 여러 부분으로 이루어져 있다.]"}]
        

        
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
        # 단어장 요청
        words = completion_executor.execute(request_data)
        # 결과 정렬
        lines = words.strip().split("\n")  # 줄 단위로 분리
        dictionary = []

        for line in lines:
            if not line.startswith("[word:"):  # 잘못된 줄 무시 -> 재요청으로 변경애햐ㅏㅁ.
                continue
            line = line.strip("[]")  # 대괄호 제거
            pairs = line.split(",")  # key-value 쌍 분리
            data = {}
            for pair in pairs:
                if ": " not in pair:
                    continue
                key, value = pair.split(": ", 1)
                data[key.strip()] = value.strip()
            dictionary.append(data)
        word_list.append({"original":sentence, "words": dictionary})




    # 번역 결과 리스트를 JSON으로 저장 
    save_json_file(output_file, word_list)

    print("Extract words! completed. Results saved to:", output_file)
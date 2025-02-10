import requests
import uuid
import time
import json
import re
import yaml
import os


with open("config.yaml", "r") as f:
    config = yaml.full_load(f)
API_URL = config["OCR_api_url"]
SECRET_KET = config["OCR_secret_key"]
API_URL2 = config["OCR_api_url2"]
SECRET_KET2 = config["OCR_secret_key2"]

def OCR(image_parh, timestamp):
    # Text OCR
    api_url = API_URL
    secret_key = SECRET_KET
    image_file = image_parh  # 이미지 경로 수정 필요

    request_json = {
        "images": [{"format": "jpg", "name": "demo"}],
        "requestId": str(uuid.uuid4()),
        "version": "V2",
        "timestamp": int(round(time.time() * 1000)),
    }

    payload = {"message": json.dumps(request_json).encode("UTF-8")}
    files = [("file", open(image_file, "rb"))]
    headers = {"X-OCR-SECRET": secret_key}

    response = requests.request(
        "POST", api_url, headers=headers, data=payload, files=files
    )

    output_file = f"saves/save1_ocr{timestamp}.json"

    directory = os.path.dirname(output_file)
    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        response_data = response.json()
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(response_data, f, ensure_ascii=False, indent=4)
        print(f"Response saved to {output_file}")
    except json.JSONDecodeError:
        print("Failed to decode response as JSON")
    
    result = process_json(timestamp)
    print(result)
    if result=='success':
        return 'success'
    else:
        return 'retry'
    

def OCR2(image_parh, timestamp):
    # Text OCR
    api_url = API_URL2
    secret_key = SECRET_KET2
    image_file = image_parh  # 이미지 경로 수정 필요

    request_json = {
        "images": [{"format": "jpg", "name": "demo"}],
        "requestId": str(uuid.uuid4()),
        "version": "V2",
        "timestamp": int(round(time.time() * 1000)),
    }

    payload = {"message": json.dumps(request_json).encode("UTF-8")}
    files = [("file", open(image_file, "rb"))]
    headers = {"X-OCR-SECRET": secret_key}

    response = requests.request(
        "POST", api_url, headers=headers, data=payload, files=files
    )

    output_file = f"saves/save1_ocr{timestamp}.json"

    directory = os.path.dirname(output_file)
    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        response_data = response.json()
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(response_data, f, ensure_ascii=False, indent=4)
        print(f"Response saved to {output_file}")
    except json.JSONDecodeError:
        print("Failed to decode response as JSON")
    
    result = process_json(timestamp)
    result = tuning(timestamp)
    print(result)
    if result=='success':
        return 'success'
    else:
        return 'retry'


def process_data(data):
    try:
        return data["images"][0]["fields"]
    except KeyError:
        return "retry"

# JSON 데이터를 읽고 변환
def process_json(timestamp):
    # 파일 경로 설정
    input_file = f"saves/save1_ocr{timestamp}.json"
    output_file = f"saves/save2_extracted{timestamp}.json"

    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    # title의 inferText 추출 및 변환
    extracted_texts = []
    # 결과 부분만 가져오기
    part=process_data(data)
    if part=='retry':
        return part
    # 파트 순서대로 확인
    for part_n in part:
        infer_text = part_n.get("inferText", "")
        # \n을 공백으로 변경하고 문장 단위로 분리
        sentences = infer_text.replace("\n", " ")
        sentences = sentences.replace("- ", "")
        # 문장 단위로 나누기 ('.,!,?,",' + 공백 + 대문자 형태일 경우 문장이 끝나는 지점으로 판단.)
        sentences = re.split(r'(?<=[.!?"\'])\s+(?=[A-Z])', sentences)
        # 문장을 list에 저장
        extracted_texts.extend(sentences)

    # 첫 번째 문장이 비어있거나 대문자로 시작하지 않으면 제거
    if  extracted_texts[0]=='' or not extracted_texts[0][0].isupper():
        extracted_texts.pop(0)

    # 마지막 문장이 종결 기호로 끝나지 않으면 제거
    if not re.search(r'[.!?"\']$', extracted_texts[-1]):
        extracted_texts.pop()
    
    # 결과를 JSON 형식으로 저장
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(extracted_texts, file, ensure_ascii=False, indent=4)
    return "success"

def tuning(timestamp):
    output_file = f"saves/save2_extracted{timestamp}.json"
    with open(output_file, "r", encoding="utf-8") as file:
        data = json.load(file)  # JSON 파일 로드

    # 리스트 데이터를 공백으로 이어붙이기
    if isinstance(data, list):  # 리스트인지 확인
        text = " ".join(data)
    extracted_texts=[]
    sentences = re.split(r'(?<=[.!?"\'])\s+(?=[A-Z])', text)
    # 문장을 list에 저장
    extracted_texts.extend(sentences)
    # 첫 번째 문장이 비어있거나 대문자로 시작하지 않으면 제거
    if  extracted_texts[0]=='' or not extracted_texts[0][0].isupper():
        extracted_texts.pop(0)

    # 마지막 문장이 종결 기호로 끝나지 않으면 제거
    if not re.search(r'[.!?"\']$', extracted_texts[-1]):
        extracted_texts.pop()
    
    # 결과를 JSON 형식으로 저장
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(extracted_texts, file, ensure_ascii=False, indent=4)
    return "success"
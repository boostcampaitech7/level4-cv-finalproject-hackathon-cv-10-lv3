import os
import json
import urllib.request
import yaml
# 네이버 클라우드 플랫폼 API 키 설정
with open('config.yaml', 'r') as f:
    config = yaml.full_load(f)
CLIENT_ID = config["Voice_CLIENT_ID"]
CLIENT_SECRET = config["Voice_CLIENT_SECRET"]


def naver_tts(input_json='extracted.json', output_folder='saves/voices'):
    """
    네이버 TTS를 사용하여 입력된 문장을 음성 파일로 변환합니다.

    Args:
        input_json (str): JSON 파일 경로 (변환할 문장 포함)
        output_folder (str): 음성 파일 저장 폴더
    """
    # JSON 파일 로드
    with open(input_json, 'r', encoding='utf-8') as f:
        sentences = json.load(f)

    # 출력 폴더 생성
    os.makedirs(output_folder, exist_ok=True)

    # 각 문장을 TTS로 변환하여 저장
    for idx, sentence in enumerate(sentences, start=1):
        #print(f"Processing sentence {idx}/{len(sentences)}")
        
        # 문장 인코딩
        enc_text = urllib.parse.quote(sentence)
        data = f"speaker=danna&volume=0&speed=0&pitch=0&format=mp3&text={enc_text}"
        url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
        
        # 요청 생성
        request = urllib.request.Request(url)
        request.add_header("X-NCP-APIGW-API-KEY-ID", CLIENT_ID)
        request.add_header("X-NCP-APIGW-API-KEY", CLIENT_SECRET)
        
        try:
            # API 호출
            response = urllib.request.urlopen(request, data=data.encode('utf-8'))
            rescode = response.getcode()
            
            if rescode == 200:
                # 음성 파일 저장
                response_body = response.read()
                output_file = os.path.join(output_folder, f"voice_{idx}.mp3")
                with open(output_file, 'wb') as f:
                    f.write(response_body)
                print(f"Voice Saved: {output_file}")
            else:
                print(f"Error Code: {rescode} for sentence {idx}")
        except Exception as e:
            print(f"Error processing sentence {idx}: {str(e)}")

    print("TTS 변환 완료!")

def naver_tts_for_chat(text, output_folder='saves/voices', filename='response.mp3'):
    """
    네이버 TTS를 사용하여 입력된 문장을 음성 파일로 변환합니다.
    """

    os.makedirs(output_folder, exist_ok=True)

    enc_text = urllib.parse.quote(text)
    data = f"speaker=danna&volume=0&speed=0&pitch=0&format=mp3&text={enc_text}"
    url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"

    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID", CLIENT_ID)
    request.add_header("X-NCP-APIGW-API-KEY", CLIENT_SECRET)
    
    output_file = os.path.join(output_folder, filename)

    try:
        response = urllib.request.urlopen(request, data=data.encode('utf-8'))
        rescode = response.getcode()

        if rescode == 200:
            with open(output_file, 'wb') as f:
                f.write(response.read())
            return output_file
        else:
            print(f"TTS 오류 발생: {rescode}")
            return None
            
    except Exception as e:
        print(f"TTS 요청 중 오류 발생: {str(e)}")
        return None
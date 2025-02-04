# Papago Text Translation API
import json
import urllib.request
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.full_load(f)
client_id = config["PaPago_client_id"]
client_secret = config["PaPago_client_secret"]

def translate_sentence_by_sentence(text_list, source_language="en", target_language="ko"):

    translated_sentences = []
    url = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"

    for sentence in text_list:
        try:
            encText = urllib.parse.quote(sentence)
            data = f"source={source_language}&target={target_language}&text={encText}"
            request = urllib.request.Request(url)
            request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
            request.add_header("X-NCP-APIGW-API-KEY", client_secret)
            response = urllib.request.urlopen(request, data=data.encode("utf-8"))
            rescode = response.getcode()

            if rescode == 200:
                response_body = response.read()
                result_json = json.loads(response_body.decode("utf-8"))
                translated_text = result_json['message']['result']['translatedText']
                translated_sentences.append({
                    "original": sentence,
                    "translation": translated_text
                })
            else:
                translated_sentences.append({
                    "original": sentence,
                    "translation": f"Error: Could not translate sentence (rescode: {rescode})"
                })
        except Exception as e:
            translated_sentences.append({
                "original": sentence,
                "translation": f"Exception: {str(e)}"
            })
    
    return translated_sentences


def translate(timestamp):
    input_file = f"saves/save2_extracted{timestamp}.json" #input파일!
    output_file = f"saves/save3_translation{timestamp}.json" # output파일!

    with open(input_file, "r", encoding="utf-8") as f:
        sentences = json.load(f)

    # 번역실행
    print("Translation Start!")
    translated = translate_sentence_by_sentence(sentences, source_language="en", target_language="ko")

    # 저장하기
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(translated, f, ensure_ascii=False, indent=4)

    print("Translation completed. Results saved to", output_file)

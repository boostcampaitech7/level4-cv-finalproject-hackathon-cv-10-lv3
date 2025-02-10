import yaml
import json
import urllib.request

with open('config.yaml', 'r') as f:
    config = yaml.full_load(f)
client_id = config["PaPago_client_id"]
client_secret = config["PaPago_client_secret"]

def translate_by_papago(text, source_language="en", target_language="ko"):
    url = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"
    try:
        encText = urllib.parse.quote(text)
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
        else:
            translated_text="Error: Could not translate sentence (rescode: {rescode})"

    except Exception as e:
        translated_text=f"Exception: {str(e)}"
    return translated_text

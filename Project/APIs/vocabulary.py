import os
import json
from APIs.HCXexecutor import CompletionExecutor
from APIs.clova_papago import translate_by_papago

def call_hcx(req,token):
    # 클라이언트 초기화
    completion_executor = CompletionExecutor()
    # 요청서 작성
    request_data = {
            'messages': req,
            'topP': 0.8,
            'topK': 0,
            'maxTokens': token,
            'temperature': 0.3,
            'repeatPenalty': 3.0,
            'stopBefore': ['###'],
            'includeAiFilters': True,
            'seed': 0
        }

    result = completion_executor.execute(request_data).strip()
    return result


def make_words(idx, sentence, timestamp):
    # 번역할 JSON 파일 경로
    output_file = f"saves/save5_words{timestamp}.json"

    word_list = []
    words=[]
    cnt=0
    while(words==[]):
        cnt+=1
        find_words=[{"role":"system",
                    "content":f"- 입력 문장: {sentence} - 입력 문장에서 고등학교 수준 이상의 영어 단어들을 추출합니다. - 고유 명사 제외해줘 - 숫자가 들어간 단어 제외해줘 - 추출된 단어만 ,로 분리하여 출력합니다. - 출력 예시: apple, banana, camera"}]
        
        result=call_hcx(find_words, 300)    
        # 결과 정렬
        lines = result.split(",")  # 줄 단위로 분리
        for word in lines:
            words.append(word.strip())
            
        if words==['']:
            words=[]

        if cnt==5: 
            break
        

    if words!=['']:
        for word in words:

            if word=='' or word[0].isupper(): # 빈문자인 경우 
                continue

            meaning=translate_by_papago(word) #papago

            find_example= [{"role":"system",
                            "content":f"- 입력 단어: {word} - 입력 단어의 영어 예문을 하나 작성합니다. -예문만 출력합니다."}]
            example=''
            cnt=0
            while(example==''):
                example=call_hcx(find_example, 500)
                cnt+=1
                if cnt==5:
                    example='예문이 없습니다.'

            if example !='예문이 없습니다.':
                translate=translate_by_papago(example) #papago
                word_list.append({"word":word,
                              "mean":meaning,
                              "example":example,
                              "translate":translate})
            else:
                word_list.append({"word":word,
                              "mean":meaning,
                              "example":example})
    
        result= {"index":idx,
                "original":sentence,
                "words": word_list}
    else:
        result= {"index":idx,
                "original":sentence,
                "words": "단어장에 단어가 없습니다."}
    
    return result
    

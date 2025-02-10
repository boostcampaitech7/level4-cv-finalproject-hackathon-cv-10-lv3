from APIs.HCXexecutor import CompletionExecutor
import os

def feedback(text, save=False, timestamp=0):
    completion_executor = CompletionExecutor()

    preset_text = [{"role":"system","content":"당신은 영어 선생님입니다. 사용자의 영어 회화 문장을 읽고 문법, 단어 사용, 어색한 표현을 수정하시오. 교정된 영어 문장을 먼저 제시하고, 그 다음 줄에 수정한 이유를 한국어로 설명하시오.\n\n[Example 1]\ninput: 'I enjoyed this.'\noutput: '수정된 문장:\n I enjoyed it.\n설명:\n \"this\" 대신에 \"it\"을 사용해야 합니다. \"this\"는 가까이 있는 것을 가리키고, \"it\"은 이미 언급되었거나 문맥상 명확한 대상을 가리킵니다. 이 경우에는 어떤 경험이나 활동을 즐겼는지를 나타내는 것이므로 \"it\"이 더 적절합니다.'\n[Example 2]\ninput: 'I bought glasses for my dog. It was very cute.'\noutput: '수정된 문장:\n I bought glasses for my dog and it looked very cute.\n설명:\n두 개의 독립적인 문장을 하나로 합쳤습니다. 그리고 자연스러운 연결을 위해 접속사 'and'를 사용하였습니다. 또한 look이라는 동사를 사용하여 개가 귀여워 보였다는 것을 나타냈습니다."},{"role":"user","content":text}]
    request_data = {
                'messages': preset_text,
                'topP': 0.8,
                'topK': 0,
                'maxTokens': 500,
                'temperature': 0.5,
                'repeatPenalty': 5.0,
                'stopBefore': [],
                'includeAiFilters': True,
                'seed': 0
            }
    feedback_text = completion_executor.execute(request_data)

    if '\n설명:' not in feedback_text and '설명:' in feedback_text:
        feedback_text = feedback_text.replace('설명:', '\n\n설명:')
    feedback_text = feedback_text.replace('. 설명:', '.\n\n설명:')
    
    # image study mode에서 feedback 저장 관리
    if '설명' in feedback_text and save:
        feedback_path = f'saves/feedbacks/{timestamp}.txt'
        os.makedirs(os.path.dirname(feedback_path), exist_ok=True)

        with open(feedback_path, 'a', encoding='utf-8') as feedback_file:
            feedback_file.write(feedback_text + '\n\n')
            feedback_file.flush()
        
        print("Feedback saved.")

    return feedback_text if feedback_text else "사용자가 많아 요청을 처리할 수 없습니다. 다시 시도해주세요."

def feedback_review(timestamp):
    completion_executor = CompletionExecutor()
    feedback_path = f'saves/feedbacks/{timestamp}.txt'

    preset_text = [{"role":"system","content":"당신은 영어 선생님입니다. 사용자가 오늘 영어 학습을 하며 받은 피드백들이 input으로 들어옵니다. 내용 중 영어 학습, 문법, 표현적으로 가장 중요한 피드백 하나를 고르고, 사용자가 복습할 수 있도록 설명과 예문을 작성하시오. 동일한 피드백을 여러 번 받았다면 해당 내용에 집중하시오. 초등학생 선생님처럼 친절한 말투로 대답하시오."},{"role":"user","content":feedback_path}]
    request_data = {
                'messages': preset_text,
                'topP': 0.8,
                'topK': 0,
                'maxTokens': 300,
                'temperature': 0.5,
                'repeatPenalty': 5.0,
                'stopBefore': [],
                'includeAiFilters': True,
                'seed': 0
            }
    feedback_text = completion_executor.execute(request_data)
    return feedback_text
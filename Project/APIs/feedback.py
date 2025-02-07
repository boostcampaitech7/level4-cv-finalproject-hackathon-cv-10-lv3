from APIs.HCXexecutor import CompletionExecutor

def feedback(text):
    completion_executor = CompletionExecutor()

    preset_text = [{"role":"system","content":"당신은 영어 선생님입니다. 사용자의 영어 회화 문장을 읽고 문법, 단어 사용, 어색한 표현을 수정하시오. 교정된 영어 문장을 먼저 제시하고, 뒤에 수정한 이유를 한국어로 설명하시오.\n[Example]\ninput: 'I enjoyed this.'\noutput: '수정된 문장: I enjoyed it.\n설명: \"this\" 대신에 \"it\"을 사용해야 합니다. \"this\"는 가까이 있는 것을 가리키고, \"it\"은 이미 언급되었거나 문맥상 명확한 대상을 가리킵니다. 이 경우에는 어떤 경험이나 활동을 즐겼는지를 나타내는 것이므로 \"it\"이 더 적절합니다.'"},{"role":"user","content":text}]
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

    return completion_executor.execute(request_data)

def feedback_for_diary(text):
    completion_executor = CompletionExecutor()

    preset_text = [{"role":"system","content":"당신은 영어 선생님입니다. 사용자의 영어 회화 문장을 읽고 문법, 단어 사용, 어색한 표현을 수정하시오.\n입력은 여러 개의 문장으로 들어옵니다. 줄글을 문장 단위로 분할하고, 한 문장씩 원래 영어 문장과 수정된 영어 문장을 번갈아가며 line by line으로 작성합니다.\n각 줄이 구분되도록 문장 앞에 '작성한 문장: ' 또는 '수정된 문장: '을 추가하시오."},{"role":"user","content":text}]
    request_data = {
                'messages': preset_text,
                'topP': 0.8,
                'topK': 0,
                'maxTokens': 800,
                'temperature': 0.5,
                'repeatPenalty': 5.0,
                'stopBefore': [],
                'includeAiFilters': True,
                'seed': 0
            }

    return completion_executor.execute(request_data)
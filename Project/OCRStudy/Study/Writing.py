import os
import json
from Project.APIs.user_input import get_user_input
from APIs.feedback import feedback

def writing_mode(timestamp):
    """
    Writing 모드: 문장 번역, 선택 및 답변 작성 후 피드백 제공
    
    """
    
    input_json = f"saves/save2_extracted{timestamp}.json"
    output_json = f"saves/save3_translation{timestamp}.json" # Use only Papago

    # 2. output_json에서 문장 선택 및 유저에게 선택된 문장 보여주기
    if not os.path.exists(output_json):
        print(f"Error: {output_json} 파일이 존재하지 않습니다.")
        return

    with open(output_json, "r", encoding="utf-8") as f:
        translations = json.load(f)

    print("번역된 문장 목록:")
    for idx, item in enumerate(translations):
        print(f"{idx + 1}. {item['translation']}")

    print("\n원하는 문장의 번호를 입력하세요 (1부터 시작):")
    try:
        selected_idx = int(input().strip()) - 1
        if selected_idx < 0 or selected_idx >= len(translations):
            print("잘못된 번호입니다. 프로그램을 종료합니다.")
            return
    except ValueError:
        print("잘못된 입력입니다. 프로그램을 종료합니다.")
        return

    selected_translation = translations[selected_idx]
    print(f"\n선택된 문장 (번역): {selected_translation['translation']}")

    # 3. 유저의 영어 답변 입력 받기
    print("\n선택된 문장에 대한 답변을 영어로 작성하세요:")
    user_answer = get_user_input()

    # 4. 선택한 문장의 원문 영어 문장 보여주기
    if os.path.exists(input_json):
        with open(input_json, "r", encoding="utf-8") as f:
            original_sentences = json.load(f)

        if selected_idx < len(original_sentences):
            original_sentence = original_sentences[selected_idx]
            print(f"\n선택한 문장의 원문 영어 문장: {original_sentence}")
        else:
            print("\n원문 영어 문장을 찾을 수 없습니다.")
    else:
        print(f"\n'{input_json}' 파일이 존재하지 않습니다.")

    # 5. 피드백 제공
    print("\n입력하신 답변에 대한 피드백을 제공합니다:")
    feedback(user_answer)

if __name__ == "__main__":
    # Writing 모드 실행
    writing_mode(timestamp)

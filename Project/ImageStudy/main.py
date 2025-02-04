from .Study.chat import chat
from .Study.diary import diary
import asyncio


# 1.image 촬영/불러오기
ImagePath='/data/ephemeral/home/clova/img/image1.jpg'

# 2.학습선택
while True:
    print("학습 방법을 선택하세요.")
    print("Chat-C, Diary-D, 종료-Q")
    StudyType = input().strip().lower()

    if StudyType=="c":
        chat(ImagePath)
    elif StudyType=='d':
        diary()
    elif StudyType=='q':
        print("학습을 종료합니다.")
        break
    else:
        print("잘못된 입력입니다.")

# async def main():
#     while True:
#         print("학습 방법을 선택하세요.")
#         print("Chat-C, Diary-D, 종료-Q")
#         StudyType = input().strip().lower()

#         if StudyType == "c":
#             await chat(ImagePath)
#         elif StudyType == 'd':
#             await diary()
#         elif StudyType == 'q':
#             print("학습을 종료합니다.")
#             break
#         else:
#             print("잘못된 입력입니다.")

# if __name__ == "__main__":
#     asyncio.run(main())
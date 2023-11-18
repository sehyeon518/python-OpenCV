import random
import os

array1 = ["정길", "정주", "다희", "세희", "세현"]
# random.shuffle(array1) # TODO 뽑는 순서도 바꾸고 싶으면 주석 해제하기
array2 = array1.copy()

random.shuffle(array2)

is_completed = True

while True:
    if(array1[0] == array2[0] or array1[1] == array2[1] or array1[2] == array2[2] or array1[3] == array2[3] or array1[4] == array2[4]):
        random.shuffle(array2)
    else:
        break

for i in range(5):
    os.system('clear')
    print(f"{array1[i]}(이)가 선물 줄 사람 확인하기 >> ENTER 입력")
    st = input()
    print(f"{array1[i]}(이)가 뽑은 사람은 {array2[i]}")
    print("다음 사람이 보지 못하게 엔터 한 번만 입력해주세요!!")
    st = input()
    os.system('clear')
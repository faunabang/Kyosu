import pyvts
import asyncio
import K8_movement as k8
import K6_makeAudio as k6
import re
import time

def start_lecture(script):
    myvts = pyvts.vts()
    asyncio.run(k8.connect_auth(myvts))


    # 강의 대본의 문장을 .?!()을 기준으로 분류
    sentences = re.split(r'(?<=[.?!])(?=\s)', script)
    sentences = [sentence for sentence in sentences if sentence]
    # print("sentences:",sentences)

    # 분류한 문장을 또 다시 단어 수준으로 분류
    for sentence in sentences:
        words = re.split(r'(?=\s)|(?<=\))', sentence)
        words = [word for word in words if word]
        # print("words:",words)
        # 단어가 표정이면 표정 변화
        for word in words:
            if word in ["(웃음)", "(감탄)", "(음미)", "(노려봄)", "(안타까움)"]:
                asyncio.run(k8.trigger(myvts, word))
                # print(word)
                words.remove(word)
            elif word in "[휴식]":
                time.sleep(1)
                # print(word)
                words.remove(word)
            else: # 단어마다 답변에 저장
                with open("texts/answer.txt", 'a', encoding='utf-8') as file:
                    # print(word)
                    file.write(word)

        combined_sentence = ''.join(words)
        k6.stream_audio(combined_sentence)
        print("comb:",combined_sentence)

        k8.asyncio.run(k8.trigger(myvts, "clear"))
        with open("texts/answer.txt", 'w', encoding='utf-8') as file:
            pass    


if __name__ == "__main__":
    scripts = ["(웃음)안녕하세요. 저는 제돌이입니다!","(노려봄)너는 누구야? 처음 보는 사람이네."]
    for script in scripts:
        start_lecture(script)
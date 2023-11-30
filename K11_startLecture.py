import pyvts
import asyncio
import K8_movement as k8
import K6_makeAudio as k6
import K9_makeSubtitle as k9
import re
import time

def start_lecture(script, myvts):

    # 강의 대본의 문장을 .?!()을 기준으로 분류
    sentences = re.split(r'(?<=[.?!])(?=\s)', script)
    sentences = [sentence for sentence in sentences if sentence]
    # print("sentences:",sentences)

    for sentence in sentences:
        sentence.replace('\n', '')

        feeling = ''.join(re.findall(r'\(.*?\)', sentence))
        sentence = re.sub(r'\(.*?\)', '', sentence)

        with open("texts/answer.txt", "w", encoding="utf-8") as outfile:
            words = sentence.split()
            lines = [words[i:i+5] for i in range(0, len(words), 5)]
            for line in lines:
                outfile.write(" ".join(line) + "\n")

        print("Feeling :",feeling)
        asyncio.run(k8.trigger(myvts, feeling))

        print("Kyosu :",sentence)
        k6.stream_audio(sentence)
        
        asyncio.run(k8.trigger(myvts, "clear"))
        with open("texts/answer.txt", 'w', encoding='utf-8') as f:
            f.truncate(0)


if __name__ == "__main__":
    print("!!! --------------- Allow Vtube Studio API --------------- !!!")
    myvts = pyvts.vts()
    asyncio.run(k8.connect_auth(myvts))
    scripts = ["(웃음)안녕하세요. 저는 제돌이입니다!","(노려봄)너는 누구야? 처음 보는 사람이네."]
    for script in scripts:
        start_lecture(script)
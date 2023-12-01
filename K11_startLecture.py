import pyvts
import asyncio
import K8_movement as k8
import K6_makeAudio as k6
import K9_makeSubtitle as k9
import re
import time

def start_lecture(script, myvts, vts_flag):

    # 강의 대본의 문장을 .?!()을 기준으로 분류
    sentences = re.split(r'(?<=[.?!])(?=\s)', script)
    sentences = [sentence for sentence in sentences if sentence]
    # print("sentences:",sentences)

    for sentence in sentences:
        sentence.replace('\n', '') # 문장에서 줄바꿈 제거

        feeling = ''.join(re.findall(r'\(.*?\)', sentence)) # 문장에서 감정 추출 후 저장
        sentence = re.sub(r'\(.*?\)', '', sentence) # 문장에서 감정 제거

        # OBS에 송출할 답변 텍스트 파일로 저장
        with open("texts/answer.txt", "w", encoding="utf-8") as outfile:
            words = sentence.split()
            lines = [words[i:i+5] for i in range(0, len(words), 5)]
            for line in lines:
                outfile.write(" ".join(line) + "\n")

        # 감정 Vtube Studio API 호출
        print("Feeling :",feeling)
        if vts_flag == True: asyncio.run(k8.trigger(myvts, feeling))

        # 강의 음성 출력
        print("Kyosu :",sentence)
        k6.stream_audio(sentence)
        
        if vts_flag == True: asyncio.run(k8.trigger(myvts, "clear")) # 감정 제거

        # 텍스트 초기화
        with open("texts/answer.txt", 'w', encoding='utf-8') as f:
            f.truncate(0)


if __name__ == "__main__":
    print("!!! --------------- Allow Vtube Studio API --------------- !!!")
    myvts = pyvts.vts()
    asyncio.run(k8.connect_auth(myvts))
    scripts = ["(웃음)안녕하세요. 저는 제돌이입니다!","(노려봄)너는 누구야? 처음 보는 사람이네."]
    for script in scripts:
        start_lecture(script)
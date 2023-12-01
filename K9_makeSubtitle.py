
def make_subtitle(chat, answer):
    # OBS에 송출할 답변 텍스트 파일로 저장
    with open("texts/answer.txt", "w", encoding="utf-8") as outfile:
        try:
            words = answer.split()
            lines = [words[i:i+5] for i in range(0, len(words), 5)]
            for line in lines:
                outfile.write(" ".join(line) + "\n")
        except:
            print("Error writing to answer.txt")

    # OBS에 송출할 질문 텍스트 파일로 저장
    with open("texts/chat.txt", "w", encoding="utf-8") as outfile:
        try:
            words = chat.split()
            lines = [words[i:i+6] for i in range(0, len(words), 6)]
            for line in lines:
                outfile.write(" ".join(line) + "\n")
        except:
            print("Error writing to chat.txt")


def generate_subtitle(chat_now, answer):
    # output.txt will be used to display the subtitle on OBS
    with open("texts/answer.txt", "w", encoding="utf-8") as outfile:
        try:
            words = answer.split()
            lines = [words[i:i+5] for i in range(0, len(words), 5)]
            for line in lines:
                outfile.write(" ".join(line) + "\n")
        except:
            print("Error writing to output.txt")

    # chat.txt will be used to display the chat/question on OBS
    with open("texts/selected_chat.txt", "w", encoding="utf-8") as outfile:
        try:
            words = chat_now.split()
            lines = [words[i:i+6] for i in range(0, len(words), 6)]
            for line in lines:
                outfile.write(" ".join(line) + "\n")
        except:
            print("Error writing to chat.txt")

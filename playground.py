from openai import OpenAI
from dotenv import load_dotenv;load_dotenv()

client = OpenAI()

prompt = []

prompt.append({"role": "user", "content": "안녕 나는 제돌이라고 해 만나서 반가워" })

response  = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=prompt,
            stream=True
            ) 

collected_messages = []

for chunk in response:
    chunk_message = str(chunk.choices[0].delta.content)
    collected_messages.append(chunk_message)
    print(chunk_message, end="", flush=True)

print("\n",collected_messages)
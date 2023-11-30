from openai import OpenAI
import K1_VectorDB as k1
import K2_ChatDbFun as k2
import os
from datetime import datetime
from dotenv import load_dotenv;load_dotenv()

def conversation( vectorDB_folder="", query="", token=""):

    client = OpenAI()
    chat_history=k2.query_history(token) # 기존 대화 내용
    # print("chat_history=",chat_history)
    # answer="" 
    # new_chat=""
          
    index_path = os.path.join(vectorDB_folder, "index.faiss")
    page_content_path = os.path.join(vectorDB_folder, "page.pkl")

    vectorDB = k1.VectorDB(index_path, page_content_path)

    docs = vectorDB.similarity_search(query, cnt=6)
    prompt=[]
    
    for page in docs:    
        prompt.append({"role": "system", "content": f"{ page }"})
        
    prompt.append({"role": "system", "content": f"""
                        위 내용은 강의에 사용한 교재이다.
                        너는 강사이고, 교재의 내용을 바탕으로 수강자가 이해하기 쉽도록 질문에 간결히 답변한다.
                        """})

    # prompt=chat_history + prompt 
        
    prompt.append({"role": "user", "content": query } )    
    
    response  = client.chat.completions.create(
                        model="gpt-4-1106-preview",
                        messages=prompt
                        ) 
    #print("response.choices[0].message=",response)
    answer= response.choices[0].message.content
    
    new_chat=[{"role": "user", "content": query },{"role": "assistant", "content":answer}]  

    answer_no_update = any( chat["content"] == answer  for chat in chat_history)
    checkMsg=["죄송합니다","확인하십시요","OpenAI","불가능합니다","미안합니다.","않았습니다"]
    for a in checkMsg: 
        if a in answer:
           answer_no_update=True
           break
                
    # 새로운 대화 내용을 업데이트
    if not answer_no_update:
        k2.update_history(token, new_chat, max_token=3000)
    return answer  

if __name__ == "__main__":

    k2.setup_db()
    token = "abcdefghij"

    today = str(datetime.now().date().today())
    print( f"vectorDB-faiss-{today}")
    vectorDB_folder = f"vectorDB-faiss-{today}"
    k1.vectorDB_create(vectorDB_folder, "files/kinetic_theory_of_gases.pdf")

    answer = conversation(vectorDB_folder, "기체분자운동론이 뭔가요", token)
    print(answer)
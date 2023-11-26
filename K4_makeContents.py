import K1_VectorDB as vec
from openai import OpenAI
import K3_GuitarFun as fun
import os
import datetime
from dotenv import load_dotenv;load_dotenv()

def makeContents( vectorDB_folder="", pdf_file=""):

    client = OpenAI()
    contents=""
            
    index_path = os.path.join(vectorDB_folder, "index.faiss")
    page_content_path = os.path.join(vectorDB_folder, "page.pkl")

    vectorDB = vec.VectorDB(index_path, page_content_path)

    docs = vectorDB.similarity_search(query, cnt=6)
    prompt=[]

    prompt.append({"role": "system", "content": f"""
                        너는 주어질 교재의 내용을 분석하고, 분석한 내용을 바탕으로 강의를 하기 위한 강의의 목차를 생성한다.
                        강의의 목차는 교재의 내용을 분석하여 
                        강
                        """})

    for page, distance in docs:
        prompt.append({"role": "system", "content": f"{ page }"})
        print(f"{page}\n\n")
        # print( "{}\n".format(distance),"="*100, page.replace('\n', ''))
    
    prompt.append({"role": "user", "content": "우리학교 이름은" } )    
    prompt.append({"role": "assistant", "content": "제주과학고입니다." } )
        
    prompt.append({"role": "user", "content": f"위 교재의 이름은 {pdf_file}이야. " } )

    
    response  = client.chat.completions.create(
                        model="gpt-4-1106-preview",
                        messages=prompt
                        ) 
    #print("response.choices[0].message=",response)
    contents= response.choices[0].message.content

    return contents       


if __name__ == "__main__":
    today = str( datetime.now().date().today())
    print( f"vectorDB-faiss-{today}")

    vectorDB_folder = f"vectorDB-faiss-{today}"
    vec.vectorDB_create(vectorDB_folder)
      
    contents = makeContents(vectorDB_folder, "files/chemi_1.pdf")

    print(f"contents: {contents}")
from openai import OpenAI
import K3_GuitarFun as fun
import os
import pdfplumber
from datetime import datetime
from langchain.text_splitter import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv;load_dotenv()

def makeContents(file_path):

    file_name = file_path.split("/")[1]
    documents = []

    with pdfplumber.open(file_path) as pdf_document:
        for page_number, page in enumerate(pdf_document.pages):
            text = page.extract_text()

            metadata = {
                'source': file_name,
                'page': page_number + 1
            }
            document= Document(page_content=text, metadata=metadata)
            documents.append(document)
    print(f"{file_name}  ----- load !")


    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size =3000,
            chunk_overlap =0,
            separators=["\n\n","\n",", "],
            length_function=len
    )
    
    pages = text_splitter.split_documents(documents)
    # fun.splitter_pages_viewer(pages)
    # quit()


    client = OpenAI()
    prompt=[]

    prompt.append({"role": "system", "content": f"""
                        너는 역할은 주어질 교재의 내용을 분석하고, 분석한 내용을 바탕으로 강의를 하기 위한 강의의 목차를 생성하는 것이다.
                        강의의 목차는 교재의 내용을 분석하여 교재 내에서의 목차를 참고하여 생성한다.
                        교재의 파일명은 {file_name}이다.
                        답변은 부가적인 설명 없이 목차만 작성한다.
                        목차는 줄바꿈을 기준으로 나눈다.
                        목차의 순서는 표시하지 않고, 목차 내용만 작성한다.
                        목차 내용은 해당 목차 내에 있는 교재의 내용을 포괄하는 문장형식으로 작성한다.
                        다음은 교재의 내용이다.
                        """})

    for page in pages:
        prompt.append({"role": "system", "content": f"{ page }"})
        print(f"{page}\n\n")
        # print( "{}\n".format(distance),"="*100, page.replace('\n', ''))
    
    prompt.append({"role": "user", "content": "위 교재의 내용을 분석하여 해당 교재로 강의할 강의의 목차를 생성해줘." } )    
    # prompt.append({"role": "assistant", "content": "" } )

    
    response  = client.chat.completions.create(
                        model="gpt-4-1106-preview",
                        messages=prompt
                        ) 
    #print("response.choices[0].message=",response)
    contents= response.choices[0].message.content

    return contents


if __name__ == "__main__":

    file_path = "files/kinetic_theory_of_gases.pdf"
    contents = makeContents(file_path)

    print(f"contents: {contents}")


    # 목차 저장
    file_name = file_path.split("/")[1].split(".")[0]
    contents_id = fun.rnd_str()
    contents_name = f"{file_name}-{contents_id}.txt"

    today = str(datetime.now().date().today())
    folder_path = f"contents\{file_name}-{today}"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    full_file_path = os.path.join(folder_path, contents_name)

    with open(full_file_path, 'w', encoding='utf-8') as file:
        file.write(contents)

    print(f"\n'{full_file_path}'에 텍스트 저장 완료")
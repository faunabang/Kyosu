from openai import OpenAI
import K3_GuitarFun as fun
import os
import pdfplumber
from datetime import datetime
from langchain.text_splitter import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from dotenv import load_dotenv;load_dotenv()

def makeScripts(pdf_path, contents_id):

    # loader = TextLoader(text_path, encoding='utf-8')
    # page=loader.load()[0]

    # documents1=[ Document(
    #                     page_content=page.page_content,
    #                     metadata=page.metadata
    #                     )
    #            ]
    # print(f" ----- load !")


    file_name = pdf_path.split("/")[1]
    documents2 = []

    with pdfplumber.open(pdf_path) as pdf_document:
        for page_number, page in enumerate(pdf_document.pages):
            text = page.extract_text()

            metadata = {
                'source': file_name,
                'page': page_number + 1
            }
            document= Document(page_content=text, metadata=metadata)
            documents2.append(document)
    print(f"{file_name}  ----- load !")


    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size =3000,
            chunk_overlap =0,
            separators=["\n\n","\n",", "],
            length_function=len
    )
    
    # pages1 = text_splitter.split_documents(documents1)
    pages2 = text_splitter.split_documents(documents2)
    # fun.splitter_pages_viewer(pages)
    # quit()

    contents = []
    today = str(datetime.now().date().today())
    file_name = file_path.split("/")[1].split(".")[0]

    # 목차 불러오기
    with open(f"contents\{file_name}-{today}\{file_name}-{contents_id}.txt", 'r', encoding='utf-8') as file:
        for line in file:
            contents.append(line.strip())
    print(contents)

    client = OpenAI()
    prompt=[]

    prompt.append({"role": "system", "content": f"""
                        너의 이름은 Kyosu이며, 너는 AI로 강의 대본을 작성하고 직접 강의한다.
                        너는 역할은 주어질 교재의 내용을 분석하고, 주어질 강의 목차를 바탕으로 강의를 하기 위한 강의의 대본을 작성하는 것이다.
                        답변은 부가적인 설명 없이 강의 대본만 작성한다.
                        강의 대본은 구체적인 예시를 들어 수강자가 잘 이해할 수 있도록 작성한다.
                        수식 작성은 되도록 피하며, 교재에 있는 개념을 확실하게 전달할 수 있도록 작성한다.
                        강의가 지루하지 않도록 강의 대본은 친근한 말투로 작성하며, 중간중간 잠시 숨 돌릴 시간을 갖고, 농담도 섞어서 강의 대본을 작성한다.
                        강의 대본 중간중간에 강사가 지을 표정을 작성한다.
                        표정은 다음 리스트에 있는 것 중 한 가지를 선택하여 (표정)과 같은 형태로 작성한다.
                        표정 리스트 = [웃음, 안타까움, 감탄, 노려봄, 음미]
                        교재의 파일명은 {file_name}이다.
                        다음은 교재의 내용이다.
                        """})

    for page in pages2:
        prompt.append({"role": "system", "content": f"{ page }"})
        print(f"{page}\n\n")

    prompt.append({"role": "system", "content": f"""
                        위는 교재의 내용이다. 교재의 내용을 분석하여 교재 중심으로 강의 대본을 작성한다.
                        다음은 강의의 전체 목차이다. 해당 목차의 순서로 강의 대본을 작성한다.
                        """})
    
    for content in contents:
        prompt.append({"role": "system", "content": f"{ content }"})
        print(f"{page}\n\n")

    prompt.append({"role": "system", "content": f"""
                        위는 강의의 전체 목차를 순서대로 나열한 것이다.
                        각 목차의 강의가 끝날 때마다 잠시간 질문 시간을 가지며, 질문 시간이 끝나면 바로 다음 목차의 강의를 시작한다.
                        첫 목차의 강의 대본의 시작부분에는 첫인사와 강의를 시작하며 수강자를 격려하는 말을 작성한다.
                        마지막 목차의 강의 대본의 끝부분에는 끝인사와 강의를 맺으며 수강자를 격려하는 말을 작성한다.
                        """})

    scripts = []

    for content in contents:
        prompt.append({"role": "user", "content": f"교재의 내용을 바탕으로 강의의 목차 {content}에 해당하는 강의 대본을 작성해줘." } )    
        # prompt.append({"role": "assistant", "content": "" } )

        response  = client.chat.completions.create(
                            model="gpt-4-1106-preview",
                            messages=prompt
                            ) 
        
        scripts.append(response.choices[0].message.content)
        prompt.append(response.choices[0].message)
        print("\n\n", response.choices[0].message.content, "\n\n")

    return scripts

if __name__ == "__main__":

    file_path = "files/kinetic_theory_of_gases.pdf"
    id = "d62ta"
    scripts = makeScripts(file_path, id)

    print(f"scripts: {scripts}")


    # 강의 대본 저장
    file_name = file_path.split("/")[1].split(".")[0]

    today = str(datetime.now().date().today())
    folder_path = f"scripts\{file_name}-{today}"
    folder2_path = f"scripts\{file_name}-{today}-{id}"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    if not os.path.exists(folder2_path):
        os.makedirs(folder2_path)

    for i in range(len(scripts)):
        scripts_name = f"scripts-{file_name}-{id}-{i+1}.txt"
        full_file_path = os.path.join(folder2_path, scripts_name)

        with open(full_file_path, 'w', encoding='utf-8') as file:
            file.write(scripts[i])

        print(f"\n'{full_file_path}'에 텍스트 저장 완료")
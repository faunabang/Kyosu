import numpy as np
import faiss
import pickle
import os
from datetime import datetime
from openai import OpenAI
import pdfplumber
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.document_loaders import WebBaseLoader,UnstructuredURLLoader
from langchain.chat_models import ChatOpenAI
from langchain.memory import ChatMessageHistory
from dotenv import load_dotenv;load_dotenv() # openai_key  .env 선언 사용 
import K3_GuitarFun as fun
import K2_ChatDbFun as chatDB


class VectorDB:

    def __init__(self, index_path, page_content_path):
        self.index = faiss.read_index(index_path)
        with open(page_content_path, 'rb') as f:
            self.page_contents = pickle.load(f)


    def similarity_search(self, query, cnt=3):
        query_embedding = create_query_embedding(query) 
        D, I = self.index.search(query_embedding, cnt)  # D는 거리, I는 인덱스

        # 결과를 거리에 따라 정렬합니다.
        results = zip(I.flatten(), D.flatten())  # flatten 결과 리스트
        sorted_results = sorted(results, key=lambda x: x[1])  # 거리에 따라 정렬
        
        # 정렬된 결과로부터 유사한 문서 추출
        search_results = []
        
        for idx, distance in sorted_results:
            if idx < len(self.page_contents):  # 유효한 인덱스인지 확인
                search_results.append((self.page_contents[idx], distance))
        
        return search_results
    


def create_query_embedding(query):
    # OpenAI API를 사용하여 쿼리의 임베딩을 생성합니다.
    client = OpenAI()
    response = client.embeddings.create(
        input=query,
        model="text-embedding-ada-002"
    )
    embedding_vector = response.data[0].embedding  # This is the corrected line
    return np.array(embedding_vector).astype('float32').reshape(1, -1)  # 2D array 형태로 반환합니다.  
   

def vectorDB_create(vectorDB_folder, text_file, pdf_file):

    loader = TextLoader(text_file, encoding='utf-8')
    page=loader.load()[0]
    documents=Document(page_content=page.page_content, metadata=page.metadata)
    print(f"{text_file}  ----- load !")


    with pdfplumber.open(pdf_file) as pdf_document:
        for page_number, page in enumerate(pdf_document.pages):
            text = page.extract_text()

            metadata = {
                'source': 'chemi_1.pdf',
                'page': page_number + 1
            }
            document = Document(page_content=text, metadata=metadata)
            documents.append(document)
    print(f"{pdf_file}  ----- load !")


    #  읽은 문서 페이지 나눔 방볍 설정 -----------------------------------
    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size =3000, # 이 숫자는 매우 중요
            chunk_overlap =0, # 필요에 따라 사용
            separators=["\n\n","\n",", "], # 결국 페이지 분리를 어떻게 하느냐 가 답변의 질을 결정
            length_function=len    
            # 위 내용을 한 페이지를 3000자 이내로 하는데 페이 나누기는 줄바꿈표시 2개 우선 없음 1개로 3000자를 체크하는 것은 len 함수로 
    )
    
    #  읽은 문서 페이지 나누기 -----------------------------------
    pages = text_splitter.split_documents(documents)
    # fun.splitter_pages_viewer(pages)
    # quit()
    
    
    # 신버전
    client = OpenAI()  
    ## 각 페이지에 대한 임베딩을 담을 리스트
    embeddings_list = []
    # 임베딩 생성을 위해 각 페이지에 대해 반복
    for page in pages:
        # print(page.page_content)
        response = client.embeddings.create(
            input=page.page_content,
            model="text-embedding-ada-002"
        )
        
        embedding_vector = response.data[0].embedding  # This is the corrected line
        embeddings_list.append(np.array(embedding_vector).astype('float32').reshape(1, -1))
        

    # FAISS 인덱스 초기화 (전체 임베딩 리스트의 첫 번째 요소를 사용하여 차원을 설정)
    dimension = len(embeddings_list[0][0])  # Get the dimension from the first embedding's length
    index = faiss.IndexFlatL2(dimension)  # Initialize the FAISS index


    # Add the embeddings to the FAISS index
    for embedding in embeddings_list:
        index.add(embedding)  # Each embedding is already a 2D numpy array
    # faiss.write_index(index, vectorDB_folder)
    if not os.path.exists(vectorDB_folder):
        os.makedirs(vectorDB_folder)

    faiss.write_index(index, f"{vectorDB_folder}/index.faiss")
    page_contents = [page.page_content for page in pages]
    with open(f"{vectorDB_folder}/page.pkl", "wb") as f:
        pickle.dump(page_contents, f)

    print("Page FAISS 인덱스가 성공적으로 저장되었습니다.")
    
    return  vectorDB_folder
      

if __name__ == "__main__":
    today = str( datetime.now().date().today())
    print( f"vectorDB-faiss-{today}")

    vectorDB_folder = f"vectorDB-faiss-{today}"
    vectorDB_create(vectorDB_folder, "files\\chemi_1.pdf")
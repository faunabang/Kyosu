import os
import requests
import random
import string
from datetime import datetime
import re
import time
import asyncio
import pyvts
from transformers import GPT2Tokenizer
from langchain.text_splitter import Document
import K6_makeAudio as k6
import K8_movement as k8

tokenizer = None

def tiktoken_len(text):
    global tokenizer
    if tokenizer is None:
        tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    tokens = tokenizer.tokenize(text)
    return len(tokens)

def page_content_append(oldChat="",newChat="",sourece=""):
       
       page_content=oldChat+ ' \n' + newChat if oldChat!="" else newChat
            
       return Document( page_content=page_content ,metadata={'source': sourece})
       
       
                    

def image_url_to_save(image_url, folder_name="", image_name=""):
   # 이미지 저장  
    if image_url    =="" :  return False
    if folder_name  =="":  folder_name="." 
    if image_name   =="":   image_name ="image-" + rnd_str(5,"n") +".jpg"
    if not os.path.exists(folder_name):   os.makedirs(folder_name)
 
    response = requests.get(image_url)

    file_path = os.path.join(folder_name, image_name)

    file=open(file_path, "wb")

    file.write(response.content)
    return True

    
def rnd_str(n=5, type="ns"):
    if type == "n":
        characters = string.digits
    elif type == "s":
        characters = string.ascii_letters
    else:  # "ns" 또는 기타
        characters = string.digits + string.ascii_letters
    return ''.join(random.choices(characters, k=n))



def remove_words(text="",remove_words=["게시", "안내"] ):
    # remove_words 문자열 제거 
    words = text.split()
    filtered_words = [word for word in words if not any(remove_word in word for remove_word in remove_words)]
    return ' '.join(filtered_words)

def get_text_after_words( text="",start_str="",end_str="",re=""):

    start_index = text.find(start_str)
    end_index = text.find(end_str)

    if start_index != -1 and end_index != -1:
        text = text[start_index:end_index]
    else:
        if start_index != -1:
            text = text[start_index]
        else:
            if  re =="" :
                text="데이터 없음!"  
            else:
                text= text
    return text


def html_parsing_text(page_content="",start_str="",end_str="",length=20,removeword=[]):

    page_content = re.sub("\n+", "\n", page_content)
    page_content = re.sub("\s+", " ", page_content)
    page_content=remove_words(text=page_content,remove_words=["게시","안내"])
    page_content=get_text_after_words(text=page_content,start_str=start_str,end_str=end_str)
    parts = page_content.split(" ")  # 공백을 기준으로 문자열 분리
    newStr=""
    for s in parts:

        if len(s)< length :
        #   s=s.replace("\n"," ")
          newStr += s +" "  
    return newStr +"\n\n"

def loader_documents_viewer(documents):

    print(documents)
    print("="*100)
    print("Page Content:\n", documents[0].page_content)
    print("\nMetadata:", documents[0].metadata)

def splitter_pages_viewer(pages):
    print("="*100)
    print("pages = ", len(pages) )
    print("-"*100)
    for index,page  in enumerate(pages):
         print( "{:02d} {}".format(index+1, tiktoken_len(page.page_content)), page.page_content.replace('\n', ''), page.metadata['source'])

    print("="*100)
        

if __name__ == "__main__":
    print("")
    
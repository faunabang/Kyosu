import K1_VectorDB as k1
import K2_ChatDbFun as k2
import K3_GuitarFun as k3
import K4_makeContents as k4
import K5_makeScripts as k5
import K6_makeAudio as k6
import K7_makeImage as k7
import K8_movement as k8
import K9_makeSubtitle as k9
import K10_conversation as k10
from K11_startLecture import *
from datetime import datetime
import os
import time
import pyvts
import asyncio

def main():

    while True:
        mode = input("\nselect mode(1: make scripts | 2: start lecture | 0: close) : ")
        if mode == "1":
            lecture_name = input("make lecture's name : ") # 만들 강의 이름 입력
            directory_path = 'files'
            files = []

            # 강의 교재 파일 불러오기
            for item in sorted(os.listdir(directory_path)):
                full_path = os.path.join(directory_path, item)
                if os.path.isfile(full_path):
                    files.append(item)
            
            # 강의 교재 파일 리스트 출력
            print("\nfile list:")
            for i in range(len(files)):
                print(f"{i+1}: {files[i]}")
            
            # 강의 교재 파일 선택
            file = files[int(input("\nselect lecture's file : "))-1] # "files/kinetic_theory_of_gases.pdf"
            print("selected file :", file)
            file_path = f"files/{file}"

            print("\n--------------- start making vectorDB ---------------\n")

            today = str(datetime.now().date().today())
            print( f"vectorDB-faiss-{today}")

            vectorDB_folder = f"vectorDB-faiss-{today}"
            k1.vectorDB_create(vectorDB_folder, file_path)

            print("\n--------------- start making contents ---------------\n")

            contents = k4.makeContents(file_path)
            k4.save_contents(contents, lecture_name)

            print("\n--------------- start making scripts ---------------\n")

            scripts = k5.makeScripts(file_path, lecture_name)
            k5.save_scripts(scripts, file_path, lecture_name)
                        
        elif mode == "2":
            scripts = []
            lecture_name = input("input lecture's name : ") # 사전에 제작한 강의 이름 입력
            directory = f"scripts/{lecture_name}" # 강의 이름에 맞는 경로 설정

            # 강의 이름에 해당하는 폴더가 없으면 강의 이름 재입력
            while not os.path.exists(directory):
                lecture_name = input("input correct lecture's name : ")
                directory = f"scripts/{lecture_name}"
            
            # 강의 정보 불러오기
            with open(f"{directory}/information.txt", 'r', encoding='utf-8') as file:
                information = file.read()
            
            # 강의 대본 불러오기
            directory = f"{directory}/texts"
            for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path) and file.endswith('.txt'):
                    with open(file_path, 'r', encoding='utf-8') as file:
                        scripts.append(file.read())

            print(f"\n{information}") # 강의 정보 출력
            # print(scripts) # 강의 대본 출력

            print("\n--------------- ready to start lecture ---------------\n")

            terminal_input = input("want to start lecture? (Y/n): ") # 강의 시작 여부 질문
            if terminal_input.lower() == "y":
                
                print("\n------------------ lecture started ------------------\n")
                
                myvts = pyvts.vts()
                if input("want to use Vtube Studio? (Y/n): ").lower() == "y" : # Vtube Studio 사용 여부 질문
                    vts_flag = True
                    print("!!!  Allow Vtube Studio API  !!!")
                    asyncio.run(k8.connect_auth(myvts))
                else: vts_flag = False
                
                for script in scripts:
                    start_lecture(script, myvts, vts_flag) # 각 목차별 강의 시작
                    print("one script finished")

                print("\n--------------- lecture Finished ---------------\n")

            else: print("\n-------------------- Stopped --------------------\n")
        
        elif mode == "0": break

        else:
            print("wrong input")

if __name__ == "__main__":
    main()
    print("\n종료")
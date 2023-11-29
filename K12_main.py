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
            lecture_name = input("make lecture's name : ")
            directory_path = 'files'
            files = []
            for item in sorted(os.listdir(directory_path)):
                full_path = os.path.join(directory_path, item)
                if os.path.isfile(full_path):
                    files.append(item)
            print("\nfile list:")
            for i in range(len(files)):
                print(f"{i+1}: {files[i]}")
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
            lecture_name = input("input lecture's name : ")
            directory = f"scripts/{lecture_name}"

            while not os.path.exists(directory):
                lecture_name = input("input correct lecture's name : ")
                directory = f"scripts/{lecture_name}"
            
            with open(f"{directory}/information.txt", 'r', encoding='utf-8') as file:
                information = file.read()
            
            directory = f"{directory}/texts"
            for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path) and file.endswith('.txt'):
                    with open(file_path, 'r', encoding='utf-8') as file:
                        scripts.append(file.read())

            print(f"\n{information}")
            # print(scripts)

            print("\n--------------- ready to start lecture ---------------\n")

            terminal_input = input("want to start lecture? (Y/n): ")
            if terminal_input.lower() == "y":
                
                print("\n------------------ lecture started ------------------\n")
                print("!!! --------------- Allow Vtube Studio API --------------- !!!")
                myvts = pyvts.vts()
                asyncio.run(k8.connect_auth(myvts))
                for script in scripts:
                    start_lecture(script, myvts) # 각 목차별 강의 시작
                    print("111111111111111111111111111111111111111111111111")

                print("\n--------------- lecture Finished ---------------\n")

            else: print("\n-------------------- Stopped --------------------\n")
        
        elif mode == "0": break

        else:
            print("wrong input")

if __name__ == "__main__":
    main()
    print("\n종료")
import K1_VectorDB as k1
import K2_ChatDbFun as k2
import K3_GuitarFun as k3
import K4_makeContents as k4
import K5_makeScripts as k5
import K6_makeAudio as k6
import K7_makeImage as k7
import K8_movement as k8
import K9_makeSubtitle as k9
import datetime
import os

# id = "d62ta"
id = k3.rnd_str()
today = str(datetime.now().date().today())
file_path = "files\kinetic_theory_of_gases.pdf" # 파일 경로 -----------------------------

contents = k4.makeContents(file_path)
k4.save_contents(contents, file_path, id)

scripts = k5.makeScripts(file_path, id)
k5.save_scripts(scripts, file_path, id)


from flask import Flask, request, abort, render_template, send_from_directory, jsonify, session
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
import K11_startLecture as k11
import threading
import pyvts
app = Flask(__name__)

app.secret_key = 'GTalkStory'

def main():
    # # id = "d62ta"
    # id = k3.rnd_str()
    # file_path = "files/kinetic_theory_of_gases.pdf" # 파일 경로 -----------------------------

    # contents = k4.makeContents(file_path)
    # k4.save_contents(contents, file_path, id)

    # scripts = with open
    # scripts = k5.makeScripts(file_path, id)
    # k5.save_scripts(scripts, file_path, id)

    # print("\n--------------- ready to start lecture ---------------\n")
    
    scripts = ["(웃음)안녕하세요. 저는 제돌이입니다!","(노려봄)너는 누구야? 처음 보는 사람이네."] # 예시 scripts
    for script in scripts:
        k11.start_lecture(script)
        k10.conversation()

    print("--------------- lecture Finished ---------------")


@app.route('/')
def home():
    if 'token' not in session:
        session['token'] = k3.rnd_str(n=20, type="s")
    return render_template("/html/index.html", token=session['token'])

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('templates/files', filename, as_attachment=True)

@app.errorhandler(404)
def not_found(e):
    return render_template('/html/404.html'), 404

@app.route('/<path:page>')
def page(page):
    if 'token' not in session:
        session['token'] = k3.rnd_str(n=20, type="s")

    if ".html" in page:
       return render_template(page, token=session['token'])
    else:
       return send_from_directory("templates", page)

# AI 쿼리 경로
@app.route("/query", methods=["POST"])
def query():
    
    query = request.json.get("query")
    
    with open("texts\chat.txt", "w", encoding="utf-8") as outfile:
        try:
            outfile.write(query)
        except:
            print("Error writing to chat.txt")


if __name__ == "__main__":
    try:
        main = threading.Thread(target=main)
        main.start()
        app.run(ssl_context=('openSSL/cert.pem', 'openSSL/key.pem'), debug=True, port=5001)
    except KeyboardInterrupt:
        main.join()
        print("Stopped")
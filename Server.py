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
import K12_main as k12
import threading
from datetime import datetime
import os
import time
app = Flask(__name__)
app.secret_key = 'GTalkStory'

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

    print("1111111111111111111111111111111111111111111111111")
    query = request.json.get("query")
    today = str(datetime.now().date().today())
    vectorDB_folder = f"vectorDB-faiss-{today}"
    token = "dhxzZUwGDzdhGrBTMSMs2" # 예시 토큰

    answer = k10.conversation(vectorDB_folder, query, token)
    k9.make_subtitle(query, answer)
    k6.stream_audio(answer)

    time.sleep(1)



if __name__ == "__main__":
    try:
        if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
            main = threading.Thread(target=k12.main)
            main.start()
            
        app.run(ssl_context=('openSSL/cert.pem', 'openSSL/key.pem'), debug=True, port=5001)
        
    except KeyboardInterrupt:
            main.join()
            print("\n--------------- Stopped ---------------\n")
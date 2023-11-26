from flask import Flask, request, abort, render_template, send_from_directory, jsonify, session
import os
import K1_VectorDB as vec
from datetime import datetime
import K3_GuitarFun as jshs
import K2_ChatDbFun as chatDB
from dotenv import load_dotenv

load_dotenv()  # openai_key .env 선언 사용
# print( os.getenv('OPENAI_KEY')) 
app = Flask(__name__) 
chatDB.setup_db()
app.secret_key = 'jedolstory'

# 오류 핸들러
@app.errorhandler(404)
def not_found(e):
    return render_template('/html/404.html'), 404

# 루트 경로
@app.route("/")
def index():
    if 'token' not in session:
        session['token'] = jshs.rnd_str(n=20, type="s")
        print(f"New token generated: {session['token']}")
    else:
        print(f"Existing token found: {session['token']}")
    return render_template("/html/index.html", token=session['token'])

# 페이지 경로
@app.route('/<path:page>')
def page(page):
    print(f"Page request: {page}")
    try:
        if ".html" in page:
            return render_template(page)
        else:
            return send_from_directory("templates", page)
    except Exception as e:
        print(f'Error serving page {page}: {e}', exc_info=True)
        abort(404)

# AI 쿼리 경로
@app.route("/query", methods=["POST"])
def query():
    
    #return jsonify({"answer": '제돌이 공부 중입니다. 14시 ~ 15시까지'})
    query = request.json.get("query")
    
    today = str(datetime.now().date().today())
    vectorDB_folder = f"vectorDB-faiss-jshs-{today}"

    
    if os.path.exists(vectorDB_folder) and os.path.isdir(vectorDB_folder):
      print(" used  vectorDB_folder ")
    else:
        print(" vectorDB_folder = ", vectorDB_folder )
        vectorDB_folder=vec.vectorDB_create(vectorDB_folder)
        print(" vectorDB_folder ok ")
       

    print(f"User token: {session['token']}, Query: {query}")
    try:
        answer = vec.ai_response(
            vectorDB_folder=vectorDB_folder,
            query=query,
            token=session['token']
        )
    except Exception as e:
        print(f'Error in query processing: {e}')
        answer = f"{e}"
    
        
    print(f"Answer: {answer}")
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)

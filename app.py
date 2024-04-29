from flask import Flask, jsonify, Blueprint, send_from_directory
from flask import render_template, request, render_template_string
from flask_cors import CORS
from db import HtmlFileManager
from flask import abort
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import cross_origin
#cmd : export FLASK_DEBUG=1
# flask run --port=8001 --host="0.0.0.0"
import json
PORT = 8001
# PORT = 5000
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 # 정적 파일 캐시 비활성화
CORS(app)
# CORS(app, resources={r"/api/*": {"origins": "*"}}) 


@app.route("/isCrawlingByUrl", methods=["GET"])
def getIsCrawlingByUrl() :

    args_dict = request.args.to_dict()
    url : str = args_dict.get("url")
    if url == None :
        abort(404)
    
    dbHtml = HtmlFileManager() # 싱글톤
    isCrawling : bool = dbHtml.getIsCrawlingUrl(url)
    data : dict = {"isCrawling" : isCrawling}
    
    return jsonify(data), 200

@app.route("/isCrawlingByTitle", methods=["GET"])
def getIsCrawlingByTitle() :
    args_dict = request.args.to_dict()
    title : str = args_dict.get("title")
    
    dbHtml = HtmlFileManager() # 싱글톤
    isCrawling : bool = dbHtml.getIsCrawlingUrl(title)
    data : dict = {"isCrawling" : isCrawling}
    # print( isCrawling )
    
    return jsonify(data)


@app.route("/postData", methods=["POST"])
def postData() :
    data = request.get_json()

    # JSON 데이터에서 필요한 값을 추출
    origin_url = data.get("origin_url")
    parameter = data.get("parameter")
    title = data.get("title")
    url = data.get("url")
    domain = data.get("domain")
    HTML = data.get("HTML")
    wordlist = data.get("wordlist")
    isCrawling = data.get("isCrawling")
    
    # print(data)
    
    try :
        wordlist = wordlist.strip("[]")
        wordlist = [word.strip(" '").strip(" \"") for word in wordlist.split(', ')]
    except :
        print("에러")
        abort(404)
        
    # print()
    # print( wordlist )
    # print( type(wordlist) )
        

    # isCrawling = True
    if url == None :
        abort(404)
    
    dbHtml = HtmlFileManager()
    
    isSuccessful : bool = dbHtml.insertIntoTable(origin_url, parameter, title,
                                        url, domain, HTML, wordlist, isCrawling)
    
    data : dict = {"isSuccessful" : isSuccessful}
    if isSuccessful == False :
        return jsonify(data), 404
    
    return jsonify(data), 200

@app.route("/getLast10Data", methods=["Get"])
def getLast10Data() :
    dbHtml = HtmlFileManager() # 싱글톤
    data : list = dbHtml.getLastAllSelect(10)
    
    if data == None or len(data) == 0:
        return abort(404)
    
    return jsonify(data), 200


@app.route('/')
def homepage():
    with open('./site/viewer.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    return render_template_string(html_content)
    
    
# ==== swagger 설정 서버 동작과 상관 없음 ====
SWAGGER_URL =  "/api/docs"
API_URL = "/api/docs/swagger.json"
swaggerui_blueprint = get_swaggerui_blueprint( 
    SWAGGER_URL,
    API_URL,
    config = {
        'app_name' : "Test Craling db application"
    },
)

@app.route("/api/docs/swagger.json")
@cross_origin()  # 이 라우트에 대해 CORS 허용
def send_swagger_json():
    # print("file")
    response = send_from_directory('api/docs', 'swagger.json')
    # 브라우저가 캐시 사용하는 것을 막음
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
# ==== 경계선 ====

if __name__ =="__main__" :
    app.run(host='0.0.0.0', port=PORT)



    
    
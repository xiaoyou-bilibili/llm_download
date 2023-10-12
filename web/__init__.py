from flask import Flask, request, Response, render_template
from agent.source.google import GoogleSpider
import json
from base import GOOGLE_SPIDER

# 初始化flaskAPP
app = Flask(__name__)


# 返回JSON字符串
def return_json(data):
    return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')


# 询问问题
@app.route('/chat/ask', methods=['POST'])
def ask_question():
    spider: GoogleSpider = app.config[GOOGLE_SPIDER]
    data = request.get_json()
    # 返回json类型字符串
    return return_json(spider.search(data["question"]))


# 主页显示HTML
@app.route('/', methods=['GET'])
def index():
    return render_template('content.html')

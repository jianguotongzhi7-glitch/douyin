# backend/api.py
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
import json

app = Flask(__name__)

# 启用CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# 提取抖音无水印视频的端点
@app.route('/api/extract')
def extract():
    # 现有代码保持不变
    pass

# Vercel 要求的入口点
def handler(event, context):
    from werkzeug.wrappers import Request, Response
    from werkzeug.wsgi import DispatcherMiddleware
    
    # 创建 WSGI 应用
    application = DispatcherMiddleware(app)
    
    # 处理请求
    request = Request(event['http'])
    with app.request_context(request.environ):
        response = app.dispatch_request()
        return Response(response.data, status=response.status_code, headers=dict(response.headers))
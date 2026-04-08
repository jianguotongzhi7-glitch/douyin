from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/extract', methods=['POST'])
def extract():
    try:
        data = request.json
        url = data.get('url')
        if not url:
            return jsonify({'error': '请提供抖音链接'}), 400
        
        # 使用第三方API来获取无水印视频链接
        # 这里使用一个示例API，实际部署时可能需要更换
        api_url = f"https://api.example.com/douyin?url={url}"
        
        # 构建请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # 注意：这里使用的是示例API，实际部署时需要使用真实的API
        # 由于是示例，我们直接返回一个模拟的无水印视频链接
        # 在实际项目中，你需要：
        # 1. 找到一个可靠的抖音无水印API服务
        # 2. 或者实现更复杂的反爬逻辑
        
        # 模拟返回结果
        # 实际项目中应该是：response = requests.get(api_url, headers=headers)
        # video_url = response.json().get('video_url')
        
        # 模拟提取成功
        video_url = "https://example.com/video.mp4"
        
        return jsonify({'video_url': video_url}), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
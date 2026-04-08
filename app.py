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
        
        # 直接使用抖音无水印解析服务
        # 这里使用一个免费的解析服务
        # 注意：免费服务可能会有调用限制
        api_url = "https://api.amemv.com/aweme/v1/play/"
        
        # 构建请求参数
        params = {
            'url': url,
            'type': 'video'
        }
        
        # 构建请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }
        
        # 请求解析服务
        response = requests.get(api_url, params=params, headers=headers)
        
        if response.status_code == 200:
            # 如果直接返回视频流，返回URL
            if 'Content-Type' in response.headers and 'video' in response.headers['Content-Type']:
                return jsonify({'video_url': response.url}), 200
            else:
                # 尝试解析JSON响应
                try:
                    result = response.json()
                    if 'data' in result and 'video_url' in result['data']:
                        return jsonify({'video_url': result['data']['video_url']}), 200
                    else:
                        return jsonify({'error': 'API返回格式错误'}), 500
                except:
                    # 如果不是JSON，返回请求的URL
                    return jsonify({'video_url': response.url}), 200
        else:
            # 尝试使用备用方法
            # 直接构建无水印视频URL
            # 注意：这种方法可能需要根据抖音的实际链接格式进行调整
            # 这里使用一个示例URL，实际使用时需要根据抖音的链接格式进行修改
            video_url = "https://example.com/video.mp4"
            
            # 提示用户API调用失败，使用示例链接
            return jsonify({
                'video_url': video_url,
                'warning': 'API调用失败，返回示例链接，请手动替换为实际的无水印视频链接'
            }), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

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
        
        # 提取视频ID
        import re
        video_id = None
        
        # 尝试从链接中提取视频ID
        patterns = [
            r'/video/([\d]+)',
            r'video/([\d]+)',
            r'\?video_id=([\d]+)',
            r'video_id=([\d]+)',
            r'/([\d]+)/'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                video_id = match.group(1)
                break
        
        if not video_id:
            # 如果无法提取视频ID，返回错误信息
            return jsonify({'error': '无法从链接中提取视频ID，请提供包含视频ID的完整链接，例如：https://www.douyin.com/video/1234567890'}), 400
        
        print(f"提取到的视频ID: {video_id}")
        
        # 构建无水印视频URL
        # 抖音无水印视频的URL格式
        video_url = f"https://aweme.snssdk.com/aweme/v1/play/?video_id={video_id}&ratio=720p&line=0&watermark=0"
        
        # 返回无水印视频链接
        print(f"成功获取视频链接: {video_url}")
        return jsonify({'video_url': video_url}), 200
            
    except Exception as e:
        print(f"提取视频失败: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
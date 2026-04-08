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
        
        # 从分享文本中提取抖音链接
        import re
        # 匹配抖音短链接或长链接
        link_pattern = r'(https?://[\w\-]+(\.[\w\-]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?)'
        match = re.search(link_pattern, url)
        if match:
            url = match.group(1)
            print(f"提取到的链接: {url}")
        
        # 构建请求头，模拟真实浏览器
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://www.douyin.com/'
        }
        
        # 使用Session来保持会话
        session = requests.Session()
        session.headers.update(headers)
        
        # 处理短链接
        if 'v.douyin.com' in url:
            # 首先获取短链接的重定向URL
            response = session.get(url, allow_redirects=True)
            final_url = response.url
            print(f"最终URL: {final_url}")
            url = final_url
        
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
        
        # 直接返回无水印视频链接
        print(f"成功获取视频链接: {video_url}")
        return jsonify({'video_url': video_url}), 200
            
    except Exception as e:
        print(f"提取视频失败: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
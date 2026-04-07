const express = require('express');
const axios = require('axios');
const cheerio = require('cheerio');
const cors = require('cors');

const app = express();
const port = 3000;

// 启用CORS
app.use(cors());

// 解析JSON请求体
app.use(express.json());

// 健康检查端点
app.get('/health', (req, res) => {
    res.json({ status: 'ok' });
});

// 提取抖音无水印视频的端点
app.get('/api/extract', async (req, res) => {
    try {
        const { url } = req.query;
        
        if (!url) {
            return res.json({ success: false, message: '请提供抖音视频链接' });
        }
        
        // 解析抖音视频ID
        const videoId = extractVideoId(url);
        if (!videoId) {
            return res.json({ success: false, message: '无效的抖音视频链接' });
        }
        
        // 获取视频信息
        const videoInfo = await getVideoInfo(videoId);
        
        res.json({ success: true, data: videoInfo });
    } catch (error) {
        console.error('提取视频失败:', error);
        res.json({ success: false, message: '提取视频失败，请稍后重试' });
    }
});

// 提取视频ID
function extractVideoId(url) {
    // 从不同格式的链接中提取视频ID
    const regex = /(?:v\.douyin\.com\/|douyin\.com\/video\/|aweme\.snssdk\.com\/aweme\/v1\/play\/)([a-zA-Z0-9]+)/;
    const match = url.match(regex);
    return match ? match[1] : null;
}

// 获取视频信息
async function getVideoInfo(videoId) {
    try {
        // 构造抖音API URL
        const apiUrl = `https://www.douyin.com/video/${videoId}`;
        
        // 设置请求头，模拟浏览器访问
        const headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.douyin.com/'
        };
        
        // 发送请求获取页面内容
        const response = await axios.get(apiUrl, { headers });
        const html = response.data;
        
        // 使用cheerio解析HTML
        const $ = cheerio.load(html);
        
        // 提取视频信息
        const scriptContent = $('script[type="application/ld+json"]').text();
        let videoInfo = {
            title: '未知标题',
            author: '未知作者',
            videoUrl: ''
        };
        
        if (scriptContent) {
            try {
                const jsonData = JSON.parse(scriptContent);
                if (jsonData) {
                    videoInfo.title = jsonData.name || videoInfo.title;
                    videoInfo.author = jsonData.author?.name || videoInfo.author;
                }
            } catch (e) {
                console.error('解析JSON失败:', e);
            }
        }
        
        // 提取视频播放链接
        const videoScript = $('script').filter((i, el) => {
            const content = $(el).text();
            return content.includes('playAddr') || content.includes('videoUrl');
        }).text();
        
        if (videoScript) {
            // 尝试提取无水印视频链接
            const playAddrMatch = videoScript.match(/playAddr:\s*"([^"]+)"/);
            if (playAddrMatch) {
                let videoUrl = playAddrMatch[1].replace(/\\u002F/g, '/');
                // 替换为无水印链接
                videoUrl = videoUrl.replace('playwm', 'play');
                videoInfo.videoUrl = videoUrl;
            }
        }
        
        // 如果没有找到视频链接，尝试其他方式
        if (!videoInfo.videoUrl) {
            // 这里可以添加其他提取视频链接的方法
            console.warn('未找到视频链接');
        }
        
        return videoInfo;
    } catch (error) {
        console.error('获取视频信息失败:', error);
        throw error;
    }
}

// 启动服务器
app.listen(port, () => {
    console.log(`服务器运行在 http://localhost:${port}`);
});
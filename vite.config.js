import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
    plugins: [vue()],
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src')
        }
    },
    server: {
        port: 5173, // 固定端口，避免随机切换
        open: true, // 启动后自动打开浏览器
        cors: true, // 允许跨域
        // 新增：解决中文乱码的响应头配置
        headers: {
            'Content-Type': 'text/html; charset=utf-8'
        },
        proxy: {
            // 代理后端API（关键修改：localhost → 127.0.0.1，强制IPv4）
            '/api': {
                target: 'http://127.0.0.1:8000', // 改为IPv4地址
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api/, ''),
                ws: true, // 支持WebSocket（可选，避免开发时断开）
                secure: false // 非HTTPS环境关闭安全校验
            },
            // 代理MinIO视频（同样改为IPv4）
            '/minio': {
                target: 'http://127.0.0.1:9000', // 改为IPv4地址
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/minio/, ''),
                secure: false
            }
        }
    }
})
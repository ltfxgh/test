<template>
    <!-- 路由出口：所有页面（首页、上传页、详情页）都会渲染到这里 -->
    <div class="app-container">
        <!-- 全局导航栏（可选，提升体验） -->
        <nav class="app-nav">
            <div class="nav-logo">Bodycam 视频管理系统</div>
            <div class="nav-menu">
                <router-link to="/" class="nav-link">首页</router-link>
                <router-link to="/upload" class="nav-link">上传视频</router-link>
            </div>
        </nav>
        <!-- 页面内容区域 -->
        <main class="app-content">
            <router-view />
        </main>
    </div>
</template>

<script setup>
// 无需额外逻辑，仅提供路由出口和基础布局
</script>

<style scoped>
    /* 基础布局样式，避免页面混乱 */
    .app-container {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
    }

    .app-nav {
        background-color: #1989fa;
        color: white;
        padding: 0 20px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .nav-logo {
        font-size: 18px;
        font-weight: bold;
    }

    .nav-menu {
        display: flex;
        gap: 30px;
    }

    .nav-link {
        color: white;
        text-decoration: none;
        font-size: 16px;
        transition: opacity 0.3s;
    }

        .nav-link:hover {
            opacity: 0.8;
        }

    .app-content {
        flex: 1;
        padding: 20px;
        max-width: 1200px;
        margin: 0 auto;
        width: 100%;
    }
</style>
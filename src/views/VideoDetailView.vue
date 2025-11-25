<template>
    <el-container>
        <el-header>
            <h1>视频详情</h1>
            <el-button @click="$router.push('/')">返回首页</el-button>
        </el-header>
        <el-main>
            <el-loading v-if="loading" target=".el-main" text="加载中..." />

            <el-card v-else-if="video" class="detail-card">
                <template #header>
                    <h3>{{ video.title }}</h3>
                </template>
                <!-- 视频加载失败提示 -->
                <video controls
                       :src="getVideoUrl(video.minio_object_name)"
                       style="width: 100%; max-width: 800px;"
                       @error="handleVideoError"></video>
                <p>描述：{{ video.description || '无' }}</p>
                <p>上传时间：{{ video.created_at }}</p>
            </el-card>

            <el-empty v-else description="视频不存在或已删除"></el-empty>
        </el-main>
    </el-container>
</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import { useRoute } from 'vue-router';
    import { getVideoMetadata } from '@/api/video';
    import { ElMessage } from 'element-plus';

    const route = useRoute();
    const video = ref(null);
    const loading = ref(true);

    // 修正视频路径（结合API前缀）
    const getVideoUrl = (objectName) => {
        return `/api/minio/bodycam-videos/${objectName}`;
    };

    // 视频加载错误处理
    const handleVideoError = () => {
        ElMessage.error('视频文件加载失败');
    };

    onMounted(async () => {
        const videoId = route.params.id;
        try {
            loading.value = true;
            const res = await getVideoMetadata(videoId);
            video.value = res;
        } catch (error) {
            video.value = null;
        } finally {
            loading.value = false;
        }
    });
</script>

<style scoped>
    .detail-card {
        max-width: 800px;
        margin: 0 auto;
    }
</style>
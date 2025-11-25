<template>
    <el-container>
        <el-header>
            <h1>Bodycam 视频管理系统</h1>
            <el-button type="primary" @click="$router.push('/upload')">
                <el-icon><UploadFilled /></el-icon> 上传视频
            </el-button>
        </el-header>
        <el-main>
            <!-- 加载状态 -->
            <el-loading v-if="loading" target=".el-main" text="加载中..." />

            <el-table v-else
                      :data="videoList"
                      style="width: 100%"
                      empty-text="暂无视频数据">
                <el-table-column prop="id" label="ID" width="80" />
                <el-table-column prop="title" label="标题" />
                <el-table-column prop="created_at" label="创建时间" />
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button type="primary"
                                   size="small"
                                   @click="$router.push(`/video/${scope.row.id}`)">
                            查看详情
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-main>
    </el-container>
</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import { getVideoList } from '@/api/video'; // 引入列表接口
    import { UploadFilled } from '@element-plus/icons-vue';
    import { ElMessage } from 'element-plus';

    const videoList = ref([]);
    const loading = ref(true); // 新增加载状态

    onMounted(async () => {
        try {
            loading.value = true;
            const res = await getVideoList(); // 调用真实接口
            videoList.value = res;
        } catch (error) {
            ElMessage.error('获取视频列表失败：' + (error.message || ''));
            videoList.value = [];
        } finally {
            loading.value = false; // 无论成功失败都关闭加载
        }
    });
</script>
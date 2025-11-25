<template>
    <el-container>
        <el-header>
            <h1>上传视频</h1>
            <el-button @click="$router.push('/')">返回首页</el-button>
        </el-header>
        <el-main>
            <el-form ref="formRef"
                     :model="form"
                     :rules="rules"
                     label-width="120px"
                     class="upload-form">
                <el-form-item label="视频标题" prop="title">
                    <el-input v-model="form.title" placeholder="请输入视频标题" />
                </el-form-item>
                <el-form-item label="视频描述" prop="description">
                    <el-input type="textarea"
                              v-model="form.description"
                              placeholder="请输入视频描述"
                              rows="3" />
                </el-form-item>
                <el-form-item label="视频文件" prop="file">
                    <el-upload class="upload-demo"
                               action="#"
                               :auto-upload="false"
                               :on-change="handleFileChange"
                               :on-remove="handleFileRemove"
                               :limit="1"
                               accept="video/*"
                               :file-list="fileList">
                        <el-button type="primary">
                            <el-icon><UploadFilled /></el-icon> 选择视频
                        </el-button>
                    </el-upload>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary"
                               @click="submitForm"
                               :loading="submitting">
                        提交上传
                    </el-button>
                </el-form-item>
            </el-form>
        </el-main>
    </el-container>
</template>

<script setup>
    import { ref, reactive } from 'vue';
    import { ElMessage } from 'element-plus';
    import { uploadVideo } from '@/api/video';
    import { UploadFilled } from '@element-plus/icons-vue';
    import { useRouter } from 'vue-router';

    const router = useRouter();
    const formRef = ref(null);
    const submitting = ref(false);
    const fileList = ref([]);

    const form = reactive({
        title: '',
        description: '',
        file: null,
    });

    const rules = {
        title: [
            { required: true, message: '请输入视频标题', trigger: 'blur' },
            { max: 100, message: '长度不能超过100个字符', trigger: 'blur' }
        ],
        file: [
            { required: true, message: '请选择视频文件', trigger: 'change' }
        ]
    };

    // 处理文件选择
    const handleFileChange = (file, fileList) => {
        form.file = file.raw;
        // 限制文件大小不超过500MB
        if (file.size > 500 * 1024 * 1024) {
            ElMessage.error('视频文件不能超过500MB');
            form.file = null;
            fileList.value.pop(); // 修正ref数组操作
        }
    };

    // 处理文件移除
    const handleFileRemove = () => {
        form.file = null; // 移除try语句块
    };

    // 提交表单
    const submitForm = async () => {
        try {
            // 表单验证
            await formRef.value.validate();
            submitting.value = true;

            // 构建表单数据并上传
            const formData = new FormData();
            formData.append('title', form.title);
            formData.append('description', form.description || '');
            formData.append('file', form.file);

            const res = await uploadVideo(formData);
            ElMessage.success('上传成功');
            router.push(`/video/${res.video_id}`);
        } catch (err) {
            console.error('提交失败', err);
            ElMessage.error('提交失败：' + (err.message || '请检查表单信息'));
        } finally {
            submitting.value = false;
        }
    };
</script>

<style scoped>
    .upload-form {
        max-width: 600px;
        margin: 0 auto;
    }
</style>
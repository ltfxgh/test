import request from '@/utils/request';

// 上传视频元数据和文件
export function uploadVideo(data) {
    return request({
        url: '/videos/',
        method: 'post',
        data,
        headers: {
            'Content-Type': 'multipart/form-data' // 明确表单数据类型
        }
    });
}

// 获取单个视频元数据
export function getVideoMetadata(videoId) {
    return request({
        url: `/videos/${videoId}`,
        method: 'get',
    });
}

// 新增：获取视频列表
export function getVideoList() {
    return request({
        url: '/videos/',
        method: 'get',
    });
}
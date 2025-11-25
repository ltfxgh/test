// 引入axios和Element Plus的消息提示组件
import axios from 'axios';
import { ElMessage } from 'element-plus';

// 创建axios实例（统一配置请求）
const service = axios.create({
  baseURL: '/api', // 对应vite.config.js中的代理前缀，自动转发到后端http://localhost:8000
  timeout: 60000, // 超时时间60秒（适配视频上传等大文件操作）
  headers: {
    'X-Requested-With': 'XMLHttpRequest'
  }
});

// 请求拦截器：发送请求前的统一处理（如添加token、设置请求头等）
service.interceptors.request.use(
  (config) => {
    // 示例：如果有用户登录token，可在此处添加（后续扩展登录功能时使用）
    // const token = localStorage.getItem('userToken');
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    return config;
  },
  (error) => {
    // 请求参数错误时的提示
    ElMessage.error('请求参数格式错误，请检查后重试');
    return Promise.reject(error);
  }
);

// 响应拦截器：接收响应后的统一处理（如错误提示、数据格式化等）
service.interceptors.response.use(
  (response) => {
    const res = response.data; // 后端返回的原始数据

    // 按之前后端约定的格式判断（后端返回 {status: "success", data: ...} 或 {status: "error", message: ...}）
    if (res.status !== 'success') {
      // 业务错误：显示后端返回的错误信息
      ElMessage.error(res.message || '操作失败，请稍后重试');
      return Promise.reject(new Error(res.message || 'Error'));
    }

    // 成功：返回响应数据中的data部分（简化组件中获取数据的逻辑）
    return res.data;
  },
  (error) => {
    // 网络错误/服务器错误的统一处理
    let errorMsg = '请求失败';
    if (error.message.includes('Network Error')) {
      errorMsg = '网络连接失败，请检查后端服务是否启动';
    } else if (error.message.includes('timeout')) {
      errorMsg = '请求超时，请重试';
    } else if (error.response) {
      // 根据后端返回的状态码提示
      switch (error.response.status) {
        case 404:
          errorMsg = '请求地址不存在';
          break;
        case 500:
          errorMsg = '服务器内部错误，请联系管理员';
          break;
        case 403:
          errorMsg = '没有访问权限';
          break;
        default:
          errorMsg = `请求失败（状态码：${error.response.status}）`;
      }
    }

    // 显示错误提示
    ElMessage.error(errorMsg);
    console.error('请求错误详情：', error);
    return Promise.reject(error);
  }
);

// 导出axios实例，供其他文件调用
export default service;
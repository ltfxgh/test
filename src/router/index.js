import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import VideoUploadView from '../views/VideoUploadView.vue';
import VideoDetailView from '../views/VideoDetailView.vue';

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView,
        },
        {
            path: '/upload',
            name: 'upload',
            component: VideoUploadView,
        },
        {
            path: '/video/:id',
            name: 'video-detail',
            component: VideoDetailView,
        },
    ],
});

export default router;
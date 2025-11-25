import redis
from config import settings

# 初始化Redis客户端
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    decode_responses=True  # 让返回值为字符串，而非字节
)

# 示例：缓存视频元数据
def cache_video_metadata(video_id, metadata, expire=3600):  # 缓存1小时
    redis_client.set(f"video:{video_id}", str(metadata), ex=expire)

def get_cached_video_metadata(video_id):
    return redis_client.get(f"video:{video_id}")
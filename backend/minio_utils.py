from minio import Minio
from config import settings

# 初始化MinIO客户端
minio_client = Minio(
    endpoint=settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False  # 本地开发用HTTP，生产可改为True（HTTPS）
)

# 确保存储桶存在
def ensure_bucket():
    if not minio_client.bucket_exists(settings.MINIO_BUCKET):
        minio_client.make_bucket(settings.MINIO_BUCKET)

# 上传视频文件到MinIO
def upload_video(file_path, object_name):
    ensure_bucket()
    with open(file_path, "rb") as file:
        minio_client.put_object(
            bucket_name=settings.MINIO_BUCKET,
            object_name=object_name,
            data=file,
            length=-1,  # 自动检测文件大小
            part_size=10*1024*1024  # 分片大小（可选）
        )
    return object_name

# 下载视频文件（可选，根据需求实现）
def download_video(object_name, local_path):
    ensure_bucket()
    minio_client.fget_object(
        bucket_name=settings.MINIO_BUCKET,
        object_name=object_name,
        file_path=local_path
    )
    return local_path
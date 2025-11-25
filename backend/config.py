from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # PostgreSQL配置
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "bodycam"
    POSTGRES_PASSWORD: str = "Bodycam123"
    POSTGRES_DB: str = "bodycam_db"

    # Redis配置
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = "Redis123"

    # MinIO配置
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "admin"
    MINIO_SECRET_KEY: str = "Admin123456"
    MINIO_BUCKET: str = "bodycam-videos"  # 自定义存储桶名

    class Config:
        env_file = ".env"  # 支持从.env文件读取（可选）

settings = Settings()
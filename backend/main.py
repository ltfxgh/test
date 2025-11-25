from fastapi import FastAPI, File, UploadFile, Depends
from sqlalchemy.orm import Session
from db import SessionLocal, create_tables
from models import VideoMetadata
from minio_utils import upload_video
from redis_utils import cache_video_metadata, get_cached_video_metadata
from datetime import datetime
import os

app = FastAPI(title="Bodycam后端服务")

# 依赖项：数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 启动时创建数据库表（仅首次需要）
@app.on_event("startup")
def startup_event():
    create_tables()

# 示例API：上传视频并存储元数据
@app.post("/videos/")
async def upload_video_api(
    title: str,
    description: str = "",
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. 保存临时文件
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    
    # 2. 上传到MinIO
    object_name = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{file.filename}"
    minio_object_name = upload_video(temp_path, object_name)
    
    # 3. 存储元数据到PostgreSQL
    video_metadata = VideoMetadata(
        title=title,
        description=description,
        minio_object_name=minio_object_name
    )
    db.add(video_metadata)
    db.commit()
    db.refresh(video_metadata)
    
    # 4. 缓存元数据到Redis
    cache_video_metadata(video_metadata.id, video_metadata)
    
    # 5. 删除临时文件
    os.remove(temp_path)
    
    return {
        "status": "success",
        "data": {
            "video_id": video_metadata.id,
            "title": video_metadata.title,
            "minio_object_name": video_metadata.minio_object_name
        }
    }

# 示例API：获取视频元数据（优先读缓存）
@app.get("/videos/{video_id}")
async def get_video_metadata(
    video_id: int,
    db: Session = Depends(get_db)
):
    # 先查Redis缓存
    cached_data = get_cached_video_metadata(video_id)
    if cached_data:
        return {"status": "success", "data": cached_data, "source": "cache"}
    
    # 缓存未命中，查数据库
    video = db.query(VideoMetadata).filter(VideoMetadata.id == video_id).first()
    if not video:
        return {"status": "error", "message": "Video not found"}
    
    # 写入缓存
    cache_video_metadata(video_id, video)
    return {"status": "success", "data": video, "source": "database"}
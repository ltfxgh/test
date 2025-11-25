from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class VideoMetadata(Base):
    __tablename__ = "video_metadata"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    minio_object_name = Column(String(255), nullable=False)  # MinIO中存储的文件名
    created_at = Column(DateTime, default=datetime.utcnow)
    # 可根据需求扩展字段（如拍摄时间、标签等）
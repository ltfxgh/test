from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings

# 连接PostgreSQL
DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建表（首次启动时需执行）
def create_tables():
    from models import Base
    Base.metadata.create_all(bind=engine)
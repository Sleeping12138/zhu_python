from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus
from config import settings

# 连接数据库URL（对密码进行URL编码，避免特殊字符导致连接失败）
encoded_password = quote_plus(settings.DB_CONFIG['password'])
encoded_user = quote_plus(settings.DB_CONFIG['user'])
DATABASE_URL = f"mysql+aiomysql://{encoded_user}:{encoded_password}@{settings.DB_CONFIG['host']}/{settings.DB_CONFIG['database']}"

# 创建异步引擎
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

# 用于异步
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()


async def get_db():
    """
    异步数据库会话
    """
    async with AsyncSessionLocal() as session:
        yield session

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# 數據庫配置 (僅保留在main.py)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:huiji.233@localhost:5432/dev"
)
engine = create_async_engine(DATABASE_URL, echo=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield

# 創建FastAPI實例
app = FastAPI(lifespan=lifespan)

# 中間件配置
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 導入並註冊路由
from routers.softwareinfo import router as softwareinfo_router
app.include_router(softwareinfo_router)

from routers.softwarelicense import router as softwarelicense_router
app.include_router(softwarelicense_router)
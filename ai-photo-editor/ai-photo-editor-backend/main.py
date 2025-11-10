import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tools.logger import setup_logging
from routers.tasks import router as tasks_router
from routers.scheduled_tasks import router as scheduled_tasks_router, set_scheduler
from routers.virtual_try import router as virtual_try_router
from routers.upload import router as upload_router
from database import engine, Base

# 初始化日志
logger = setup_logging()

# 创建FastAPI应用
app = FastAPI(title="AI Photo Editor Backend", version="1.0.0")

# 初始化 APScheduler
scheduler = AsyncIOScheduler()

# 设置调度器到定时任务路由模块
set_scheduler(scheduler)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由
app.include_router(tasks_router)
app.include_router(scheduled_tasks_router)
app.include_router(virtual_try_router)
app.include_router(upload_router)


@app.on_event("startup")
async def startup_event():
    """应用启动时启动调度器"""
    scheduler.start()
    logger.info("APScheduler 调度器已启动")
    logger.info("数据库引擎已初始化")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时关闭调度器"""
    scheduler.shutdown()
    logger.info("APScheduler 调度器已关闭")
    await engine.dispose()
    logger.info("数据库引擎已关闭")


# 用于本地测试
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        workers=1,
        log_level="info"
    )

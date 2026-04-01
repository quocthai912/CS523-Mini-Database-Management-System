from __future__ import annotations

"""
Entry point của ứng dụng FastAPI.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Cấu hình ứng dụng được đọc từ file .env."""

    app_name: str = "Mini Database Management System"
    app_version: str = "1.0.0"
    debug: bool = False

    class Config:
        env_file = ".env"


settings = Settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    description="Hệ Quản Trị Cơ Sở Dữ Liệu Mini Sử Dụng Cây BTree Làm Chỉ Mục",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.student_router import router as student_router

app.include_router(student_router)


@app.get("/", tags=["Health"])
async def root() -> dict:
    """Health check endpoint."""
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
    }


@app.get("/health", tags=["Health"])
async def health_check() -> dict:
    """Kiểm tra chi tiết trạng thái hệ thống"""
    return {"status": "healthy", "debug_mode": settings.debug}

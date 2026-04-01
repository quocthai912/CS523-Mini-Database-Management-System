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

    app_name: str = "Mini DBMS Indexing Visualizer"
    app_version: str = "1.0.0"
    debug: bool = True
    cors_origins: list[str] = ["http://localhost:5173"]

    class Config:
        env_file = ".env"


settings = Settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    description="API quản lý sinh viên với minh hoạ B-Tree indexing",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers
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
    """Chi tiết trạng thái hệ thống."""
    return {"status": "healthy", "debug_mode": settings.debug}

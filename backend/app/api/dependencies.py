from __future__ import annotations

"""
Module quản lý Dependency Injection cho FastAPI.
Dùng singleton pattern để đảm bảo toàn bộ ứng dụng dùng chung một instance Repository và Service.
SOLID: Dependency Inversion — API layer nhận Service qua hàm get_student_service(), không tự khởi tạo.
"""

from functools import lru_cache
from app.repository.student_repository import BTreeStudentRepository
from app.service.student_service import StudentService


@lru_cache(maxsize=1)
def get_repository() -> BTreeStudentRepository:
    """
    Tạo và cache một instance BTreeStudentRepository duy nhất.

    lru_cache đảm bảo hàm này chỉ chạy một lần trong suốt vòng đời ứng dụng → singleton pattern.

    Returns:
        Instance BTreeStudentRepository duy nhất.
    """
    return BTreeStudentRepository()


@lru_cache(maxsize=1)
def get_student_service() -> StudentService:
    """
    Tạo và cache một instance StudentService duy nhất.

    Inject repository vào service tại đây — đây là điểm
    duy nhất trong ứng dụng biết implementation cụ thể là BTree.

    Returns:
        Instance StudentService duy nhất.
    """
    return StudentService(repository=get_repository())

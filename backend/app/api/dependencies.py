from __future__ import annotations

"""
Module quản lý Dependency Injection cho FastAPI.

Thay vì dùng singleton toàn cục, mỗi session_id sẽ có
Repository và Service riêng — đảm bảo dữ liệu độc lập.

SOLID: Dependency Inversion — API layer nhận Service qua
hàm get_student_service(), không tự khởi tạo.
"""

from app.repository.student_repository import BTreeStudentRepository
from app.service.student_service import StudentService

# Dict lưu repository theo session_id
_session_repositories: dict[str, BTreeStudentRepository] = {}


def get_repository_for_session(session_id: str) -> BTreeStudentRepository:
    """
    Lấy hoặc tạo mới Repository cho session_id.

    Mỗi session_id có 1 BTreeStudentRepository riêng biệt
    → dữ liệu hoàn toàn độc lập giữa các người dùng.

    Args:
        session_id: UUID định danh phiên làm việc của người dùng.

    Returns:
        BTreeStudentRepository tương ứng với session_id.
    """
    if session_id not in _session_repositories:
        _session_repositories[session_id] = BTreeStudentRepository()
    return _session_repositories[session_id]


def get_student_service_for_session(session_id: str) -> StudentService:
    """
    Tạo StudentService với Repository tương ứng session_id.

    Args:
        session_id: UUID định danh phiên làm việc của người dùng.

    Returns:
        StudentService được inject đúng Repository.
    """
    repo = get_repository_for_session(session_id)
    return StudentService(repository=repo)

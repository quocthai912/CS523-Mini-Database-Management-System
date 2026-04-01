from __future__ import annotations

"""
Module định nghĩa FastAPI Router cho Student endpoints.

Chịu trách nhiệm:
- Định nghĩa HTTP routes (GET, POST, PUT, DELETE).
- Parse và validate request data qua Pydantic schemas.
- Gọi Service layer để xử lý logic.
- Trả về response chuẩn hóa.

SOLID: Single Responsibility — chỉ lo HTTP routing,
không chứa business logic hay storage logic.
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from app.api.schemas import (
    StudentCreateRequest,
    StudentUpdateRequest,
    ApiResponse,
    TreeSnapshotResponse,
)
from app.api.dependencies import get_student_service
from app.service.student_service import StudentService

router = APIRouter(prefix="/api/students", tags=["Students"])


def _clean(msg: str) -> str:
    """Lột bỏ dấu nháy đơn/kép thừa bọc quanh message từ exception."""
    return str(msg).strip("'\"")


@router.get("", response_model=ApiResponse)
async def get_all_students(
    service: StudentService = Depends(get_student_service),
) -> ApiResponse:
    """
    Lấy toàn bộ danh sách sinh viên theo thứ tự thêm vào.

    Returns:
        ApiResponse chứa danh sách sinh viên.
    """
    students = service.get_all_students()
    return ApiResponse(
        success=True,
        message=f"Retrieved {len(students)} student(s) successfully.",
        data={"students": students, "total": len(students)},
    )


@router.get("/search", response_model=ApiResponse)
async def search_students(
    name: str = Query(min_length=1, description="Student name to search"),
    service: StudentService = Depends(get_student_service),
) -> ApiResponse:
    """
    Tìm kiếm sinh viên theo tên (partial match).

    Args:
        name: Chuỗi tên cần tìm kiếm.

    Returns:
        ApiResponse chứa danh sách sinh viên khớp.
    """
    try:
        students = service.search_by_name(name)
        return ApiResponse(
            success=True,
            message=f"Found {len(students)} student(s).",
            data={"students": students, "total": len(students)},
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=_clean(str(e)))


@router.get("/tree", response_model=TreeSnapshotResponse)
async def get_tree_snapshot(
    service: StudentService = Depends(get_student_service),
) -> TreeSnapshotResponse:
    """
    Lấy snapshot cấu trúc B-Tree để frontend visualize.

    Returns:
        TreeSnapshotResponse chứa cấu trúc cây.
    """
    snapshot = service.get_tree_snapshot()
    return TreeSnapshotResponse(success=True, data=snapshot)


@router.get("/{student_id}", response_model=ApiResponse)
async def get_student(
    student_id: int,
    service: StudentService = Depends(get_student_service),
) -> ApiResponse:
    """
    Lấy thông tin một sinh viên theo mã số.

    Args:
        student_id: Mã sinh viên cần tìm.

    Returns:
        ApiResponse chứa thông tin sinh viên.
    """
    try:
        student = service.get_student(student_id)
        return ApiResponse(
            success=True,
            message="Student found.",
            data=student,
        )
    except KeyError as e:
        raise HTTPException(status_code=404, detail=_clean(str(e)))


@router.post("", response_model=ApiResponse, status_code=201)
async def create_student(
    body: StudentCreateRequest,
    service: StudentService = Depends(get_student_service),
) -> ApiResponse:
    """
    Tạo sinh viên mới.

    Args:
        body: Dữ liệu sinh viên từ request body.

    Returns:
        ApiResponse chứa thông tin sinh viên vừa tạo.
    """
    try:
        student = service.create_student(
            student_id=body.student_id,
            full_name=body.full_name,
            gender=body.gender.value,
            major=body.major,
            gpa=body.gpa,
            email=body.email,
        )
        return ApiResponse(
            success=True,
            message=f"Student {body.student_id} created successfully.",
            data=student,
        )
    except KeyError as e:
        raise HTTPException(status_code=409, detail=_clean(str(e)))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=_clean(str(e)))


@router.put("/{student_id}", response_model=ApiResponse)
async def update_student(
    student_id: int,
    body: StudentUpdateRequest,
    service: StudentService = Depends(get_student_service),
) -> ApiResponse:
    """
    Cập nhật thông tin sinh viên.

    Args:
        student_id: Mã sinh viên cần cập nhật.
        body: Dữ liệu mới từ request body.

    Returns:
        ApiResponse chứa thông tin sinh viên sau khi cập nhật.
    """
    try:
        student = service.update_student(
            student_id=student_id,
            full_name=body.full_name,
            gender=body.gender.value,
            major=body.major,
            gpa=body.gpa,
            email=body.email,
        )
        return ApiResponse(
            success=True,
            message=f"Student {student_id} updated successfully.",
            data=student,
        )
    except KeyError as e:
        raise HTTPException(status_code=404, detail=_clean(str(e)))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=_clean(str(e)))


@router.delete("/{student_id}", response_model=ApiResponse)
async def delete_student(
    student_id: int,
    service: StudentService = Depends(get_student_service),
) -> ApiResponse:
    """
    Xóa sinh viên khỏi hệ thống.

    Args:
        student_id: Mã sinh viên cần xóa.

    Returns:
        ApiResponse xác nhận xóa thành công.
    """
    try:
        result = service.delete_student(student_id)
        return ApiResponse(
            success=True,
            message=result["message"],
            data=None,
        )
    except KeyError as e:
        raise HTTPException(status_code=404, detail=_clean(str(e)))

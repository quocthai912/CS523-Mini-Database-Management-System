from __future__ import annotations

"""
Module định nghĩa Pydantic Schemas cho API Request/Response.

Schemas khác với Domain Entities:
- Entity: Đối tượng nghiệp vụ thuần túy, dùng nội bộ.
- Schema: Định nghĩa shape của HTTP request/response, có validation.

SOLID: Single Responsibility — chỉ lo validate và serialize HTTP data.
"""

from pydantic import BaseModel, Field, field_validator
from app.domain.entities import Gender


class StudentCreateRequest(BaseModel):
    """Schema cho request tạo sinh viên mới (POST /students)."""

    student_id: int = Field(
        gt=0,
        description="Mã sinh viên (số nguyên dương)",
        examples=[22001],
    )
    full_name: str = Field(
        min_length=1,
        max_length=100,
        description="Họ và tên đầy đủ",
        examples=["Nguyen Van An"],
    )
    gender: Gender = Field(
        description="Giới tính",
        examples=[Gender.MALE],
    )
    major: str = Field(
        min_length=1,
        max_length=100,
        description="Ngành học",
        examples=["Computer Science"],
    )
    gpa: float = Field(
        ge=0.0,
        le=4.0,
        description="Điểm trung bình tích lũy (0.0 - 4.0)",
        examples=[3.5],
    )
    email: str = Field(
        min_length=5,
        max_length=100,
        description="Địa chỉ email",
        examples=["22001@student.edu.vn"],
    )

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        """Kiểm tra email có chứa '@' không."""
        if "@" not in v:
            raise ValueError("Email không hợp lệ.")
        return v.strip().lower()

    @field_validator("full_name", "major")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        """Loại bỏ khoảng trắng thừa ở đầu và cuối."""
        return v.strip()


class StudentUpdateRequest(BaseModel):
    """Schema cho request cập nhật sinh viên (PUT /students/{id})."""

    full_name: str = Field(min_length=1, max_length=100)
    gender: Gender
    major: str = Field(min_length=1, max_length=100)
    gpa: float = Field(ge=0.0, le=4.0)
    email: str = Field(min_length=5, max_length=100)

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Email không hợp lệ.")
        return v.strip().lower()

    @field_validator("full_name", "major")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()


class StudentResponse(BaseModel):
    """Schema cho response trả về thông tin sinh viên."""

    student_id: int
    full_name: str
    gender: str
    major: str
    gpa: float
    email: str


class ApiResponse(BaseModel):
    """Schema chuẩn cho mọi API response."""

    success: bool
    message: str
    data: dict | list | None = None


class TreeSnapshotResponse(BaseModel):
    """Schema cho response trả về cấu trúc B-Tree."""

    success: bool
    data: dict

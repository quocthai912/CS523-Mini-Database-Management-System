from __future__ import annotations

"""
Module định nghĩa các Domain Entities của hệ thống.
Entity là đối tượng nghiệp vụ thuần túy — không phụ thuộc vào FastAPI, database, hay bất kỳ framework nào.
SOLID: Single Responsibility — chỉ mô tả cấu trúc dữ liệu nghiệp vụ.
Hay nói cách khác Module này được dùng để định nghĩa đầy đủ thông tin của một sinh viên trong toàn bộ hệ thống.
"""

"""
Đồng thời, Module này đóng vai trò là 'bộ chuyển đổi' (Serializer/Deserializer) mượt mà giữa dữ liệu giao diện (Frontend) và đối tượng nghiệp vụ bên trong Backend 
cụ thể là:
- Hàm from_dict: Nhận dữ liệu JSON từ Frontend gửi xuống API, hàm sẽ chuyển nó thành một đối tượng Student hoàn chỉnh để thêm vào cây BTree.
- Hàm to_dict: Khi Frontend cần xem dữ liệu, hệ thống sẽ lấy Student từ kho lưu trữ (Cây BTree) ra và ép ngược lại thành định dạng JSON để trả về cho Frontend.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Gender(str, Enum):
    """Giới tính sinh viên."""

    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


@dataclass
class Student:
    """
    Entity đại diện cho một sinh viên trong hệ thống.

    Attributes:
        student_id: Mã sinh viên (khóa chính, dùng làm khóa cho cây BTree).
        full_name: Họ và tên đầy đủ.
        gender: Giới tính.
        major: Ngành học.
        gpa: Điểm trung bình tích lũy (0.0 - 4.0).
        email: Địa chỉ email.
    """

    student_id: int
    full_name: str
    gender: Gender
    major: str
    gpa: float
    email: str

    def to_dict(self) -> dict:
        """Chuyển entity thành dict để serialize."""
        return {
            "student_id": self.student_id,
            "full_name": self.full_name,
            "gender": self.gender.value,
            "major": self.major,
            "gpa": self.gpa,
            "email": self.email,
        }

    @staticmethod
    def from_dict(data: dict) -> "Student":
        """Tạo Student entity từ dict."""
        return Student(
            student_id=data["student_id"],
            full_name=data["full_name"],
            gender=Gender(data["gender"]),
            major=data["major"],
            gpa=data["gpa"],
            email=data["email"],
        )

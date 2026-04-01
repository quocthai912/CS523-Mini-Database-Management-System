from __future__ import annotations

"""
Module chứa Business Logic (Logic nghiệp vụ) cho Student Management.

Service layer chịu trách nhiệm:
- Validation (Xác thực) dữ liệu đầu vào.
- Điều phối giữa API layer và Repository layer.
- Xử lý các business rule (ví dụ: GPA phải từ 0.0 đến 4.0).

SOLID:
- Single Responsibility: Chỉ lo business logic, không lo HTTP hay storage.
- Dependency Inversion: Nhận IStudentRepository qua constructor — không cần biết implementation cụ thể là BTree hay SQL.
"""

from typing import Optional
from app.domain.entities import Student, Gender
from app.domain.interfaces import IStudentRepository


class StudentService:
    """
    Service xử lý business logic cho Student Management.
    """

    def __init__(self, repository: IStudentRepository) -> None:
        """
        Khởi tạo service với repository được inject từ bên ngoài.

        Args:
            repository: Implementation của IStudentRepository.
        """
        self._repo = repository

    #  CREATE (Khởi tạo thông tin sinh viên)

    def create_student(
        self,
        student_id: int,
        full_name: str,
        gender: str,
        major: str,
        gpa: float,
        email: str,
    ) -> dict:
        """
        Tạo sinh viên mới sau khi validate (Xác thực) dữ liệu.

        Args:
            student_id: Mã sinh viên (phải > 0).
            full_name: Họ tên (không được rỗng).
            gender: Giới tính ('male', 'female', 'other').
            major: Ngành học (không được rỗng).
            gpa: Điểm TB (0.0 - 4.0).
            email: Email hợp lệ.

        Returns:
            Dict chứa thông tin sinh viên vừa tạo.

        Raises:
            ValueError: Nếu dữ liệu không hợp lệ.
            KeyError: Nếu student_id đã tồn tại.
        """
        # Validation
        self._validate_student_id(student_id)
        self._validate_full_name(full_name)
        self._validate_gpa(gpa)
        self._validate_email(email)
        gender_enum = self._validate_gender(gender)

        student = Student(
            student_id=student_id,
            full_name=full_name.strip(),
            gender=gender_enum,
            major=major.strip(),
            gpa=round(gpa, 2),
            email=email.strip().lower(),
        )

        success = self._repo.add(student)
        if not success:
            raise KeyError(f"Student ID {student_id} already exists in the system.")

        return student.to_dict()

    #  READ (Đọc - Lấy thông tin sinh viên)

    def get_student(self, student_id: int) -> dict:
        """
        Lấy thông tin một sinh viên theo ID.

        Args:
            student_id: Mã sinh viên cần tìm.

        Returns:
            Dict thông tin sinh viên.

        Raises:
            KeyError: Nếu không tìm thấy sinh viên.
        """
        student = self._repo.find_by_id(student_id)
        if student is None:
            raise KeyError(f"Student ID {student_id} not found.")
        return student.to_dict()

    def get_all_students(self) -> list[dict]:
        """
        Lấy toàn bộ sinh viên theo thứ tự thêm vào.

        Returns:
            Danh sách dict thông tin sinh viên.
        """
        return [s.to_dict() for s in self._repo.find_all()]

    def search_by_name(self, name: str) -> list[dict]:
        """
        Tìm kiếm sinh viên theo tên (partial, case-insensitive).

        Args:
            name: Chuỗi tên cần tìm.

        Returns:
            Danh sách dict sinh viên khớp.

        Raises:
            ValueError: Nếu chuỗi tìm kiếm rỗng.
        """
        if not name or not name.strip():
            raise ValueError("Search string must not be empty.")
        return [s.to_dict() for s in self._repo.find_by_name(name.strip())]

    def get_tree_snapshot(self) -> dict:
        """
        Lấy snapshot cấu trúc B-Tree để frontend visualize.

        Returns:
            Dict cấu trúc cây B-Tree.
        """
        return self._repo.get_tree_snapshot()

    #  UPDATE (Cập nhật thông tin sinh viên)

    def update_student(
        self,
        student_id: int,
        full_name: str,
        gender: str,
        major: str,
        gpa: float,
        email: str,
    ) -> dict:
        """
        Cập nhật thông tin sinh viên.

        Args:
            student_id: Mã sinh viên cần cập nhật.
            full_name: Họ tên mới.
            gender: Giới tính mới.
            major: Ngành học mới.
            gpa: Điểm TB mới.
            email: Email mới.

        Returns:
            Dict thông tin sinh viên sau khi cập nhật.

        Raises:
            ValueError: Nếu dữ liệu không hợp lệ.
            KeyError: Nếu không tìm thấy sinh viên.
        """
        # Validation
        self._validate_full_name(full_name)
        self._validate_gpa(gpa)
        self._validate_email(email)
        gender_enum = self._validate_gender(gender)

        student = Student(
            student_id=student_id,
            full_name=full_name.strip(),
            gender=gender_enum,
            major=major.strip(),
            gpa=round(gpa, 2),
            email=email.strip().lower(),
        )

        success = self._repo.update(student)
        if not success:
            raise KeyError(f"Student ID {student_id} not found.")

        return student.to_dict()

    #  DELETE (Xóa thông tin sinh viên khỏi hệ thống)

    def delete_student(self, student_id: int) -> dict:
        """
        Xóa sinh viên khỏi hệ thống.

        Args:
            student_id: Mã sinh viên cần xóa.

        Returns:
            Dict xác nhận xóa thành công.

        Raises:
            KeyError: Nếu không tìm thấy sinh viên.
        """
        success = self._repo.remove(student_id)
        if not success:
            raise KeyError(f"Student ID {student_id} not found.")

        return {"message": f"Student {student_id} deleted successfully."}

    #  PRIVATE VALIDATORS (Các hàm xác thực các Logic nghiệp vụ và xác thực thông tin sinh viên)

    def _validate_student_id(self, student_id: int) -> None:
        """Kiểm tra student_id phải là số nguyên dương."""
        if student_id <= 0:
            raise ValueError("Student ID must be a positive integer.")

    def _validate_full_name(self, full_name: str) -> None:
        """Kiểm tra họ tên không được rỗng và không quá 100 ký tự."""
        if not full_name or not full_name.strip():
            raise ValueError("Full name must not be empty.")
        if len(full_name.strip()) > 100:
            raise ValueError("Full name must not exceed 100 characters.")

    def _validate_gpa(self, gpa: float) -> None:
        """Kiểm tra GPA phải nằm trong khoảng 0.0 đến 4.0."""
        if not (0.0 <= gpa <= 4.0):
            raise ValueError("GPA must be between 0.0 and 4.0.")

    def _validate_email(self, email: str) -> None:
        """Kiểm tra email không được rỗng và có định dạng cơ bản."""
        if not email or not email.strip():
            raise ValueError("Email must not be empty.")
        if "@" not in email:
            raise ValueError("Invalid email address.")

    def _validate_gender(self, gender: str) -> Gender:
        """
        Kiểm tra giới tính hợp lệ và chuyển sang Gender enum.

        Args:
            gender: Chuỗi giới tính ('male', 'female', 'other').

        Returns:
            Gender enum tương ứng.

        Raises:
            ValueError: Nếu giá trị không hợp lệ.
        """
        try:
            return Gender(gender.lower())
        except ValueError:
            valid = [g.value for g in Gender]
            raise ValueError(f"Gender must be one of: {valid}.")

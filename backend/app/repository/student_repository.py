"""
Module cài đặt StudentRepository sử dụng B-Tree làm Database.

Đây là implementation cụ thể của IStudentRepository (Sử dụng cây BTree).
Dùng BTree để index theo student_id (O(log n) search/insert/delete).
Dùng dict để lưu trữ toàn bộ thông tin Student (O(1) lookup sau khi đã có student_id từ B-Tree).
Dùng list _insertion_order để ghi nhớ thứ tự thêm vào — đảm bảo find_all() trả về đúng thứ tự người dùng thêm vào.

SOLID:
- Single Responsibility: Chỉ lo việc lưu trữ và truy xuất dữ liệu.
- Open/Closed: Muốn thêm index theo tên → thêm BTree mới, không sửa logic hiện tại.
- Liskov Substitution: Class này có thể thay thế IStudentRepository hoàn toàn mà không phá vỡ Service layer.
- Dependency Inversion: Implement từ interface, không để layer trên phụ thuộc trực tiếp vào class này.
"""

from __future__ import annotations
from typing import Optional

from app.core.btree import BTree
from app.domain.entities import Student
from app.domain.interfaces import IStudentRepository


class BTreeStudentRepository(IStudentRepository):
    """
    Student Repository sử dụng B-Tree làm chỉ mục (index).

    Storage architecture:
    - _index (BTree)          : Lưu student_id làm key → O(log n) search.
    - _store (dict)           : Map student_id → Student entity → O(1) access.
    - _insertion_order (list) : Ghi nhớ thứ tự thêm vào → find_all() đúng thứ tự.

    Luồng INSERT : student_id → BTree.insert() + dict[id] = student + list.append(id)
    Luồng SEARCH : BTree.search(id) → dict[id]
    Luồng DELETE : BTree.delete(id) + dict.pop(id) + list.remove(id)
    """

    def __init__(self) -> None:
        """Khởi tạo repository với B-Tree index, dict storage và insertion order rỗng."""
        self._index: BTree = BTree()
        self._store: dict[int, Student] = {}
        self._insertion_order: list[int] = []  # Track thứ tự thêm vào

    #  Implement IStudentRepository

    def add(self, student: Student) -> bool:
        """
        Thêm sinh viên mới.

        Chèn student_id vào B-Tree index trước,
        nếu thành công mới lưu vào dict store và ghi nhớ thứ tự.

        Args:
            student: Student entity cần thêm.

        Returns:
            True nếu thêm thành công, False nếu student_id đã tồn tại.
        """
        inserted = self._index.insert(student.student_id)
        if not inserted:
            return False  # Duplicate student_id

        self._store[student.student_id] = student
        self._insertion_order.append(student.student_id)  # Ghi nhớ thứ tự
        return True

    def find_by_id(self, student_id: int) -> Optional[Student]:
        """
        Tìm sinh viên theo ID.

        Dùng B-Tree search để xác nhận key tồn tại,
        sau đó lấy data từ dict store.

        Args:
            student_id: Mã sinh viên cần tìm.

        Returns:
            Student entity nếu tìm thấy, None nếu không.
        """
        node = self._index.search(student_id)
        if node is None:
            return None
        return self._store.get(student_id)

    def find_all(self) -> list[Student]:
        """
        Lấy toàn bộ sinh viên theo đúng thứ tự được thêm vào.

        Dùng _insertion_order list để đảm bảo thứ tự hiển thị
        khớp với thứ tự người dùng thêm vào hệ thống.

        Returns:
            Danh sách Student entities theo thứ tự thêm vào.
        """
        return [self._store[sid] for sid in self._insertion_order if sid in self._store]

    def update(self, student: Student) -> bool:
        """
        Cập nhật thông tin sinh viên (không thay đổi student_id).

        B-Tree index không cần thay đổi vì student_id giữ nguyên.
        _insertion_order cũng không thay đổi — vị trí trong danh
        sách hiển thị giữ nguyên sau khi update.

        Args:
            student: Student entity với thông tin mới.

        Returns:
            True nếu cập nhật thành công, False nếu không tìm thấy.
        """
        if self._index.search(student.student_id) is None:
            return False

        self._store[student.student_id] = student
        return True

    def remove(self, student_id: int) -> bool:
        """
        Xóa sinh viên.

        Xóa khỏi B-Tree index, dict store và _insertion_order.

        Args:
            student_id: Mã sinh viên cần xóa.

        Returns:
            True nếu xóa thành công, False nếu không tìm thấy.
        """
        deleted = self._index.delete(student_id)
        if not deleted:
            return False

        self._store.pop(student_id, None)
        self._insertion_order.remove(student_id)  # Xóa khỏi danh sách thứ tự
        return True

    def get_tree_snapshot(self) -> dict:
        """
        Lấy snapshot B-Tree để frontend visualize.

        Returns:
            Dict chứa cấu trúc cây đầy đủ.
        """
        return self._index.get_snapshot()

    def find_by_name(self, name: str) -> list[Student]:
        """
        Tìm sinh viên theo tên (partial match, case-insensitive).

        Giữ nguyên thứ tự insertion order trong kết quả trả về.
        Sử dụng Linear Search với độ phức tạp O(n) vì không có B-Tree index theo tên.

        Args:
            name: Chuỗi tên cần tìm (không phân biệt hoa thường).

        Returns:
            Danh sách Student entities khớp với tên theo thứ tự thêm vào.
        """
        name_lower = name.lower()
        return [
            self._store[sid]
            for sid in self._insertion_order
            if sid in self._store and name_lower in self._store[sid].full_name.lower()
        ]

    def get_sorted_students(self) -> list[Student]:
        """
        Lấy danh sách sinh viên theo thứ tự MSSV tăng dần.

        Khác với find_all() trả về insertion order (Thứ tự người dùng nhập vào),
        method này dùng B-Tree in-order traversal.

        Returns:
            Danh sách Student entities được sắp xếp theo student_id.
        """
        sorted_ids = self._index.get_all_keys()
        return [self._store[sid] for sid in sorted_ids if sid in self._store]

    @property
    def total_count(self) -> int:
        """Tổng số sinh viên hiện có trong repository."""
        return self._index.size

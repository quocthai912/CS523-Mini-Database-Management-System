"""
Module định nghĩa Giao Diện (Interface) cho Kho lưu trữ (Repository).

Đây là nơi áp dụng nguyên lý Đảo ngược phụ thuộc (Dependency Inversion - chữ D trong SOLID):
1. Tính linh hoạt (Plug & Play): Hệ thống chỉ ra lệnh "Cần lưu sinh viên",
   còn việc lưu bằng cây B-Tree, SQL hay File Excel là chuyện của lớp thực thi bên dưới.
2. Dễ dàng thay thế: Nếu sau này muốn đổi từ cây B-Tree sang các Database khác (MySQL, MongoDB),
   Chỉ cần tạo một lớp mới và triển khai giao diện này là xong, KHÔNG CẦN sửa lại code ở tầng xử lý hay giao diện.
3. Tách biệt hoàn toàn: Tầng điều khiển (API/Service) sẽ không bị "dính chặt" vào một công nghệ cụ thể nào.

Tuân thủ SOLID:
- Interface Segregation (Phân tách giao diện): Chỉ khai báo những hàm thực sự cần thiết cho việc quản lý sinh viên.
- Dependency Inversion (Đảo ngược phụ thuộc): Các tầng cao (API) chỉ tin tưởng vào "Giao Diện" (Interface),
  không quan tâm đến chi tiết cài đặt phức tạp bên dưới (Implementation).
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities import Student


class IStudentRepository(ABC):
    """
    Đây là phần Giao Diện (Interface) được dùng để định nghĩa và quy định cách thức làm việc với Kho lưu trữ Sinh viên.

    Hiểu đơn giản:
    - Nó đặt ra một bộ quy tắc chung: "Muốn làm Database của kho lưu trữ này, Database đó phải có đủ các đủ chức năng: Thêm, Xóa, Sửa, Tìm".
    - Nhờ có phần giao diện này, ta có thể dễ dàng thay đổi và triển khai bất kì hệ quản trị cơ sở dữ liệu nào.
    - Tầng điều khiển (API/Service) cũng không cần quan tâm bên dưới đang xài công nghệ gì, kho lưu trữ nào
      và cũng không bao giờ phải sửa lại code mỗi khi thay đổi loại kho lưu trữ (Database).
    """

    @abstractmethod
    def add(self, student: Student) -> bool:
        """
        Thêm sinh viên mới vào storage.

        Args:
            student: Entity sinh viên cần thêm.

        Returns:
            True nếu thêm thành công, False nếu student_id đã tồn tại.
        """
        ...

    @abstractmethod
    def find_by_id(self, student_id: int) -> Optional[Student]:
        """
        Tìm sinh viên theo mã số.

        Args:
            student_id: Mã sinh viên cần tìm.

        Returns:
            Student entity nếu tìm thấy, None nếu không.
        """
        ...

    @abstractmethod
    def find_all(self) -> list[Student]:
        """
        Lấy toàn bộ danh sách sinh viên (theo thứ tự student_id tăng dần).

        Returns:
            Danh sách Student entities.
        """
        ...

    @abstractmethod
    def update(self, student: Student) -> bool:
        """
        Cập nhật thông tin sinh viên.

        Args:
            student: Entity sinh viên với thông tin mới
                     (student_id phải tồn tại).

        Returns:
            True nếu cập nhật thành công, False nếu không tìm thấy.
        """
        ...

    @abstractmethod
    def remove(self, student_id: int) -> bool:
        """
        Xóa sinh viên khỏi storage.

        Args:
            student_id: Mã sinh viên cần xóa.

        Returns:
            True nếu xóa thành công, False nếu không tìm thấy.
        """
        ...

    @abstractmethod
    def get_tree_snapshot(self) -> dict:
        """
        Lấy snapshot cấu trúc B-Tree hiện tại để visualize.

        Returns:
            Dict chứa cấu trúc cây (root, size, order).
        """
        ...

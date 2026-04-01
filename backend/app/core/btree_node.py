"""
- Module định nghĩa cấu trúc Node của cây B-Tree bậc 3.
- Mỗi Node chỉ chứa tối đa 2 khóa và 3 nhánh con.
- Module này được thiết kế hoàn toàn độc lập và không phụ thuộc bất kỳ layer nào khác.
- Mục đích chính là thiết kế theo chuẩn SOLID, cụ thể là Single Responsibility - chỉ chịu trách nhiệm mô tả cấu trúc dữ liệu Node của cây B-Tree bậc 3.
"""

# Sử dụng tham chiếu chéo, cho phép sử dụng tên của 1 Class làm kiểu dữ liệu ngay cả khi Class đó chưa được định nghĩa.
# annotations cũng có tác dụng tương tự với hàm
from __future__ import annotations

# Dùng dataclass để tự sinh các hàm constructor như __init__, __repr__,... mà không cần phải tự định nghĩa.
# Dùng field để đảm bảo mỗi một Node được khởi tạo đều chứa một danh sách Key mới của riêng Node đó.
from dataclasses import dataclass, field

# Optinal cho phép kiểu dữ liệu có thể mang giá trị None.
from typing import Optional


@dataclass
class BTreeNode:
    """
    Một node trong cây B-Tree bậc 3.

    Attributes:
        keys: Danh sách các khóa (student_id) trong node, chứa tối đa 2 phần tử.
        children: Danh sách các node con, chứa tối đa 3 phần tử.
        parent: Tham chiếu đến node cha, node cha sẽ có giá trị là None nếu node hiện thời là node root.
    """

    keys: list[int] = field(default_factory=list)
    children: list[Optional["BTreeNode"]] = field(default_factory=list)
    parent: Optional["BTreeNode"] = field(default=None, repr=False)

    # Các Properties kiểm tra trạng thái node.
    # Các Properties cho phép gọi hàm như là 1 biến thuộc tính của đối tượng, giúp code sạch, dễ đọc, dễ bảo trì hơn
    @property
    def is_leaf(self) -> bool:
        """Trả về True nếu node là lá (không có con)."""
        return len(self.children) == 0

    @property
    def is_full(self) -> bool:
        """Trả về True nếu node đã đầy (có 2 khóa — số lượng khóa tối đa của bậc 3)."""
        return len(self.keys) == 2

    @property
    def is_overflow(self) -> bool:
        """Trả về True nếu node bị tràn sau khi insert (có từ 3 khóa trở lên)."""
        return len(self.keys) == 3

    @property
    def is_deficient(self) -> bool:
        """Trả về True nếu node bị thiếu khóa - tức là không đủ số lượng khóa tối thiểu (có 0 khóa — cần phải gộp hoặc mượn)."""
        return len(self.keys) == 0

    @property
    def is_root(self) -> bool:
        """Trả về True nếu node là root."""
        return self.parent is None

    # Serialization
    # Mục đích chính là chuyển đổi một Node trong cây BTree thành một dictionary để FastAPI có thể hiểu được và chuyển cho Frontend.

    def to_dict(self) -> dict:
        """
        Chuyển node đang xét hiện thời và toàn bộ các cây con bên dưới của nó thành kiểu dữ liệu dictionary.
        Dùng để serialize trả về Frontend qua API (FastAPI).

        Returns:
            dict: chứa danh sách khóa của node hiện thời và danh sách các con của nó (sử dụng đệ quy để duyệt).
        """
        return {
            "keys": list(self.keys),
            "children": [child.to_dict() for child in self.children],
        }

"""
Module này được sử dụng để cài đặt cây B-Tree bậc 3 hoàn chỉnh.

Hỗ trợ các thao tác:
- insert(key): Chèn key mới, tự động split khi tràn.
- search(key): Tìm kiếm key, trả về node chứa key đó.
- delete(key): Xóa key, tự động merge/borrow để cân bằng cây.
- get_snapshot(): Trả về toàn bộ cấu trúc cây dưới dạng dict.

SOLID áp dụng:
- Single Responsibility: Module chỉ lo thuật toán B-Tree.
- Open/Closed: Có thể mở rộng thêm traverse, range_search mà không cần sửa các method hiện tại.
- Dependency Inversion: Chỉ phụ thuộc vào BTreeNode (abstraction trong cùng layer core/), không phụ thuộc layer ngoài.
- Tức là lõi thuật toán BTree cứ chạy mà không cần quan tâm các Framework bên ngoài là gì.
- Giúp source code BTree có thể dễ dàng tích hợp các Framework khác mà không cần phải xây lại từ đầu
"""

from __future__ import annotations
from typing import Optional
from app.core.btree_node import BTreeNode


class BTree:
    """
    Cây B-Tree bậc 3 (còn gọi là 2-3 Tree).

    Bậc 3 nghĩa là:
    - Mỗi node có tối đa 2 keys.
    - Mỗi node có tối đa 3 children.
    - Mỗi node (trừ root) có tối thiểu 1 key.
    """

    def __init__(self) -> None:
        """Khởi tạo cây rỗng với root là None."""
        self._root: Optional[BTreeNode] = None
        self._size: int = 0  # Tổng số keys trong cây.

    @property
    def root(self) -> Optional[BTreeNode]:
        """Truy cập root node (read-only từ bên ngoài)."""
        return self._root

    @property
    def size(self) -> int:
        """Tổng số keys đang lưu trong cây."""
        return self._size

    def insert(self, key: int) -> bool:
        """
        Chèn một key mới vào cây B-Tree.

        Args:
            key: Giá trị nguyên cần chèn (student_id).

        Returns:
            True nếu chèn thành công, False nếu key đã tồn tại.
        """
        if self._root is None:
            # Trường hợp cây rỗng: tạo root mới
            self._root = BTreeNode(keys=[key])
            self._size += 1
            return True

        # Kiểm tra key đã tồn tại chưa
        if self.search(key) is not None:
            return False

        # Tìm node lá phù hợp để chèn
        leaf = self._find_leaf(self._root, key)

        # Chèn key vào node lá (luôn giữ thứ tự tăng dần)
        self._insert_into_node(leaf, key)
        self._size += 1

        # Xử lý overflow nếu node lá bị tràn
        if leaf.is_overflow:
            self._split(leaf)

        return True

    def search(self, key: int) -> Optional[BTreeNode]:
        """
        Tìm kiếm key trong cây.

        Args:
            key: Giá trị cần tìm.

        Returns:
            Node chứa key nếu tìm thấy, None nếu không tìm thấy.
        """
        return self._search_recursive(self._root, key)

    def delete(self, key: int) -> bool:
        """
        Xóa một key khỏi cây B-Tree.

        Args:
            key: Giá trị cần xóa.

        Returns:
            True nếu xóa thành công, False nếu key không tồn tại.
        """
        if self._root is None:
            return False

        node = self._search_recursive(self._root, key)
        if node is None:
            return False

        self._delete_key(node, key)
        self._size -= 1
        return True

    def get_snapshot(self) -> dict:
        """
        Trả về toàn bộ cấu trúc cây dưới dạng dict để serialize.

        Returns:
            Dict chứa root node (đệ quy) và metadata.
        """
        return {
            "root": self._root.to_dict() if self._root else None,
            "size": self._size,
            "order": 3,
        }

    def get_all_keys(self) -> list[int]:
        """
        Duyệt cây theo thứ tự (in-order) và trả về tất cả keys.

        Returns:
            Danh sách keys được sắp xếp tăng dần.
        """
        result: list[int] = []
        self._inorder(self._root, result)
        return result

    # Các hàm nội bộ (Private)
    # Các hàm này được cài đặt với mục đích chạy dưới lõi Backend, hỗ trợ nhiều thao tác quan trọng trong việc xây dựng cây

    # Các hàm hỗ trợ cho việc tìm kiếm (Search)

    def _find_leaf(self, node: BTreeNode, key: int) -> BTreeNode:
        """
        Tìm node lá phù hợp để chèn key.

        Thuật toán: Đi từ root xuống lá, rẽ nhánh dựa trên so sánh key.

        Args:
            node: Node bắt đầu tìm kiếm (thường là root).
            key: Key cần chèn.

        Returns:
            Node lá phù hợp nhất để chèn key.
        """
        if node.is_leaf:
            return node

        # Xác định index của child cần đi xuống
        child_index = self._find_child_index(node, key)
        return self._find_leaf(node.children[child_index], key)

    def _find_child_index(self, node: BTreeNode, key: int) -> int:
        """
        Xác định index của child phù hợp để đi xuống khi tìm kiếm/insert.

        Logic:
        - Nếu key < keys[0] ta sẽ đi xuống children[0] (Nhánh bên trái)
        - Nếu node có 2 keys và keys[0] <= key < keys[1] ta sẽ đi xuống children[1] (Nhánh ở giữa)
        - Ngược lại tất cả trường hợp trên, ta sẽ đi xuống children[2] cuối cùng (Nhánh bên phải)

        Args:
            node: Node hiện tại.
            key: Key cần xác định hướng đi.

        Returns:
            Index của child phù hợp.
        """
        for i, k in enumerate(node.keys):
            if key < k:
                return i
        return len(node.keys)

    def _search_recursive(
        self, node: Optional[BTreeNode], key: int
    ) -> Optional[BTreeNode]:
        """
        Tìm kiếm key đệ quy trong cây.

        Args:
            node: Node hiện tại đang xét.
            key: Key cần tìm.

        Returns:
            Node chứa key nếu tìm thấy, None nếu không.
        """
        if node is None:
            return None

        if key in node.keys:
            return node

        if node.is_leaf:
            return None

        child_index = self._find_child_index(node, key)
        return self._search_recursive(node.children[child_index], key)

    def _inorder(self, node: Optional[BTreeNode], result: list[int]) -> None:
        """
        Duyệt cây theo thứ tự in-order để lấy tất cả keys.

        Args:
            node: Node hiện tại.
            result: List tích lũy kết quả (truyền tham chiếu).
        """
        # Nếu Node là null
        if node is None:
            return
        # Nếu Node là lá, không còn nhánh con, nhặt hết khóa
        if node.is_leaf:
            result.extend(node.keys)
            return

        for i, key in enumerate(node.keys):
            """
            Vòng lặp sẽ nhặt khóa theo thứ tự:
            - Nhặt khóa bên nhánh con trái[0]
            - Nhặt khóa đầu tiên của Node hiện thời
            - Nhặt khóa ở nhánh con giữa[1]
            - Nhặt khóa thứ hai của Node hiện thời
            """
            self._inorder(node.children[i], result)
            result.append(key)

        # Nhặt khóa ở nhánh con cuối cùng[2]
        self._inorder(node.children[len(node.keys)], result)

    # Các hàm hỗ trợ cho việc thêm Node (Insert)

    def _insert_into_node(self, node: BTreeNode, key: int) -> None:
        """
        Chèn key vào node theo thứ tự tăng dần.

        Args:
            node: Node cần chèn key vào.
            key: Key cần chèn.
        """
        node.keys.append(key)
        # Sắp xếp lại theo thứ tự tăng dần
        node.keys.sort()

    def _split(self, node: BTreeNode) -> None:
        """
        Xử lý overflow: tách node thành 2 và đẩy key giữa lên cha.

        Với B-Tree bậc 3, khi node có 3 keys [k0, k1, k2]:
        - k1 (key giữa) được đẩy lên node cha.
        - Node trái giữ [k0].
        - Node phải giữ [k2].
        - Children được phân phối tương ứng.

        Args:
            node: Node bị overflow (đang có 3 keys).
        """
        # Key giữa sẽ được đẩy lên cha
        mid_key = node.keys[1]

        # Tạo node phải chứa key bên phải key giữa
        right_node = BTreeNode(keys=[node.keys[2]])

        # Node hiện tại (trái) giữ lại key bên trái key giữa
        node.keys = [node.keys[0]]

        # Phân phối các children nếu node không phải lá
        if not node.is_leaf:
            # Children[2] và children[3] thuộc về right_node
            right_node.children = node.children[2:]
            # Children[0] và children[1] thuộc về left_node (Node hiện thời)
            node.children = node.children[:2]

            # Cập nhật parent reference cho children của right_node
            for child in right_node.children:
                child.parent = right_node

        # Xử lý node cha
        # Nếu node bị split là node root
        if node.is_root:
            # Tạo root mới
            new_root = BTreeNode(keys=[mid_key])
            new_root.children = [node, right_node]
            # Cập nhật parent reference
            node.parent = new_root
            right_node.parent = new_root
            # Cập nhật root mới
            self._root = new_root
        else:
            # Chèn mid_key lên node cha
            parent = node.parent
            right_node.parent = parent

            # Tìm vị trí của node trong danh sách children của cha
            node_index = parent.children.index(node)

            # Ở đây ta gọi các hàm insert mặc định của List, không phải hàm insert của cây BTree được xây dựng phía trên
            # Chèn mid_key vào cha theo đúng vị trí
            parent.keys.insert(node_index, mid_key)
            # Chèn right_node vào sau node hiện tại
            parent.children.insert(node_index + 1, right_node)

            # Nếu cha cũng bị overflow, tiếp tục đệ quy và split lên trên
            if parent.is_overflow:
                self._split(parent)

    # Các hàm hỗ trợ cho việc xóa Node ra khỏi cây (Delete)

    def _delete_key(self, node: BTreeNode, key: int) -> None:
        """
        Xóa key khỏi node và xử lý các trường hợp mất cân bằng.

        Có 2 trường hợp chính:
        1. Node là lá: Xóa trực tiếp rồi kiểm tra Node có đủ khóa tối thiểu không.
        2. Node là node trong: Tìm Key ở Node lá thay thế và sau đó thực hiện xóa Key ở Node lá.

        Args:
            node: Node chứa key cần xóa.
            key: Key cần xóa.
        """
        if node.is_leaf:
            node.keys.remove(key)
            # Kiểm tra nếu node thiếu key và không phải root
            # Ta thấy các properties được tận dụng triệt để
            if node.is_deficient and not node.is_root:
                self._fix_deficiency(node)
        else:
            # Node trong: tìm Key của Node lá thay thế (Khóa nhỏ nhất của Node lá nằm bên phải)
            key_index = node.keys.index(key)
            successor_node = self._find_min_leaf(node.children[key_index + 1])
            successor_key = successor_node.keys[0]

            # Thay key cần xóa bằng key thay thế
            node.keys[key_index] = successor_key

            # Xóa key ở node lá
            self._delete_key(successor_node, successor_key)

    def _find_min_leaf(self, node: BTreeNode) -> BTreeNode:
        """
        Tìm node lá có key nhỏ nhất trong cây con bắt đầu từ node.

        Args:
            node: Root của cây con cần tìm.

        Returns:
            Node lá ngoài cùng bên trái.
        """
        if node.is_leaf:
            return node
        return self._find_min_leaf(node.children[0])

    def _fix_deficiency(self, node: BTreeNode) -> None:
        """
        Sửa node bị deficient (không còn key) sau khi xóa.

        Thử theo thứ tự ưu tiên:
        1. Borrow from left sibling (mượn từ anh em bên trái).
        2. Borrow from right sibling (mượn từ anh em bên phải).
        3. Merge with a sibling (gộp với anh em).

        Args:
            node: Node đang bị deficient.
        """
        parent = node.parent
        node_index = parent.children.index(node)

        # Xác định anh em bên trái và phải
        left_sibling = parent.children[node_index - 1] if node_index > 0 else None
        right_sibling = (
            parent.children[node_index + 1]
            if node_index < len(parent.children) - 1
            else None
        )

        if left_sibling and len(left_sibling.keys) > 1:
            # Ưu tiên 1: Borrow from left sibling
            self._borrow_from_left(node, left_sibling, parent, node_index)

        elif right_sibling and len(right_sibling.keys) > 1:
            # Ưu tiên 2: Borrow from right sibling
            self._borrow_from_right(node, right_sibling, parent, node_index)

        elif left_sibling:
            # Ưu tiên 3a: Merge với left sibling
            self._merge(left_sibling, node, parent, node_index - 1)

        else:
            # Ưu tiên 3b: Merge với right sibling
            self._merge(node, right_sibling, parent, node_index)

    def _borrow_from_left(
        self,
        node: BTreeNode,
        left_sibling: BTreeNode,
        parent: BTreeNode,
        node_index: int,
    ) -> None:
        """
        Mượn key từ anh em bên trái thông qua node cha (rotation phải).

        Luồng chạy như sau: left_sibling.keys[-1] → parent.keys[node_index-1] → node.keys[0]

        Args:
            node: Node đang thiếu key.
            left_sibling: Anh em bên trái có thể cho mượn.
            parent: Node cha chung.
            node_index: Vị trí của node trong children của cha.
        """
        # Key từ cha xuống node
        node.keys.insert(0, parent.keys[node_index - 1])

        # Key lớn nhất của left_sibling lên cha
        parent.keys[node_index - 1] = left_sibling.keys.pop()

        # Nếu left_sibling có children, chuyển child cuối sang node
        if not left_sibling.is_leaf:
            child_to_move = left_sibling.children.pop()
            child_to_move.parent = node
            node.children.insert(0, child_to_move)

    def _borrow_from_right(
        self,
        node: BTreeNode,
        right_sibling: BTreeNode,
        parent: BTreeNode,
        node_index: int,
    ) -> None:
        """
        Mượn key từ anh em bên phải thông qua node cha (rotation trái).

        Luồng chạy như sau: right_sibling.keys[0] → parent.keys[node_index] → node.keys[-1]

        Args:
            node: Node đang thiếu key.
            right_sibling: Anh em bên phải có thể cho mượn.
            parent: Node cha chung.
            node_index: Vị trí của node trong children của cha.
        """
        # Key từ cha xuống node
        node.keys.append(parent.keys[node_index])

        # Key nhỏ nhất của right_sibling lên cha
        parent.keys[node_index] = right_sibling.keys.pop(0)

        # Nếu right_sibling có children, chuyển child đầu sang node
        if not right_sibling.is_leaf:
            child_to_move = right_sibling.children.pop(0)
            child_to_move.parent = node
            node.children.append(child_to_move)

    def _merge(
        self,
        left_node: BTreeNode,
        right_node: BTreeNode,
        parent: BTreeNode,
        parent_key_index: int,
    ) -> None:
        """
        Gộp left_node và right_node thành một node duy nhất.

        Kéo separator key từ cha xuống node gộp.
        Sau merge, nếu Node cha bị thiếu khóa, tiếp tục đệ quy lên trên.

        Args:
            left_node: Node bên trái (sẽ là node kết quả sau merge).
            right_node: Node bên phải (sẽ bị xóa sau merge).
            parent: Node cha chung.
            parent_key_index: Index của separator key trong cha.
        """
        # Kéo separator key từ cha xuống left_node
        left_node.keys.append(parent.keys.pop(parent_key_index))

        # Chuyển toàn bộ keys và children của right_node sang left_node
        left_node.keys.extend(right_node.keys)
        if not right_node.is_leaf:
            for child in right_node.children:
                child.parent = left_node
            left_node.children.extend(right_node.children)

        # Xóa right_node khỏi danh sách children của cha
        parent.children.pop(parent_key_index + 1)

        # Xử lý node cha sau khi mất một key
        if parent.is_root:
            if not parent.keys:
                # Root rỗng thì left_node sẽ trở thành root mới
                self._root = left_node
                left_node.parent = None
        elif parent.is_deficient:
            self._fix_deficiency(parent)

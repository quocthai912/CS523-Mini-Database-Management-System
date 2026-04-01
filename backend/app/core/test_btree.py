"""
Source code này được dùng để kiểm thử lõi thuật toán cây BTree
Tránh trường hợp lõi thuật toán xây dựng sai, dẫn tới việc ảnh hưởng toàn bộ hệ thống
"""

from app.core.btree import BTree


# In cây để kiểm thử
def print_tree(node, level: int = 0, prefix: str = "Root: ") -> None:
    """In cây ra terminal theo dạng cây thư mục."""
    if node is None:
        print(" " * (level * 4) + prefix + "None")
        return
    print(" " * (level * 4) + prefix + str(node.keys))
    for i, child in enumerate(node.children):
        print_tree(child, level + 1, prefix=f"Child[{i}]: ")


# Kiểm tra thêm khóa
def test_insert() -> None:
    print("\n" + "=" * 50)
    print("TEST 1: INSERT")
    print("=" * 50)

    tree = BTree()
    keys = [10, 20, 5, 6, 12, 30, 7, 17]

    for key in keys:
        result = tree.insert(key)
        print(f"Insert {key:>3}: {'OK' if result else 'DUPLICATE'}")

    print(f"\nTree size: {tree.size}")
    print(f"All keys (sorted): {tree.get_all_keys()}")
    print("\nTree structure:")
    print_tree(tree.root)

    # Kiểm tra thêm trùng khóa
    dup = tree.insert(10)
    print(f"\nInsert duplicate 10: {'OK' if dup else 'DUPLICATE (correct!)'}")


# Kiểm tra việc tìm kiếm khóa trên cây
def test_search() -> None:
    print("\n" + "=" * 50)
    print("TEST 2: SEARCH")
    print("=" * 50)

    tree = BTree()
    for key in [10, 20, 5, 6, 12, 30, 7, 17]:
        tree.insert(key)

    for key in [10, 15, 30, 99]:
        result = tree.search(key)
        found = result is not None
        print(
            f"Search {key:>3}: {'FOUND in node ' + str(result.keys) if found else 'NOT FOUND'}"
        )


# Kiểm tra xóa khóa trên cây
def test_delete() -> None:
    print("\n" + "=" * 50)
    print("TEST 3: DELETE")
    print("=" * 50)

    tree = BTree()
    for key in [10, 20, 5, 6, 12, 30, 7, 17]:
        tree.insert(key)

    print("Before delete:", tree.get_all_keys())
    print("Tree structure:")
    print_tree(tree.root)

    for key in [6, 20, 10]:
        result = tree.delete(key)
        print(f"\nDelete {key}: {'OK' if result else 'NOT FOUND'}")
        print(f"Keys remaining: {tree.get_all_keys()}")
        print("Tree structure:")
        print_tree(tree.root)


def test_snapshot() -> None:
    print("\n" + "=" * 50)
    print("TEST 4: SNAPSHOT (for API)")
    print("=" * 50)

    tree = BTree()
    for key in [10, 20, 5]:
        tree.insert(key)

    import json

    snapshot = tree.get_snapshot()
    print(json.dumps(snapshot, indent=2))


if __name__ == "__main__":
    test_insert()
    test_search()
    test_delete()
    test_snapshot()

"""
Script được dùng để kiểm thử BTreeStudentRepository.
"""

from app.domain.entities import Student, Gender
from app.repository.student_repository import BTreeStudentRepository
import json


def make_student(sid: int, name: str, gpa: float = 3.0) -> Student:
    """Helper tạo Student entity nhanh."""
    return Student(
        student_id=sid,
        full_name=name,
        gender=Gender.MALE,
        major="Computer Science",
        gpa=gpa,
        email=f"s{sid}@university.edu",
    )


def test_insertion_order() -> None:
    print("\n" + "=" * 50)
    print("TEST 1: INSERTION ORDER vs SORTED ORDER")
    print("=" * 50)

    repo = BTreeStudentRepository()

    # Thêm theo thứ tự ngẫu nhiên
    order = [22005, 22001, 22003, 22002, 22004]
    for sid in order:
        repo.add(make_student(sid, f"Student {sid}"))

    print(f"Thứ tự thêm vào : {order}")

    display = [s.student_id for s in repo.find_all()]
    print(f"find_all()       : {display} phải giống thứ tự thêm vào")

    sorted_list = [s.student_id for s in repo.get_sorted_students()]
    print(f"get_sorted()     : {sorted_list} B-Tree sorted tăng dần")

    assert display == order, "FAIL: find_all() không đúng thứ tự!"
    assert sorted_list == sorted(order), "FAIL: get_sorted() không đúng!"
    print("PASS")


def test_add_duplicate() -> None:
    print("\n" + "=" * 50)
    print("TEST 2: DUPLICATE CHECK")
    print("=" * 50)

    repo = BTreeStudentRepository()
    repo.add(make_student(22001, "Nguyen Van An"))
    dup = repo.add(make_student(22001, "Duplicate"))
    print(f"Add duplicate 22001: {'DUPLICATE (correct!)' if not dup else 'FAIL'}")
    print(f"Total count vẫn là 1: {repo.total_count == 1}")
    print("PASS" if not dup and repo.total_count == 1 else "FAIL")


def test_update_keeps_order() -> None:
    print("\n" + "=" * 50)
    print("TEST 3: UPDATE GIỮ NGUYÊN THỨ TỰ")
    print("=" * 50)

    repo = BTreeStudentRepository()
    for sid in [22003, 22001, 22002]:
        repo.add(make_student(sid, f"Student {sid}"))

    before = [s.student_id for s in repo.find_all()]

    updated = make_student(22001, "Nguyen Van An UPDATED", gpa=3.9)
    repo.update(updated)

    after = [s.student_id for s in repo.find_all()]
    found = repo.find_by_id(22001)

    print(f"Thứ tự trước update : {before}")
    print(f"Thứ tự sau update   : {after} phải giống nhau")
    print(f"Tên sau update      : {found.full_name}")

    assert before == after, "FAIL: thứ tự thay đổi sau update!"
    print("PASS")


def test_remove_updates_order() -> None:
    print("\n" + "=" * 50)
    print("TEST 4: REMOVE CẬP NHẬT THỨ TỰ")
    print("=" * 50)

    repo = BTreeStudentRepository()
    for sid in [22003, 22001, 22002]:
        repo.add(make_student(sid, f"Student {sid}"))

    print(f"Trước xóa  : {[s.student_id for s in repo.find_all()]}")
    repo.remove(22001)
    after = [s.student_id for s in repo.find_all()]
    print(f"Sau xóa 22001: {after} phải là [22003, 22002]")

    assert after == [22003, 22002], "FAIL: thứ tự sau xóa sai!"
    print("PASS")


def test_find_by_name() -> None:
    print("\n" + "=" * 50)
    print("TEST 5: FIND BY NAME")
    print("=" * 50)

    repo = BTreeStudentRepository()
    repo.add(make_student(22001, "Nguyen Van An"))
    repo.add(make_student(22002, "Tran Thi Bich"))
    repo.add(make_student(22003, "Nguyen Thi Cam"))

    results = repo.find_by_name("nguyen")
    print(f"Search 'nguyen': {[s.full_name for s in results]}")
    assert len(results) == 2

    results2 = repo.find_by_name("BICH")
    print(f"Search 'BICH'  : {[s.full_name for s in results2]}")
    assert len(results2) == 1

    results3 = repo.find_by_name("xyz")
    print(f"Search 'xyz'   : {results3} (correct!)")
    assert len(results3) == 0
    print("PASS")


def test_tree_snapshot() -> None:
    print("\n" + "=" * 50)
    print("TEST 6: TREE SNAPSHOT")
    print("=" * 50)

    repo = BTreeStudentRepository()
    for sid in [22001, 22002, 22003, 22004, 22005]:
        repo.add(make_student(sid, f"Student {sid}"))

    snapshot = repo.get_tree_snapshot()
    print(json.dumps(snapshot, indent=2))
    print("PASS")


if __name__ == "__main__":
    test_insertion_order()
    test_add_duplicate()
    test_update_keeps_order()
    test_remove_updates_order()
    test_find_by_name()
    test_tree_snapshot()

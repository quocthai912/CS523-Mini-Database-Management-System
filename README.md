<p align="center">
  <a href="https://www.uit.edu.vn/" title="Trường Đại học Công nghệ Thông tin" style="border: none;">
    <img src="https://i.imgur.com/WmMnSRt.png" alt="Trường Đại học Công nghệ Thông tin | University of Information Technology">
  </a>
</p>
<h1 align="center">CS523 - CẤU TRÚC DỮ LIỆU VÀ GIẢI THUẬT NÂNG CAO</h1>

# MINI DATABASE MANAGEMENT SYSTEM
![React](https://img.shields.io/badge/Frontend-ReactJS-61DAFB?style=flat-square&logo=react)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi)
![Python](https://img.shields.io/badge/Language-Python_3.x-3776AB?style=flat-square&logo=python)
> +	Ứng dụng Web Mini Database Management System là một hệ thống quản lý sinh viên kết hợp minh họa trực quan thuật toán đánh chỉ mục bằng Cây B-Tree bậc 3 (2-3 Tree). Ứng dụng được xây dựng theo kiến trúc Clean Architecture và tuân thủ nghiêm túc các nguyên tắc SOLID.
> +	Mục tiêu chính của ứng dụng là minh họa cách một hệ quản trị cơ sở dữ liệu thực tế sử dụng cấu trúc B-Tree để đánh chỉ mục và tăng tốc độ tìm kiếm. Mỗi thao tác thêm, sửa, xóa trên danh sách sinh viên đều được phản ánh trực tiếp lên cấu trúc cây B-Tree hiển thị trên giao diện, giúp người dùng quan sát rõ ràng cách cây tự cân bằng thông qua các thao tác Split, Merge và Borrow.

LINK DEMO: https://www.cs523-quocthai-minidbms.me/
---
## 1. GIỚI THIỆU MÔN HỌC:
| | |
|---|---|
| **Môn học** | Cấu Trúc Dữ Liệu Và Giải Thuật Nâng Cao |
| **Mã lớp** | CS523.Q21 |
| **Giảng viên** | ThS. Nguyễn Thanh Sơn |
| **Sinh viên** | Tô Quốc Thái |
| **MSSV** | 24521598 |
---

## 2. MÔ TẢ DỰ ÁN:
### Quản lý dữ liệu sinh viên:
  + Thêm mới sinh viên với đầy đủ thông tin: Mã sinh viên, Họ tên, Giới tính, Ngành học, GPA, Email.
  + Chỉnh sửa thông tin sinh viên đã có trong hệ thống.
  + Xóa sinh viên khỏi hệ thống với xác nhận qua hộp thoại hiển thị câu lệnh SQL tương ứng.
### Minh họa cấu trúc B-Tree bậc 3 (2-3 Tree):
  + Trực quan hóa cấu trúc cây B-Tree theo thời gian thực sau mỗi thao tác thêm/xóa.
  + Phân biệt trực quan Root Node (màu cam), Internal Nodes và Leaf Nodes (màu xanh lá).
  + Highlight node chứa kết quả tìm kiếm hoặc node vừa được thêm vào.
  + Quan sát cây tự động tái cân bằng thông qua các thao tác Split, Merge và Borrow.
### Tìm kiếm và lọc dữ liệu:
  + Tìm kiếm sinh viên theo Tên với độ phức tạp O(n).
  + Tìm kiếm sinh viên theo Mã số sinh viên sử dụng thuật toán tìm kiếm B-Tree với độ phức tạp O(logn).
### Hai chế độ hiển thị dữ liệu:
  + Insertion Order: Hiển thị danh sách sinh viên theo thứ tự thêm vào hệ thống.
  + Sort by ID: Hiển thị danh sách sinh viên theo thứ tự Mã số sinh viên tăng dần, sử dụng kết quả in-order traversal của cây B-Tree.
### Phiên làm việc độc lập (Session-based Isolation):
  + Mỗi người dùng khi truy cập hệ thống được cấp một Session ID riêng biệt, lưu trữ trong localStorage của trình duyệt.
  + Dữ liệu và cấu trúc B-Tree của mỗi người dùng hoàn toàn độc lập với nhau.
### Giao diện Enterprise DBMS:
  + Thiết kế theo phong cách SQL Server Management Studio / pgAdmin.
  + Hiển thị câu lệnh SQL tương ứng với từng thao tác người dùng thực hiện.
  + Trạng thái kết nối Backend được hiển thị realtime trên Title Bar.
---

## 3. CÔNG NGHỆ SỬ DỤNG:
| Phần | Công nghệ |
|---|---|
| **Backend** | Python 3.11, FastAPI, Uvicorn, Pydantic |
| **Frontend** | React, TypeScript, Vite, Tailwind CSS |
| **Thuật toán** | B-Tree bậc 3 (2-3 Tree) |
| **State Management** | Zustand |
| **HTTP Client** | Axios |
| **Deploy Backend** | DigitalOcean App Platform |
| **Deploy Frontend** | Vercel |
| **Custom Domain** | Namecheap (.me) |
---

## 4. CẤU TRÚC DỰ ÁN:
```
CS523-Mini-Database-Management-System/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── btree_node.py        # Cấu trúc dữ liệu Node của B-Tree
│   │   │   └── btree.py             # Thuật toán B-Tree (Insert, Search, Delete, Split, Merge, Borrow)
│   │   ├── domain/
│   │   │   ├── entities.py          # Domain Entities (Student, Gender)
│   │   │   └── interfaces.py        # Abstract Interface IStudentRepository
│   │   ├── repository/
│   │   │   └── student_repository.py # Cài đặt Repository dùng B-Tree làm storage engine
│   │   ├── service/
│   │   │   └── student_service.py   # Business Logic và Validation
│   │   ├── api/
│   │   │   ├── schemas.py           # Pydantic Schemas cho Request/Response
│   │   │   ├── dependencies.py      # Dependency Injection và Session Management
│   │   │   └── student_router.py    # FastAPI Routers định nghĩa HTTP endpoints
│   │   └── main.py                  # Entry point FastAPI, CORS Middleware
│   ├── Dockerfile                   # Cấu hình Docker để deploy lên DigitalOcean
│   └── requirements.txt             # Các thư viện Python cần thiết
├── frontend/
│   ├── src/
│   │   ├── domain/
│   │   │   └── types.ts             # TypeScript Interfaces và Types
│   │   ├── services/
│   │   │   └── studentApi.ts        # API Service Layer (Axios)
│   │   ├── store/
│   │   │   └── studentStore.ts      # Global State Management (Zustand)
│   │   ├── components/
│   │   │   ├── ui/
│   │   │   │   └── Badge.tsx        # GenderBadge, GpaBadge components
│   │   │   ├── student/
│   │   │   │   ├── StudentForm.tsx  # Form thêm/sửa sinh viên
│   │   │   │   ├── StudentTable.tsx # Bảng dữ liệu SQL-style
│   │   │   │   └── DeleteModal.tsx  # Modal xác nhận xóa
│   │   │   └── btree/
│   │   │       └── BTreeCanvas.tsx  # Vẽ cây B-Tree bằng SVG
│   │   ├── index.css                # Global CSS, Font, Utility Classes
│   │   └── App.tsx                  # Root Component, Layout, State Orchestration
│   ├── vite.config.ts               # Cấu hình Vite và Path Aliases
│   ├── tsconfig.app.json            # Cấu hình TypeScript
│   └── package.json                 # Dependencies và Scripts
└── .gitignore
```
---
## 5. GIẤY PHÉP:
Dự Án Được Thực Hiện Cho Mục Đích Học Thuật - Môn Cấu Trúc Dữ Liệu Và Giải Thuật Nâng Cao (CS523) - Trường Đại Học Công Nghệ Thông Tin ĐHQG.TPHCM (UIT).


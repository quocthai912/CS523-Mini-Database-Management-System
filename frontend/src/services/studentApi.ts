/**
 * API Service layer — toàn bộ giao tiếp HTTP với Backend.
 */

import axios from "axios";
import type {
  ApiResponse,
  Student,
  StudentListData,
  BTreeSnapshot,
} from "@/domain/types";

const BASE_URL = import.meta.env.VITE_API_URL ?? "/api";

/** Lấy hoặc tạo session_id mới cho người dùng */
function getSessionId(): string {
  let sessionId = localStorage.getItem("session_id");
  if (!sessionId) {
    sessionId = crypto.randomUUID();
    localStorage.setItem("session_id", sessionId);
  }
  return sessionId;
}

const api = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
  timeout: 15000,
});

/** Tự động thêm X-Session-Id vào mọi request */
api.interceptors.request.use((config) => {
  config.headers["X-Session-Id"] = getSessionId();
  return config;
});

export interface CreateStudentDto {
  student_id: number;
  full_name: string;
  gender: string;
  major: string;
  gpa: number;
  email: string;
}

export interface UpdateStudentDto {
  full_name: string;
  gender: string;
  major: string;
  gpa: number;
  email: string;
}

export const studentApi = {
  getAll: async (): Promise<StudentListData> => {
    const res = await api.get<ApiResponse<StudentListData>>("/students");
    return res.data.data!;
  },

  searchByName: async (name: string): Promise<StudentListData> => {
    const res = await api.get<ApiResponse<StudentListData>>(
      "/students/search",
      {
        params: { name },
      },
    );
    return res.data.data!;
  },

  searchById: async (id: number): Promise<Student | null> => {
    try {
      const res = await api.get<ApiResponse<Student>>(`/students/${id}`);
      return res.data.data!;
    } catch {
      return null;
    }
  },

  getById: async (id: number): Promise<Student> => {
    const res = await api.get<ApiResponse<Student>>(`/students/${id}`);
    return res.data.data!;
  },

  create: async (dto: CreateStudentDto): Promise<Student> => {
    const res = await api.post<ApiResponse<Student>>("/students", dto);
    return res.data.data!;
  },

  update: async (id: number, dto: UpdateStudentDto): Promise<Student> => {
    const res = await api.put<ApiResponse<Student>>(`/students/${id}`, dto);
    return res.data.data!;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/students/${id}`);
  },

  getTreeSnapshot: async (): Promise<BTreeSnapshot> => {
    const res = await api.get<{ success: boolean; data: BTreeSnapshot }>(
      "/students/tree",
    );
    return res.data.data;
  },

  /** Xóa session hiện tại — tạo session mới khi gọi lại */
  resetSession: (): void => {
    localStorage.removeItem("session_id");
  },
};

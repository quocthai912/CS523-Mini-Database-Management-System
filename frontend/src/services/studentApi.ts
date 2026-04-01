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

const api = axios.create({
  baseURL: "/api",
  headers: { "Content-Type": "application/json" },
  timeout: 10000,
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

  /** Search by Student ID — dùng GET /students/{id} */
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
};

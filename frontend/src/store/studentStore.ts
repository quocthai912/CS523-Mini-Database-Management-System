/**
 * Global state management dùng Zustand.
 *
 * Store chịu trách nhiệm:
 * - Lưu trữ danh sách sinh viên và B-Tree snapshot.
 * - Expose các actions để UI gọi (CRUD + fetch tree).
 * - Xử lý loading/error state tập trung.
 *
 * SOLID: Single Responsibility — chỉ lo state, không lo UI rendering.
 */

import { create } from "zustand";
import { studentApi } from "@/services/studentApi";
import type { Student, BTreeSnapshot } from "@/domain/types";
import type { CreateStudentDto, UpdateStudentDto } from "@/services/studentApi";

interface StudentState {
  students: Student[];
  treeSnapshot: BTreeSnapshot | null;
  isLoading: boolean;
  error: string | null;
  searchQuery: string;
  searchMode: "name" | "id" | "none";

  fetchStudents: () => Promise<void>;
  fetchTree: () => Promise<void>;
  createStudent: (dto: CreateStudentDto) => Promise<void>;
  updateStudent: (id: number, dto: UpdateStudentDto) => Promise<void>;
  deleteStudent: (id: number) => Promise<void>;
  searchStudents: (name: string) => Promise<Student[]>;
  searchStudentById: (id: number) => Promise<void>;
  clearSearch: () => Promise<void>;
  clearError: () => void;
}

export const useStudentStore = create<StudentState>((set) => ({
  students: [],
  treeSnapshot: null,
  isLoading: false,
  error: null,
  searchQuery: "",
  searchMode: "none",

  fetchStudents: async () => {
    set({ isLoading: true, error: null });
    try {
      const data = await studentApi.getAll();
      set({ students: data.students, isLoading: false });
    } catch {
      set({ error: "Failed to load student list.", isLoading: false });
    }
  },

  fetchTree: async () => {
    try {
      const snapshot = await studentApi.getTreeSnapshot();
      set({ treeSnapshot: snapshot });
    } catch {
      set({ error: "Failed to load B-Tree structure." });
    }
  },

  createStudent: async (dto) => {
    set({ isLoading: true, error: null });
    try {
      await studentApi.create(dto);
      const data = await studentApi.getAll();
      const snapshot = await studentApi.getTreeSnapshot();
      set({
        students: data.students,
        treeSnapshot: snapshot,
        isLoading: false,
      });
    } catch (err: unknown) {
      const msg =
        (err as { response?: { data?: { detail?: string } } })?.response?.data
          ?.detail ?? "Failed to create student.";
      set({ error: msg, isLoading: false });
      throw err;
    }
  },

  updateStudent: async (id, dto) => {
    set({ isLoading: true, error: null });
    try {
      await studentApi.update(id, dto);
      const data = await studentApi.getAll();
      set({ students: data.students, isLoading: false });
    } catch (err: unknown) {
      const msg =
        (err as { response?: { data?: { detail?: string } } })?.response?.data
          ?.detail ?? "Failed to update student.";
      set({ error: msg, isLoading: false });
      throw err;
    }
  },

  deleteStudent: async (id) => {
    set({ isLoading: true, error: null });
    try {
      await studentApi.delete(id);
      const data = await studentApi.getAll();
      const snapshot = await studentApi.getTreeSnapshot();
      set({
        students: data.students,
        treeSnapshot: snapshot,
        isLoading: false,
      });
    } catch {
      set({ error: "Failed to delete student.", isLoading: false });
    }
  },

  searchStudents: async (name) => {
    set({
      isLoading: true,
      error: null,
      searchQuery: name,
      searchMode: "name",
    });
    try {
      const data = await studentApi.searchByName(name);
      if (data.students.length === 0) {
        set({
          students: [],
          isLoading: false,
          error: `No student found with the name '${name}'.`,
        });
        return [];
      }
      set({ students: data.students, isLoading: false });
      return data.students;
    } catch {
      set({
        error: `No student found with the name '${name}'.`,
        isLoading: false,
      });
      return [];
    }
  },

  searchStudentById: async (id) => {
    set({
      isLoading: true,
      error: null,
      searchQuery: String(id),
      searchMode: "id",
    });
    try {
      const student = await studentApi.searchById(id);
      if (student) {
        set({ students: [student], isLoading: false });
      } else {
        set({
          students: [],
          isLoading: false,
          error: `Student ID ${id} not found.`,
        });
      }
    } catch {
      set({ error: `Student ID ${id} not found.`, isLoading: false });
    }
  },

  clearSearch: async () => {
    set({ searchQuery: "", searchMode: "none", error: null });
    const data = await studentApi.getAll();
    set({ students: data.students });
  },

  clearError: () => set({ error: null }),
}));

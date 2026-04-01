/**
 * Domain types cho Frontend.
 * Mirror của Backend domain entities.
 * Hoàn toàn độc lập với API layer và UI layer.
 */

export type Gender = "male" | "female" | "other";

export interface Student {
  student_id: number;
  full_name: string;
  gender: Gender;
  major: string;
  gpa: number;
  email: string;
}

export interface BTreeNode {
  keys: number[];
  children: BTreeNode[];
}

export interface BTreeSnapshot {
  root: BTreeNode | null;
  size: number;
  order: number;
}

/** Shape của mọi API response từ backend */
export interface ApiResponse<T = unknown> {
  success: boolean;
  message: string;
  data: T | null;
}

export interface StudentListData {
  students: Student[];
  total: number;
}

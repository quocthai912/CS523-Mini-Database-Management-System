/**
 * Form thêm - chỉnh sửa sinh viên.
 * SOLID — Single Responsibility: chỉ lo form UI + client validation.
 */

import { useState, useEffect } from "react";
import type { Student } from "@/domain/types";
import type { CreateStudentDto, UpdateStudentDto } from "@/services/studentApi";

interface StudentFormProps {
  editStudent: Student | null;
  onSubmit: (dto: CreateStudentDto | UpdateStudentDto) => Promise<void>;
  onCancelEdit: () => void;
}

const MAJORS = [
  "Computer Science",
  "Information Technology",
  "Software Engineering",
  "Data Science",
  "Artificial Intelligence",
  "Cybersecurity",
];

const EMPTY = {
  student_id: "",
  full_name: "",
  gender: "male",
  major: "Computer Science",
  gpa: "",
  email: "",
};

export function StudentForm({
  editStudent,
  onSubmit,
  onCancelEdit,
}: StudentFormProps) {
  const isEdit = !!editStudent;
  const [form, setForm] = useState(EMPTY);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [busy, setBusy] = useState(false);
  const [successMsg, setSuccessMsg] = useState("");

  useEffect(() => {
    if (editStudent) {
      setForm({
        student_id: String(editStudent.student_id),
        full_name: editStudent.full_name,
        gender: editStudent.gender,
        major: editStudent.major,
        gpa: String(editStudent.gpa),
        email: editStudent.email,
      });
    } else {
      setForm(EMPTY);
    }
    setErrors({});
    setSuccessMsg("");
  }, [editStudent]);

  const set = (key: string, val: string) =>
    setForm((f) => ({ ...f, [key]: val }));

  const validate = (): boolean => {
    const e: Record<string, string> = {};
    if (!isEdit) {
      const id = Number(form.student_id);
      if (!form.student_id || isNaN(id) || id <= 0)
        e.student_id = "Required. Must be a positive integer.";
    }
    if (!form.full_name.trim()) e.full_name = "Required.";
    const gpa = Number(form.gpa);
    if (!form.gpa || isNaN(gpa)) e.gpa = "Must be a number.";
    else if (gpa < 0 || gpa > 4) e.gpa = "Range: 0.0 – 4.0";
    if (!form.email.includes("@")) e.email = "Invalid email address.";
    setErrors(e);
    return Object.keys(e).length === 0;
  };

  const handleSubmit = async (ev: React.FormEvent) => {
    ev.preventDefault();
    if (!validate()) return;
    setBusy(true);
    setSuccessMsg("");
    try {
      if (isEdit) {
        await onSubmit({
          full_name: form.full_name.trim(),
          gender: form.gender,
          major: form.major,
          gpa: Number(form.gpa),
          email: form.email.trim(),
        } as UpdateStudentDto);
        setSuccessMsg("Record updated successfully.");
      } else {
        await onSubmit({
          student_id: Number(form.student_id),
          full_name: form.full_name.trim(),
          gender: form.gender,
          major: form.major,
          gpa: Number(form.gpa),
          email: form.email.trim(),
        } as CreateStudentDto);
        setSuccessMsg("Record inserted successfully.");
        setForm(EMPTY);
      }
    } catch {
      /* error handled by store */
    } finally {
      setBusy(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col h-full" noValidate>
      <div className="panel-header">
        <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
          {/* Add User Icon / Edit Icon */}
          {isEdit ? (
            <svg
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="none"
              stroke="#64748b"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
            </svg>
          ) : (
            <svg
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="none"
              stroke="#64748b"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
              <circle cx="9" cy="7" r="4" />
              <line x1="19" y1="8" x2="19" y2="14" />
              <line x1="16" y1="11" x2="22" y2="11" />
            </svg>
          )}
          <span>{isEdit ? "Edit Record" : "Insert New Record"}</span>
        </div>

        {isEdit && (
          <button
            type="button"
            onClick={onCancelEdit}
            style={{
              background: "none",
              border: "none",
              color: "#94a3b8",
              cursor: "pointer",
              fontSize: 16,
              lineHeight: 1,
              padding: "0 2px",
            }}
            title="Cancel edit"
          >
            ×
          </button>
        )}
      </div>

      <div
        style={{
          padding: "6px 12px",
          fontSize: 11,
          background: isEdit ? "#eff6ff" : "#f0fdf4",
          borderBottom: `1px solid ${isEdit ? "#bfdbfe" : "#bbf7d0"}`,
          color: isEdit ? "#1d4ed8" : "#15803d",
          fontWeight: 600,
          fontFamily: "'Consolas', 'Fira Code', monospace",
          letterSpacing:
            "normal" /* Ép khoảng cách các chữ cái về chuẩn mặc định */,
          wordSpacing:
            "-2px" /* Kéo các từ (words) xích lại gần nhau một chút */,
        }}
      >
        {isEdit
          ? `UPDATE · [${editStudent?.student_id}] ${editStudent?.full_name}`
          : "INSERT INTO dbo.students"}
      </div>

      <div
        className="overflow-y-auto"
        style={{
          padding: 12,
          display: "flex",
          flexDirection: "column",
          gap: 10,
        }}
      >
        {!isEdit && (
          <div>
            <label className="field-label">
              Student ID <span style={{ color: "#dc2626" }}>(*)</span>
            </label>
            <input
              className="inp"
              type="number"
              placeholder="2x52xxxx"
              value={form.student_id}
              onChange={(e) => set("student_id", e.target.value)}
            />
            {errors.student_id && (
              <p style={{ color: "#dc2626", fontSize: 10, marginTop: 3 }}>
                {errors.student_id}
              </p>
            )}
          </div>
        )}

        <div>
          <label className="field-label">
            Full Name <span style={{ color: "#dc2626" }}>(*)</span>
          </label>
          <input
            className="inp"
            type="text"
            placeholder="Example: Nguyễn Văn A"
            value={form.full_name}
            onChange={(e) => set("full_name", e.target.value)}
          />
          {errors.full_name && (
            <p style={{ color: "#dc2626", fontSize: 10, marginTop: 3 }}>
              {errors.full_name}
            </p>
          )}
        </div>

        <div>
          <label className="field-label">
            Gender <span style={{ color: "#dc2626" }}>(*)</span>
          </label>
          <select
            className="inp"
            value={form.gender}
            onChange={(e) => set("gender", e.target.value)}
          >
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
          </select>
        </div>

        <div>
          <label className="field-label">
            Major <span style={{ color: "#dc2626" }}>(*)</span>
          </label>
          <select
            className="inp"
            value={form.major}
            onChange={(e) => set("major", e.target.value)}
          >
            {MAJORS.map((m) => (
              <option key={m} value={m}>
                {m}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="field-label">
            GPA <span style={{ color: "#dc2626" }}>(*)</span>{" "}
            <span
              style={{ color: "#94a3b8", textTransform: "none", fontSize: 10 }}
            >
              (0.0 – 4.0)
            </span>
          </label>
          <input
            className="inp"
            type="number"
            step="0.01"
            min="0"
            max="4"
            placeholder="Example: 3.60"
            value={form.gpa}
            onChange={(e) => set("gpa", e.target.value)}
          />
          {errors.gpa && (
            <p style={{ color: "#dc2626", fontSize: 10, marginTop: 3 }}>
              {errors.gpa}
            </p>
          )}
        </div>

        <div>
          <label className="field-label">
            Email <span style={{ color: "#dc2626" }}>(*)</span>
          </label>
          <input
            className="inp"
            type="email"
            placeholder="2x52xxxx@gm.uit.edu.vn"
            value={form.email}
            onChange={(e) => set("email", e.target.value)}
          />
          {errors.email && (
            <p style={{ color: "#dc2626", fontSize: 10, marginTop: 3 }}>
              {errors.email}
            </p>
          )}
        </div>

        {/* Submit button nằm ngay sau Email — YC2 */}
        <div style={{ marginTop: 6, display: "flex", gap: 6 }}>
          <button
            type="submit"
            className="btn-primary"
            disabled={busy}
            style={{ flex: 1 }}
          >
            {busy ? "Processing..." : isEdit ? "Save Changes" : "Insert Record"}
          </button>
          {isEdit && (
            <button
              type="button"
              className="btn-secondary"
              onClick={onCancelEdit}
            >
              Cancel
            </button>
          )}
        </div>

        {successMsg && (
          <div
            style={{
              padding: "6px 8px",
              background: "#f0fdf4",
              border: "1px solid #86efac",
              borderRadius: 3,
              fontSize: 11,
              color: "#15803d",
              fontWeight: 600,
            }}
          >
            {successMsg}
          </div>
        )}
      </div>
    </form>
  );
}

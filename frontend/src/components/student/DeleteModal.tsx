/**
 * Modal xác nhận xóa một sinh viên
 * SOLID — Single Responsibility: chỉ lo confirm UI.
 */

import { useState } from "react";
import type { Student } from "@/domain/types";

interface DeleteModalProps {
  student: Student | null;
  onConfirm: () => Promise<void>;
  onCancel: () => void;
}

export function DeleteModal({
  student,
  onConfirm,
  onCancel,
}: DeleteModalProps) {
  const [busy, setBusy] = useState(false);
  if (!student) return null;

  const handleConfirm = async () => {
    setBusy(true);
    await onConfirm();
    setBusy(false);
  };

  return (
    /* Overlay - Tăng độ tối nhẹ để modal nổi bật hơn */
    <div
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(30, 41, 59, 0.4)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 100,
      }}
    >
      {/* Modal container - Giữ font Sans-serif cho toàn khối */}
      <div
        style={{
          background: "#ffffff" /* Trắng tinh */,
          border: "1px solid #e5e7eb" /* Viền xám mỏng */,
          borderRadius: 4,
          width: 460 /* Tăng width một chút để code SQL không bị ngộp */,
          boxShadow: "0 4px 20px rgba(0,0,0,0.08)",
          fontFamily: "'Segoe UI', Inter, Roboto, Helvetica, sans-serif",
          overflow: "hidden",
        }}
      >
        {/* ── Title bar ── */}
        <div
          style={{
            padding: "16px",
            borderBottom: "1px solid #e5e7eb",
            display: "flex",
            alignItems: "center",
            gap: 10,
            background: "#fafafa" /* Nền xám cực nhạt cho Header */,
          }}
        >
          {/* Warning indicator - Đỏ tinh tế */}
          <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="#dc2626" /* Màu đỏ red-600 Enterprise */
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            style={{ flexShrink: 0 }}
          >
            {/* Vẽ hình tam giác bo góc */}
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
            {/* Vẽ thân dấu chấm than */}
            <line x1="12" y1="9" x2="12" y2="13" />
            {/* Vẽ dấu chấm phía dưới */}
            <line x1="12" y1="17" x2="12.01" y2="17" />
          </svg>
          {/* ------------------------- */}

          <span style={{ fontSize: 15, fontWeight: 600, color: "#111827" }}>
            Confirm Record Deletion
          </span>
        </div>

        {/* ── Body ── */}
        <div style={{ padding: "20px 16px" }}>
          {/* Mô tả ngắn - Sans-serif */}
          <p
            style={{
              fontSize: 13,
              color: "#4b5563",
              marginBottom: 16,
              lineHeight: 1.5,
            }}
          >
            The following record will be permanently removed from{" "}
            <span
              style={{
                fontFamily: "'Consolas', 'Fira Code', monospace",
                fontSize: 12,
                color: "#2563eb" /* Corporate Blue cho Table name */,
                fontWeight: 600,
                background: "#eff6ff" /* Nền xanh nhạt */,
                padding: "2px 6px",
                borderRadius: 4,
              }}
            >
              dbo.students
            </span>
            :
          </p>

          {/* Record info - FIX BUG 1: DÙNG TABLE ĐỂ GIÓNG THẲNG HÀNG TUYỆT ĐỐI */}
          <div
            style={{
              border: "1px solid #e5e7eb",
              borderRadius: 4,
              overflow: "hidden",
              marginBottom: 16,
            }}
          >
            <table
              style={{
                width: "100%",
                borderCollapse: "collapse",
                textAlign: "left",
              }}
            >
              <thead
                style={{
                  background: "#f9fafb" /* Nền xám table header */,
                  borderBottom: "1px solid #e5e7eb",
                }}
              >
                <tr>
                  {["student_id", "full_name", "major"].map((h, i) => (
                    <th
                      key={h}
                      style={{
                        padding: "8px 12px",
                        fontSize: 11,
                        fontWeight: 600,
                        color: "#6b7280",
                        textTransform: "uppercase",
                        letterSpacing: "0.05em",
                        width: i === 0 ? "80px" : "auto" /* Cố định cột ID */,
                      }}
                    >
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td
                    style={{
                      padding: "10px 12px",
                      fontFamily: "'Consolas', 'Fira Code', monospace",
                      fontSize: 13,
                      fontWeight: 700,
                      color: "#1d4ed8" /* Xanh đậm cho ID */,
                      borderRight: "1px solid #f3f4f6" /* Vạch ngăn cách cột */,
                    }}
                  >
                    {student.student_id}
                  </td>
                  <td
                    style={{
                      padding: "10px 12px",
                      fontSize: 13,
                      fontWeight: 600,
                      color: "#111827",
                      borderRight: "1px solid #f3f4f6",
                    }}
                  >
                    {student.full_name}
                  </td>
                  <td
                    style={{
                      padding: "10px 12px",
                      fontSize: 13,
                      color: "#6b7280",
                    }}
                  >
                    {student.major}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          {/* SQL statement - FIX BUG 3 & CHÓI LÒA: CHUYỂN SANG NỀN TRẮNG HÀI HÒA */}
          <div
            style={{
              background: "#f9fafb" /* Nền xám nhạt tinh tế */,
              border: "1px solid #e5e7eb" /* Viền xám mảnh */,
              borderRadius: 6,
              padding: "16px 20px" /* Tăng padding để dễ thở */,
              marginBottom: 16,
              fontFamily: "'Consolas', 'Fira Code', monospace",
              fontSize: 13,
              lineHeight: 1.6,
              overflowX: "auto",
            }}
          >
            <span style={{ color: "#0369a1" /* Blue 700 cho Keywords */ }}>
              DELETE FROM{" "}
            </span>
            <span style={{ color: "#1e293b" /* Slate 900 cho Table */ }}>
              dbo.students
            </span>
            <br />
            <span style={{ color: "#0369a1" }}>WHERE </span>
            <span style={{ color: "#1e293b" }}>student_id</span>
            <span style={{ color: "#9ca3af" /* Gray 400 cho Toán tử */ }}>
              {" "}
              ={" "}
            </span>
            <span
              style={{
                color: "#dc2626" /* Muted Enterprise Red cho literal */,
              }}
            >
              {student.student_id}
            </span>
            <span style={{ color: "#9ca3af" }}>;</span>
          </div>

          {/* Warning - Tone vàng mù tạt trên nền sáng */}
          <div
            style={{
              background: "#fffcf0" /* Nền kem cực nhạt tiệp với form trắng */,
              border:
                "1px solid #d4b830" /* Viền vàng mù tạt chuẩn từ ảnh của bạn */,
              borderRadius: 6,
              padding: "12px 16px",
              fontSize: 13,
              color:
                "#997300" /* Hạ tone chữ xuống một xíu xiu để dễ đọc trên nền sáng */,
              lineHeight: 1.5,
              display: "flex",
              alignItems: "flex-start",
              gap: 8,
            }}
          >
            {/* Icon tam giác vàng mù tạt */}
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="#d4b830" /* Đồng bộ màu viền */
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              style={{ flexShrink: 0, marginTop: 2 }}
            >
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
              <line x1="12" y1="9" x2="12" y2="13" />
              <line x1="12" y1="17" x2="12.01" y2="17" />
            </svg>
            <span>
              WARNING: The B-Tree index will be rebuilt. This action cannot be
              undone.
            </span>
          </div>
        </div>
        {/* ── Footer — Buttons ── */}
        <div
          style={{
            padding: "12px 16px",
            borderTop: "1px solid #e5e7eb",
            display: "flex",
            justifyContent: "flex-end",
            gap: 12,
            background: "#fafafa" /* Nền xám nhạt cho Footer */,
          }}
        >
          {/* Cancel - Trắng viền xám */}
          <button
            style={{
              padding: "6px 16px",
              fontSize: 13,
              fontWeight: 500,
              color: "#374151",
              background: "#ffffff",
              border: "1px solid #d1d5db",
              borderRadius: 4,
              cursor: busy ? "not-allowed" : "pointer",
              fontFamily: "inherit",
            }}
            onClick={onCancel}
            disabled={busy}
          >
            Cancel
          </button>

          {/* Confirm - Đỏ đô doanh nghiệp, phẳng */}
          <button
            style={{
              padding: "6px 16px",
              fontSize: 13,
              fontWeight: 600,
              color: "#ffffff",
              background: "#dc2626" /* Muted Enterprise Red */,
              border: "1px solid #b91c1c",
              borderRadius: 4,
              cursor: busy ? "not-allowed" : "pointer",
              fontFamily: "inherit",
            }}
            onClick={handleConfirm}
            disabled={busy}
          >
            {busy ? "Deleting..." : "Confirm Delete"}
          </button>
        </div>
      </div>
    </div>
  );
}

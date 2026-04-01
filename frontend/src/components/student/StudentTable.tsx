/**
 * Bảng dữ liệu sinh viên — SQL Table style.
 * SOLID — Single Responsibility: chỉ lo render + row interaction.
 */

import { useState, useMemo } from "react";
import type { Student } from "@/domain/types";
import { GenderBadge, GpaBadge } from "@/components/ui/Badge";

interface StudentTableProps {
  students: Student[];
  selectedId: number | null;
  searchQuery: string;
  searchMode: "name" | "id" | "none";
  onSelect: (s: Student) => void;
  onEdit: (s: Student) => void;
  onDelete: (s: Student) => void;
}

type SortMode = "insertion" | "sorted";

export function StudentTable({
  students,
  selectedId,
  searchQuery,
  searchMode,
  onSelect,
  onEdit,
  onDelete,
}: StudentTableProps) {
  const [sortMode, setSortMode] = useState<SortMode>("insertion");
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);

  const displayedStudents = useMemo(() => {
    if (sortMode === "sorted") {
      return [...students].sort((a, b) => a.student_id - b.student_id);
    }
    return students;
  }, [students, sortMode]);

  return (
    <div className="flex flex-col h-full" style={{ background: "#ffffff" }}>
      {/* SQL Header Bar */}
      <div
        className="panel-header"
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        <span
          style={{
            fontFamily: "'Consolas', 'Fira Code', monospace",
            fontWeight: 400,
            textTransform: "none",
            letterSpacing: 0,
            fontSize: 11,
            color: "#334155",
          }}
        >
          <span style={{ color: "#6366f1", fontWeight: 700 }}>SELECT</span>
          {" * "}
          <span style={{ color: "#6366f1", fontWeight: 700 }}>FROM</span>
          {" dbo.students"}
          {searchQuery && searchMode === "id" && (
            <span>
              {" "}
              <span style={{ color: "#6366f1", fontWeight: 700 }}>WHERE</span>
              <span style={{ color: "#2563eb" }}>
                {" "}
                student_id = {searchQuery}
              </span>
            </span>
          )}
          {searchQuery && searchMode === "name" && (
            <span>
              {" "}
              <span style={{ color: "#6366f1", fontWeight: 700 }}>WHERE</span>
              <span style={{ color: "#2563eb" }}>
                {" "}
                full_name LIKE '%{searchQuery}%'
              </span>
            </span>
          )}
          {sortMode === "sorted" && (
            <span style={{ color: "#7c3aed" }}> ORDER BY student_id ASC</span>
          )}
        </span>

        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <div
            style={{
              display: "flex",
              border: "1px solid #e2e8f0",
              borderRadius: 3,
              overflow: "hidden",
            }}
          >
            <button
              onClick={() => setSortMode("insertion")}
              style={{
                padding: "2px 8px",
                fontSize: 10,
                fontWeight: 700,
                background: sortMode === "insertion" ? "#2563eb" : "#ffffff",
                color: sortMode === "insertion" ? "#ffffff" : "#64748b",
                border: "none",
                cursor: "pointer",
                fontFamily: "'Segoe UI', sans-serif",
                textTransform: "uppercase",
                letterSpacing: "0.05em",
              }}
            >
              Insertion Order
            </button>
            <button
              onClick={() => setSortMode("sorted")}
              style={{
                padding: "2px 8px",
                fontSize: 10,
                fontWeight: 700,
                background: sortMode === "sorted" ? "#2563eb" : "#ffffff",
                color: sortMode === "sorted" ? "#ffffff" : "#64748b",
                border: "none",
                borderLeft: "1px solid #e2e8f0",
                cursor: "pointer",
                fontFamily: "'Segoe UI', sans-serif",
                textTransform: "uppercase",
                letterSpacing: "0.05em",
              }}
            >
              Sort by ID
            </button>
          </div>
          <span style={{ color: "#94a3b8", fontSize: 11 }}>
            {students.length} row(s)
          </span>
        </div>
      </div>

      {/* Table area — position relative để đặt empty state tuyệt đối */}
      <div
        className="flex-1 overflow-auto"
        style={{ background: "#ffffff", position: "relative" }}
      >
        {/* Empty state — căn giữa tuyệt đối, không ảnh hưởng table */}
        {displayedStudents.length === 0 && (
          <div
            style={{
              position: "absolute",
              top: "50%",
              left: "50%",
              transform: "translate(-50%, -50%)",
              fontFamily: "'Consolas', monospace",
              fontSize: 12,
              color: "#94a3b8",
              pointerEvents: "none",
              whiteSpace: "nowrap",
            }}
          >
            (0 rows affected)
          </div>
        )}

        <table
          style={{ width: "100%", borderCollapse: "collapse", fontSize: 12 }}
        >
          <thead>
            <tr
              style={{
                background: "#f1f5f9",
                position: "sticky",
                top: 0,
                zIndex: 5,
              }}
            >
              {[
                "STT",
                "student_id",
                "full_name",
                "gender",
                "major",
                "gpa",
                "email",
                "actions",
              ].map((h) => (
                <th
                  key={h}
                  style={{
                    textAlign: "left",
                    padding: "6px 10px",
                    fontWeight: 700,
                    fontSize: 10,
                    letterSpacing: "0.07em",
                    textTransform: "uppercase",
                    color: "#64748b",
                    borderBottom: "2px solid #e2e8f0",
                    borderRight: "1px solid #e2e8f0",
                    whiteSpace: "nowrap",
                    fontFamily: "'Segoe UI', sans-serif",
                  }}
                >
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody style={{ background: "#ffffff" }}>
            {displayedStudents.map((s, i) => {
              const isSelected = selectedId === s.student_id;
              const isHovered = hoveredIndex === i;
              const isEven = i % 2 === 1;

              const rowBg = isSelected
                ? "#bfdbfe"
                : isHovered
                  ? "#93c5fd40"
                  : isEven
                    ? "#f9fafb"
                    : "#ffffff";

              return (
                <tr
                  key={s.student_id}
                  onClick={() => onSelect(s)}
                  onMouseEnter={() => setHoveredIndex(i)}
                  onMouseLeave={() => setHoveredIndex(null)}
                  style={{
                    background: rowBg,
                    cursor: "pointer",
                    transition: "background 0.12s",
                    borderBottom: "1px solid #e5e7eb",
                  }}
                >
                  <td style={td}>{i + 1}</td>
                  <td
                    style={{
                      ...td,
                      fontFamily: "'Consolas','Fira Code',monospace",
                      fontWeight: 700,
                      color: "#1d4ed8",
                    }}
                  >
                    {s.student_id}
                  </td>
                  <td style={{ ...td, fontWeight: 500, color: "#1e293b" }}>
                    {s.full_name}
                  </td>
                  <td style={td}>
                    <GenderBadge value={s.gender} />
                  </td>
                  <td style={{ ...td, color: "#475569" }}>{s.major}</td>
                  <td style={td}>
                    <GpaBadge value={s.gpa} />
                  </td>
                  <td
                    style={{
                      ...td,
                      color: "#64748b",
                    }}
                  >
                    {s.email}
                  </td>
                  <td style={{ ...td, whiteSpace: "nowrap" }}>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onEdit(s);
                      }}
                      style={actionBtn("#2563eb")}
                    >
                      Edit
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onDelete(s);
                      }}
                      style={{ ...actionBtn("#dc2626"), marginLeft: 4 }}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const td: React.CSSProperties = {
  padding: "5px 10px",
  borderRight: "1px solid #f1f5f9",
  fontSize: 12,
  color: "#374151",
  fontFamily: "'Segoe UI', sans-serif",
};

const actionBtn = (color: string): React.CSSProperties => ({
  padding: "2px 8px",
  fontSize: 10,
  fontWeight: 700,
  border: `1px solid ${color}33`,
  background: `${color}11`,
  color,
  borderRadius: 2,
  cursor: "pointer",
  letterSpacing: "0.04em",
  textTransform: "uppercase",
  fontFamily: "'Segoe UI', sans-serif",
});

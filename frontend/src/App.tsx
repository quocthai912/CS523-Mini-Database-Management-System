/**
 * Root App — Enterprise DBMS layout.
 */

import { useEffect, useState, useCallback } from "react";
import { useStudentStore } from "@/store/studentStore";
import { StudentForm } from "@/components/student/StudentForm";
import { StudentTable } from "@/components/student/StudentTable";
import { DeleteModal } from "@/components/student/DeleteModal";
import { BTreeCanvas } from "@/components/btree/BTreeCanvas";
import type { Student } from "@/domain/types";
import type { CreateStudentDto, UpdateStudentDto } from "@/services/studentApi";

/* #12 — Search mode type */
type SearchType = "name" | "id";

export default function App() {
  const {
    students,
    treeSnapshot,
    isLoading,
    error,
    searchQuery,
    searchMode,
    fetchStudents,
    fetchTree,
    createStudent,
    updateStudent,
    deleteStudent,
    searchStudents,
    searchStudentById,
    clearSearch,
    clearError,
  } = useStudentStore();

  const [editTarget, setEditTarget] = useState<Student | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<Student | null>(null);
  const [selectedId, setSelectedId] = useState<number | null>(null);

  /* #12 — Search state */
  const [searchInput, setSearchInput] = useState("");
  const [searchType, setSearchType] = useState<SearchType>("name");
  const [highlightKeys, setHighlightKeys] = useState<number[]>([]);

  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const checkConnection = async () => {
      try {
        await fetch("http://localhost:8000/health");
        setIsConnected(true);
      } catch {
        setIsConnected(false);
      }
    };

    checkConnection();
    fetchStudents();
    fetchTree();

    const interval = setInterval(checkConnection, 5000);
    return () => clearInterval(interval);
  }, [fetchStudents, fetchTree]);

  const handleSubmit = useCallback(
    async (dto: CreateStudentDto | UpdateStudentDto) => {
      if (editTarget) {
        await updateStudent(editTarget.student_id, dto as UpdateStudentDto);
        setEditTarget(null);
      } else {
        const d = dto as CreateStudentDto;
        await createStudent(d);
        setHighlightKeys([d.student_id]);
        setTimeout(() => setHighlightKeys([]), 2500);
      }
    },
    [editTarget, createStudent, updateStudent],
  );

  const handleEdit = (s: Student) => {
    setEditTarget(s);
    setSelectedId(s.student_id);
  };

  const handleConfirmDelete = async () => {
    if (!deleteTarget) return;
    await deleteStudent(deleteTarget.student_id);
    if (editTarget?.student_id === deleteTarget.student_id) setEditTarget(null);
    setDeleteTarget(null);
    setSelectedId(null);
  };

  /* #12 — Search handler hỗ trợ cả name và ID */
  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    const val = searchInput.trim();
    if (!val) {
      await clearSearch();
      return;
    }

    if (searchType === "id") {
      const id = parseInt(val, 10);
      if (isNaN(id)) return;
      await searchStudentById(id);
      setHighlightKeys([id]);
      setTimeout(() => setHighlightKeys([]), 2500);
    } else {
      const results = await searchStudents(val);
      if (results.length > 0) {
        const ids = results.map((s) => s.student_id);
        setHighlightKeys(ids);
        setTimeout(() => setHighlightKeys([]), 2500);
      }
    }
  };

  const handleClearSearch = async () => {
    setSearchInput("");
    setHighlightKeys([]);
    await clearSearch();
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100vh",
        overflow: "hidden",
      }}
    >
      {/* ── TITLE BAR — Fix #3, #5: sáng, border-bottom ── */}
      <div
        style={{
          background: "#ffffff" /* #5: sáng */,
          borderBottom: "2px solid #2563eb" /* #5: accent border */,
          padding: "0 16px",
          height: 44,
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          flexShrink: 0,
        }}
      >
        {/* #3: chỉ giữ tên hệ thống — ĐÃ CHÈN ICON DATABASE */}
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          {/* DATABASE ICON - Vẽ bằng SVG thuần */}
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="#111827"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            style={{ flexShrink: 0 }}
          >
            <ellipse cx="12" cy="5" rx="9" ry="3" />
            <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3" />
            <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5" />
          </svg>

          {/* TEXT TÊN HỆ THỐNG */}
          <span
            style={{
              fontFamily: "'Segoe UI', Inter, Roboto, Helvetica, sans-serif",
              fontSize: 15,
              fontWeight: 700,
              color: "#111827",
              letterSpacing: "0.03em",
              textTransform: "uppercase",
            }}
          >
            MINI DATABASE MANAGEMENT SYSTEM
          </span>
        </div>

        {/* #2: bỏ localhost. Chỉ hiện status */}
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <span
            style={{
              width: 7,
              height: 7,
              borderRadius: "50%",
              background: isLoading
                ? "#f59e0b"
                : isConnected
                  ? "#22c55e"
                  : "#ef4444",
              display: "inline-block",
              transition: "background 0.3s",
            }}
          />
          <span
            className="mono"
            style={{
              fontSize: 11,
              color: isConnected ? "#64748b" : "#ef4444",
              fontWeight: isConnected ? 400 : 600,
            }}
          >
            {isLoading
              ? "Executing..."
              : isConnected
                ? "Connected"
                : "Not Connected"}
          </span>
        </div>
      </div>

      {/* ── BODY ── */}
      <div style={{ display: "flex", flex: 1, overflow: "hidden" }}>
        {/* LEFT PANEL — Form */}
        <div
          style={{
            width: 240,
            flexShrink: 0,
            background: "#f8fafc",
            borderRight: "1px solid #e2e8f0",
            display: "flex",
            flexDirection: "column",
            overflow: "hidden",
          }}
        >
          <StudentForm
            editStudent={editTarget}
            onSubmit={handleSubmit}
            onCancelEdit={() => setEditTarget(null)}
          />
        </div>

        {/* RIGHT SIDE */}
        <div
          style={{
            flex: 1,
            display: "flex",
            flexDirection: "column",
            overflow: "hidden",
          }}
        >
          {/* TOOLBAR */}
          <div
            style={{
              background: "#f8fafc",
              borderBottom: "1px solid #e2e8f0",
              padding: "6px 12px",
              display: "flex",
              alignItems: "center",
              gap: 6,
              flexShrink: 0,
            }}
          >
            <button
              className="btn-secondary"
              onClick={() => {
                fetchStudents();
                fetchTree();
              }}
            >
              Refresh
            </button>

            <div
              style={{
                width: 1,
                height: 20,
                background: "#e2e8f0",
                margin: "0 4px",
              }}
            />

            {/* #12 — Search type toggle + input */}
            <form
              onSubmit={handleSearch}
              style={{ display: "flex", gap: 4, alignItems: "center" }}
            >
              {/* Toggle Name / ID */}
              <div
                style={{
                  display: "flex",
                  border: "1px solid #e2e8f0",
                  borderRadius: 3,
                  overflow: "hidden",
                }}
              >
                <button
                  type="button"
                  onClick={() => setSearchType("name")}
                  style={{
                    padding: "4px 8px",
                    fontSize: 10,
                    fontWeight: 700,
                    background: searchType === "name" ? "#2563eb" : "#ffffff",
                    color: searchType === "name" ? "#ffffff" : "#64748b",
                    border: "none",
                    cursor: "pointer",
                    fontFamily: "inherit",
                    textTransform: "uppercase",
                    letterSpacing: "0.05em",
                  }}
                >
                  By Name
                </button>
                <button
                  type="button"
                  onClick={() => setSearchType("id")}
                  style={{
                    padding: "4px 8px",
                    fontSize: 10,
                    fontWeight: 700,
                    background: searchType === "id" ? "#2563eb" : "#ffffff",
                    color: searchType === "id" ? "#ffffff" : "#64748b",
                    border: "none",
                    borderLeft: "1px solid #e2e8f0",
                    cursor: "pointer",
                    fontFamily: "inherit",
                    textTransform: "uppercase",
                    letterSpacing: "0.05em",
                  }}
                >
                  By ID
                </button>
              </div>

              <input
                className="inp"
                type={searchType === "id" ? "number" : "text"}
                value={searchInput}
                onChange={(e) => setSearchInput(e.target.value)}
                placeholder={
                  searchType === "id"
                    ? "Enter Student ID..."
                    : "Search by name..."
                }
                style={{ width: 200 }}
              />
              <button type="submit" className="btn-secondary">
                Search
              </button>
              {searchQuery && (
                <button
                  type="button"
                  className="btn-secondary"
                  onClick={handleClearSearch}
                >
                  Clear Filter
                </button>
              )}
            </form>

            {/* Error inline + #4 node info */}
            <div
              style={{
                marginLeft: "auto",
                display: "flex",
                gap: 16,
                alignItems: "center",
              }}
            >
              {error && (
                <span style={{ fontSize: 11, color: "#dc2626" }}>
                  [ERROR] {error}
                  <button
                    onClick={clearError}
                    style={{
                      marginLeft: 6,
                      color: "#94a3b8",
                      background: "none",
                      border: "none",
                      cursor: "pointer",
                      fontSize: 12,
                    }}
                  >
                    ×
                  </button>
                </span>
              )}
              {/* #4 */}
              <span className="mono" style={{ fontSize: 11, color: "#94a3b8" }}>
                Nodes: {treeSnapshot?.size ?? 0} | Order: 3
              </span>
            </div>
          </div>

          {/* B-TREE CANVAS */}
          <div
            style={{
              flex: 1,
              overflow: "hidden",
              borderBottom: "2px solid #e2e8f0",
              position: "relative",
            }}
          >
            <div
              style={{
                position: "absolute",
                top: 8,
                left: 12,
                zIndex: 10,
                background: "rgba(248,250,252,0.9)",
                border: "1px solid #e2e8f0",
                borderRadius: 3,
                padding: "2px 10px",
              }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
                {/* Tree/Hierarchy icon */}
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
                  {/* Root node — căn giữa trên cùng */}
                  <rect x="8" y="1" width="8" height="5" rx="1" />

                  {/* Đường thẳng từ root xuống */}
                  <line x1="12" y1="6" x2="12" y2="10" />

                  {/* Đường ngang nối 2 nhánh */}
                  <line x1="5" y1="10" x2="19" y2="10" />

                  {/* Đường thẳng xuống node trái */}
                  <line x1="5" y1="10" x2="5" y2="13" />

                  {/* Đường thẳng xuống node phải */}
                  <line x1="19" y1="10" x2="19" y2="13" />

                  {/* Node trái */}
                  <rect x="1" y="13" width="8" height="5" rx="1" />

                  {/* Node phải */}
                  <rect x="15" y="13" width="8" height="5" rx="1" />
                </svg>
                <span
                  className="mono"
                  style={{
                    fontSize: 10,
                    color: "#64748b",
                    fontWeight: 700,
                    letterSpacing: "0.1em",
                  }}
                >
                  INDEX TREE VIEW
                </span>
              </div>
            </div>
            <BTreeCanvas
              snapshot={treeSnapshot}
              highlightKeys={highlightKeys}
            />
          </div>

          {/* DATA TABLE */}
          <div
            style={{
              height: "35vh",
              flexShrink: 0,
              overflow: "hidden",
              display: "flex",
              flexDirection: "column",
            }}
          >
            <StudentTable
              students={students}
              selectedId={selectedId}
              searchQuery={searchQuery}
              searchMode={searchMode}
              onSelect={(s) => setSelectedId(s.student_id)}
              onEdit={handleEdit}
              onDelete={(s) => setDeleteTarget(s)}
            />
          </div>
        </div>
      </div>

      <DeleteModal
        student={deleteTarget}
        onConfirm={handleConfirmDelete}
        onCancel={() => setDeleteTarget(null)}
      />
    </div>
  );
}

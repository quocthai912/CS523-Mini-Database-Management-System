/**
 * Vẽ cây B-Tree bằng SVG thuần.
 * Node: hình chữ nhật, viền xám, text mono.
 * Edge: nét liền mỏng màu xám.
 * Highlight: viền xanh + nền xanh nhạt khi key vừa được thao tác.
 *
 * SOLID — Single Responsibility: chỉ lo render SVG tree.
 */
import React, { useMemo } from "react";
import type { BTreeNode, BTreeSnapshot } from "@/domain/types";

interface BTreeCanvasProps {
  snapshot: BTreeSnapshot | null;
  highlightKeys?: number[];
}

interface LayoutNode {
  node: BTreeNode;
  x: number;
  y: number;
  width: number;
  isRoot: boolean;
}

const NODE_H = 44;
const KEY_W = 72;
const V_GAP = 80;
const H_GAP = 28;

function buildLayout(
  node: BTreeNode | null,
  depth: number,
  offsetX: number,
  isRoot: boolean = false,
): { items: LayoutNode[]; totalWidth: number } {
  if (!node) return { items: [], totalWidth: 0 };

  const nodeW = node.keys.length * KEY_W;

  if (node.children.length === 0) {
    return {
      items: [
        { node, x: offsetX, y: depth * (NODE_H + V_GAP), width: nodeW, isRoot },
      ],
      totalWidth: nodeW,
    };
  }

  const childResults: ReturnType<typeof buildLayout>[] = [];
  for (const child of node.children) {
    childResults.push(buildLayout(child, depth + 1, 0, false));
  }

  const totalChildW =
    childResults.reduce((s, c) => s + c.totalWidth, 0) +
    H_GAP * (childResults.length - 1);

  const allItems: LayoutNode[] = [];
  let curX = offsetX;
  for (const cr of childResults) {
    cr.items.forEach((item) => allItems.push({ ...item, x: item.x + curX }));
    curX += cr.totalWidth + H_GAP;
  }

  const rootX = offsetX + totalChildW / 2 - nodeW / 2;

  return {
    items: [
      { node, x: rootX, y: depth * (NODE_H + V_GAP), width: nodeW, isRoot },
      ...allItems,
    ],
    totalWidth: Math.max(totalChildW, nodeW),
  };
}

export function BTreeCanvas({
  snapshot,
  highlightKeys = [],
}: BTreeCanvasProps) {
  const layout = useMemo(() => {
    if (!snapshot?.root) return null;
    return buildLayout(snapshot.root, 0, 48, true);
  }, [snapshot]);

  if (!snapshot?.root || !layout) {
    return (
      <div
        className="btree-canvas-bg"
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          flexDirection: "column",
          gap: 8,
        }}
      >
        <p
          style={{
            fontFamily: "'Consolas', 'Fira Code', monospace",
            color: "#94a3b8",
            fontSize: 13,
          }}
        >
          B-TREE INDEX IS EMPTY
        </p>
        <p style={{ color: "#cbd5e1", fontSize: 11 }}>
          Add a student record to visualize the index tree
        </p>
      </div>
    );
  }

  const items = layout.items;
  const svgW = Math.max(...items.map((n) => n.x + n.width)) + 60;
  const svgH = Math.max(...items.map((n) => n.y)) + NODE_H + 56;

  const edges: React.ReactElement[] = [];
  for (const parent of items) {
    if (parent.node.children.length === 0) continue;

    parent.node.children.forEach((child, ci) => {
      const childLayout = items.find((it) => it.node === child);
      if (!childLayout) return;

      const numCh = parent.node.children.length;

      const centerParentX = parent.x + parent.width / 2;
      const spacing = 16;
      const offset = (ci - (numCh - 1) / 2) * spacing;
      const x1 = centerParentX + offset;
      const y1 = parent.y + NODE_H;

      const x2 = childLayout.x + childLayout.width / 2;
      const y2 = childLayout.y;

      edges.push(
        <line
          key={`edge-${parent.node.keys.join("-")}-${ci}`}
          x1={x1}
          y1={y1}
          x2={x2}
          y2={y2}
          stroke="#94a3b8"
          strokeWidth="1.5"
        />,
      );
    });
  }

  const nodes: React.ReactElement[] = items.map((item, idx) => {
    const { node, x, y, width, isRoot } = item;
    const isHl = node.keys.some((k) => highlightKeys.includes(k));
    const isLeaf = node.children.length === 0;

    // Xanh dương cho Highlight, Cam cho Root, Xanh lá cho các Node còn lại
    const strokeColor = isHl ? "#2563eb" : isRoot ? "#d97706" : "#16a34a"; // green-600
    const strokeWidth = isRoot && !isHl ? 2 : isHl ? 2 : 1.5; // Tăng viền xanh lá lên 1.5
    const fillColor = isHl ? "#eff6ff" : isRoot ? "#fffbeb" : "#f0fdf4"; // green-50
    const textColor = isHl ? "#1d4ed8" : isRoot ? "#92400e" : "#14532d"; // green-900
    const divColor = isHl ? "#93c5fd" : isRoot ? "#fde68a" : "#bbf7d0"; // green-200

    const shadowFilter = `drop-shadow(0px 2px 4px rgba(0,0,0,0.10))`;

    return (
      <g key={idx} style={{ filter: shadowFilter }}>
        <rect
          x={x}
          y={y}
          width={width}
          height={NODE_H}
          rx={3}
          fill={fillColor}
          stroke={strokeColor}
          strokeWidth={strokeWidth}
        />

        {node.keys.map((_, ki) =>
          ki < node.keys.length - 1 ? (
            <line
              key={`d-${ki}`}
              x1={x + (ki + 1) * KEY_W}
              y1={y + 6}
              x2={x + (ki + 1) * KEY_W}
              y2={y + NODE_H - 6}
              stroke={divColor}
              strokeWidth="1"
            />
          ) : null,
        )}

        {node.keys.map((key, ki) => (
          <text
            key={`k-${ki}`}
            x={x + ki * KEY_W + KEY_W / 2}
            y={y + NODE_H / 2 + 5}
            textAnchor="middle"
            fontFamily="'Consolas', 'Fira Code', monospace"
            fontSize="13"
            fontWeight="600"
            fill={textColor}
          >
            {key}
          </text>
        ))}

        {isLeaf && (
          <rect
            x={x + 1}
            y={y + NODE_H - 3}
            width={width - 2}
            height={3}
            rx={0}
            fill={isHl ? "#3b82f6" : "#e2e8f0"}
          />
        )}
      </g>
    );
  });

  return (
    <div
      className="btree-canvas-bg"
      style={{
        width: "100%",
        height: "100%",
        overflow: "auto",
        paddingBottom: "120px",
      }}
    >
      <svg
        width={svgW}
        height={svgH}
        viewBox={`0 0 ${svgW} ${svgH}`}
        style={{ display: "block", minWidth: "100%" }}
      >
        <defs>
          <filter id="node-shadow" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow
              dx="0"
              dy="2"
              stdDeviation="3"
              floodColor="#00000018"
            />
          </filter>
        </defs>
        {nodes}
        {edges}
      </svg>
    </div>
  );
}

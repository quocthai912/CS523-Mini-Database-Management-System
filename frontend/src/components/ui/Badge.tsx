/**
 * Badge components cho GPA và Gender.
 */

export function GenderBadge({ value }: { value: string }) {
  const map: Record<string, string> = {
    male: "Male",
    female: "Female",
    other: "Other",
  };
  return (
    <span
      style={{
        fontSize: 12,
        color: "#475569",
        fontFamily: "'Segoe UI', sans-serif",
      }}
    >
      {map[value] ?? value}
    </span>
  );
}

export function GpaBadge({ value }: { value: number }) {
  const color = value >= 3.5 ? "#15803d" : value >= 2.5 ? "#b45309" : "#dc2626";
  return (
    <span
      style={{
        fontFamily: "'Consolas', 'Fira Code', monospace",
        fontSize: 12,
        fontWeight: 600,
        color,
      }}
    >
      {value.toFixed(2)}
    </span>
  );
}

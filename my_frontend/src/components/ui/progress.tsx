// src/components/ui/progress.tsx
import React from "react";

interface ProgressProps extends React.HTMLAttributes<HTMLDivElement> {
  value?: number; // 0..100
}

export function Progress({
  value = 0,
  className = "",
  ...props
}: ProgressProps) {
  return (
    <div
      className={`relative w-full h-2 bg-gray-200 rounded ${className}`}
      {...props}
    >
      <div
        className="absolute left-0 top-0 h-full bg-green-500 transition-all"
        style={{ width: `${value}%` }}
      ></div>
    </div>
  );
}

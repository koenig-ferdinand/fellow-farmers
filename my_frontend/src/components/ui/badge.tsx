// src/components/ui/badge.tsx
import React from "react";

interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "outline" | "solid";
}

export function Badge({
  children,
  variant = "outline",
  className = "",
  ...props
}: BadgeProps) {
  const base = "inline-block px-2 py-1 text-xs font-medium rounded";
  let variantStyles = "";

  if (variant === "outline") {
    variantStyles = "border border-gray-300 bg-transparent";
  } else {
    variantStyles = "bg-gray-200";
  }

  return (
    <div className={`${base} ${variantStyles} ${className}`} {...props}>
      {children}
    </div>
  );
}

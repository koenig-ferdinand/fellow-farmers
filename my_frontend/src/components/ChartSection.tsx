// src/components/ChartSection.tsx
import React from "react";

interface ChartSectionProps {
  title?: string;
  // ...other props
}

const ChartSection: React.FC<ChartSectionProps> = ({ title }) => {
  return (
    <div className="bg-white p-4 rounded shadow">
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-sm text-gray-600">Chart goes here...</p>
    </div>
  );
};

export default ChartSection;

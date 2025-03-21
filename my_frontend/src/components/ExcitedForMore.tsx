// src/components/ExcitedForMore.tsx
import React from "react";

const ExcitedForMore: React.FC = () => {
  const handleBubbleClick = (destination: string) => {
    console.log(`Navigating to ${destination}`);
  };

  return (
    <div className="fixed inset-0 z-0 flex items-end justify-center pointer-events-none">
      <div className="mb-10 flex gap-6">
        <div
          className="bg-white p-4 rounded-full shadow-lg cursor-pointer pointer-events-auto"
          onClick={() => handleBubbleClick("Fellow Farmers")}
        >
          <span className="text-2xl font-bold text-gray-800">
            Fellow Farmers
          </span>
        </div>
        <div
          className="bg-white p-4 rounded-full shadow-lg cursor-pointer pointer-events-auto"
          onClick={() => handleBubbleClick("Experts")}
        >
          <span className="text-2xl font-bold text-gray-800">Experts</span>
        </div>
        <div
          className="bg-white p-4 rounded-full shadow-lg cursor-pointer pointer-events-auto"
          onClick={() => handleBubbleClick("New Ideas")}
        >
          <span className="text-2xl font-bold text-gray-800">New Ideas</span>
        </div>
      </div>
    </div>
  );
};

export default ExcitedForMore;

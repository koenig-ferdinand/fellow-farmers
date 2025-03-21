// src/components/Header.tsx
import React from "react";

const Header: React.FC = () => {
  return (
    <header className="w-full bg-white py-4 shadow z-10 relative">
      <div className="max-w-5xl mx-auto px-4 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-air-blue-core">
          My Cool Farm App
        </h1>
      </div>
    </header>
  );
};

export default Header;

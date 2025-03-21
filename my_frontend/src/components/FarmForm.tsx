// src/components/FarmForm.tsx
import React, { useState } from "react";
import { FarmFormData, CropType } from "@/types";

interface FarmFormProps {
  onSubmit: (data: FarmFormData) => Promise<void>;
  isLoading: boolean;
}

const FarmForm: React.FC<FarmFormProps> = ({ onSubmit, isLoading }) => {
  const [location, setLocation] = useState("");
  const [cropType, setCropType] = useState<CropType>("rice"); // default
  const [fieldSize, setFieldSize] = useState(5);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({ location, cropType, fieldSize });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Location Input */}
      <div>
        <label
          htmlFor="location"
          className="block text-lg font-medium text-gray-700 mb-1"
        >
          Location
        </label>
        <input
          id="location"
          type="text"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          required
          placeholder="Enter your location"
          className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-air-blue-core"
        />
      </div>

      {/* Crop Type */}
      <div>
        <label
          htmlFor="cropType"
          className="block text-lg font-medium text-gray-700 mb-1"
        >
          Crop Type
        </label>
        <select
          id="cropType"
          value={cropType}
          onChange={(e) => setCropType(e.target.value as CropType)}
          className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-air-blue-core"
        >
          <option value="rice">Rice</option>
          <option value="cotton">Cotton</option>
          <option value="maize">Maize</option>
          <option value="wheat">Wheat</option>
        </select>
      </div>

      {/* Field Size Slider */}
      <div>
        <label
          htmlFor="fieldSize"
          className="block text-lg font-medium text-gray-700 mb-1"
        >
          Field Size (acres)
        </label>
        <div className="flex items-center space-x-4">
          <input
            id="fieldSize"
            type="range"
            min="0"
            max="10"
            step="0.1"
            value={fieldSize}
            onChange={(e) => setFieldSize(Number(e.target.value))}
            className="w-full accent-plant-green-core"
          />
          <span className="text-xl font-semibold text-gray-800">
            {fieldSize.toFixed(1)} acres
          </span>
        </div>
      </div>

      {/* Submit Button */}
      <div>
        <button
          type="submit"
          disabled={isLoading}
          className="w-full py-3 px-6 bg-air-blue-core text-white rounded-md text-xl font-bold hover:bg-air-blue-dark transition-colors disabled:opacity-50"
        >
          {isLoading ? "Analyzing..." : "Submit"}
        </button>
      </div>
    </form>
  );
};

export default FarmForm;

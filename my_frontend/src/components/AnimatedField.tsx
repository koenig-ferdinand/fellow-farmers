// src/components/AnimatedField.tsx
import React, { useEffect, useState } from "react";
import { ArrowDown, ArrowUp, ArrowLeft, ArrowRight } from "lucide-react";
import { motion } from "framer-motion";

interface AnimatedFieldProps {
  cropType: string;
  appliedProduct?: boolean;
  activeZone?: string; // 'soil','water','products','disease'
}

const AnimatedField: React.FC<AnimatedFieldProps> = ({
  cropType,
  appliedProduct,
  activeZone,
}) => {
  const [scale, setScale] = useState(appliedProduct ? 1.4 : 1);

  useEffect(() => {
    if (activeZone) {
      setScale(1.05);
      const timer = setTimeout(() => {
        setScale(appliedProduct ? 1.4 : 1);
      }, 300);
      return () => clearTimeout(timer);
    }
  }, [activeZone, appliedProduct]);

  const getCropImage = () => {
    switch (cropType.toLowerCase()) {
      case "rice":
        return "/rice-field.svg";
      case "wheat":
        return "/wheat-field.svg";
      case "cotton":
        return "/cotton-field.svg";
      default:
        return "/default-field.svg";
    }
  };

  const getHighlightClass = () => {
    if (!activeZone) return "";
    switch (activeZone) {
      case "soil":
        return "after:absolute after:inset-x-0 after:bottom-0 after:h-1/4 after:bg-green-400/20 after:animate-pulse-subtle";
      case "water":
        return "after:absolute after:inset-0 after:bg-blue-400/10 after:animate-pulse-subtle";
      case "products":
        return "after:absolute after:inset-x-0 after:top-1/4 after:h-2/4 after:bg-amber-400/20 after:animate-pulse-subtle";
      case "disease":
        return "after:absolute after:inset-x-0 after:top-0 after:h-1/3 after:bg-red-400/20 after:animate-pulse-subtle";
      default:
        return "";
    }
  };

  const getArrows = () => {
    if (!activeZone) return null;
    switch (activeZone) {
      case "soil":
        return (
          <div className="absolute bottom-32 left-1/2 transform -translate-x-1/2 text-green-600 animate-bounce">
            <ArrowDown size={28} className="filter drop-shadow-md" />
          </div>
        );
      case "water":
        return (
          <div className="absolute top-1/2 left-24 transform -translate-y-1/2 text-blue-600 animate-pulse">
            <ArrowRight size={28} className="filter drop-shadow-md" />
          </div>
        );
      case "products":
        return (
          <div className="absolute top-1/2 right-24 transform -translate-y-1/2 text-amber-600 animate-pulse">
            <ArrowLeft size={28} className="filter drop-shadow-md" />
          </div>
        );
      case "disease":
        return (
          <div className="absolute top-32 left-1/2 transform -translate-x-1/2 text-red-600 animate-bounce">
            <ArrowUp size={28} className="filter drop-shadow-md" />
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div
      className={`relative w-full h-full flex items-center justify-center ${getHighlightClass()}`}
    >
      {getArrows()}
      <div
        className="w-4/5 h-4/5 flex items-center justify-center transition-transform duration-300 field-glow rounded-2xl overflow-hidden"
        style={{ transform: `scale(${scale})` }}
      >
        <div className="relative w-full h-full flex items-center justify-center">
          <img
            src={getCropImage()}
            alt={`${cropType} field`}
            className="max-w-full max-h-full object-contain"
          />

          {/* Overlay with plant images */}
          <div className="absolute inset-0 pointer-events-none">
            <div className="absolute inset-0 grid grid-cols-3 grid-rows-3 gap-4 p-8">
              {Array.from({ length: 9 }).map((_, i) => (
                <div key={i} className="flex items-center justify-center">
                  <img
                    src="/lovable-uploads/3f9473b0-8750-49e6-b8e4-a7cf506d0db0.png"
                    alt="Plant"
                    className={`h-12 md:h-16 object-contain transition-all duration-500 filter drop-shadow-md ${
                      activeZone === "products"
                        ? "opacity-100 scale-110"
                        : activeZone === "disease"
                        ? "opacity-70"
                        : "opacity-90"
                    }`}
                    style={{
                      transform: `rotate(${Math.random() * 20 - 10}deg) scale(${
                        0.8 + Math.random() * 0.4
                      })`,
                    }}
                  />
                </div>
              ))}
            </div>

            {/* Additional overlays */}
            {activeZone === "water" && (
              <div className="absolute bottom-1/4 left-1/4 w-16 h-8">
                <div className="absolute inset-0 bg-blue-400/30 rounded-full animate-pulse"></div>
              </div>
            )}
            {activeZone === "soil" && (
              <div className="absolute bottom-0 inset-x-0 h-1/4 flex justify-around items-center">
                {[1, 2, 3].map((i) => (
                  <div
                    key={i}
                    className="w-4 h-4 bg-green-600/20 rounded-full animate-pulse"
                  ></div>
                ))}
              </div>
            )}
            {activeZone === "products" && (
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="w-1/2 h-1/3 border-2 border-amber-400/30 border-dashed rounded-lg"></div>
              </div>
            )}
            {activeZone === "disease" && (
              <div className="absolute top-1/4 inset-x-0 flex justify-around">
                {[1, 2].map((i) => (
                  <div
                    key={i}
                    className="w-5 h-5 bg-red-400/20 rounded-full animate-pulse"
                  ></div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnimatedField;

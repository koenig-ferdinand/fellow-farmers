// src/components/ActionPlan.tsx
import React from "react";

interface ActionPlanProps {
  selectedBoxes: string[]; // e.g. ['soil','water','disease','products']
}

const ActionPlan: React.FC<ActionPlanProps> = ({ selectedBoxes }) => {
  // Example tasks
  const tasksMap: Record<string, string[]> = {
    soil: ["Test soil pH", "Apply compost"],
    water: ["Irrigate every 3 days", "Monitor soil moisture"],
    disease: ["Inspect crops weekly", "Apply preventive spray if needed"],
    products: ["Use Bio-Fertilizer XL", "Track growth response"],
  };

  let combinedTasks: string[] = [];
  selectedBoxes.forEach((key) => {
    if (tasksMap[key]) {
      combinedTasks = [...combinedTasks, ...tasksMap[key]];
    }
  });

  return (
    <section className="py-12 bg-white">
      <div className="container mx-auto px-4 max-w-5xl">
        <h2 className="text-3xl font-bold text-gray-800 mb-6">Action Plan</h2>
        {/* Placeholder Calendar */}
        <div className="w-full h-64 bg-gray-200 rounded flex items-center justify-center mb-8">
          <span className="text-gray-500">[Calendar Placeholder]</span>
        </div>

        <h3 className="text-2xl font-semibold mb-2">Recommended Tasks</h3>
        <ul className="list-disc list-inside text-gray-700 text-lg">
          {combinedTasks.length > 0 ? (
            combinedTasks.map((task, idx) => <li key={idx}>{task}</li>)
          ) : (
            <li>No tasks selected.</li>
          )}
        </ul>
      </div>
    </section>
  );
};

export default ActionPlan;

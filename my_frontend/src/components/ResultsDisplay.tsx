// src/components/ResultsDisplay.tsx
import React, { useEffect, useRef } from "react";
import { StressResult } from "@/types";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Sun, Moon, CheckCircle, AlertTriangle, Info } from "lucide-react";

interface ResultsDisplayProps {
  results: StressResult;
}

const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ results }) => {
  const cardRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (cardRef.current) {
      cardRef.current.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  }, [results]);

  const getDiurnalStressLevel = (value: number) => {
    if (value < 0.3) return { label: "Low", color: "bg-green-500" };
    if (value < 0.7) return { label: "Moderate", color: "bg-yellow-500" };
    return { label: "High", color: "bg-red-500" };
  };

  const getNightStressLevel = (value: number) => {
    if (value < 0.3) return { label: "Low", color: "bg-green-500" };
    if (value < 0.7) return { label: "Moderate", color: "bg-yellow-500" };
    return { label: "High", color: "bg-red-500" };
  };

  const diurnalStress = getDiurnalStressLevel(results.diurnal_heat_stress);
  const nightStress = getNightStressLevel(results.night_heat_stress);

  return (
    <div ref={cardRef} className="w-full max-w-2xl mx-auto mt-12">
      <Card className="border border-gray-300 shadow-md overflow-hidden glass">
        <CardHeader className="bg-gradient-to-r from-farm-green/10 to-farm-light-green/10 pb-6">
          <div className="flex justify-between items-start">
            <div>
              <CardTitle className="text-xl font-medium">
                Analysis Results
              </CardTitle>
              <CardDescription className="mt-1">
                Based on your farm data
              </CardDescription>
            </div>
            <Badge
              variant="outline"
              className="bg-white/80 backdrop-blur-sm border-farm-green text-farm-green font-medium"
            >
              AI-Generated
            </Badge>
          </div>
        </CardHeader>
        <CardContent className="pt-6 pb-8 space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Daytime Heat */}
            <div className="space-y-4">
              <div className="flex items-center space-x-2 mb-2">
                <Sun className="h-5 w-5 text-farm-wheat" />
                <h3 className="font-medium text-lg">Daytime Heat Stress</h3>
              </div>
              <Progress
                value={results.diurnal_heat_stress * 100}
                className="h-2.5 bg-gray-100"
              />
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-500">
                  Stress Index: {(results.diurnal_heat_stress * 100).toFixed(0)}
                  %
                </span>
                <Badge
                  variant="outline"
                  className={`${diurnalStress.color.replace(
                    "bg-",
                    "bg-opacity-10 border-"
                  )} ${diurnalStress.color.replace("bg-", "text-")}`}
                >
                  {diurnalStress.label}
                </Badge>
              </div>
            </div>
            {/* Night Heat */}
            <div className="space-y-4">
              <div className="flex items-center space-x-2 mb-2">
                <Moon className="h-5 w-5 text-indigo-400" />
                <h3 className="font-medium text-lg">Night Heat Stress</h3>
              </div>
              <Progress
                value={results.night_heat_stress * 100}
                className="h-2.5 bg-gray-100"
              />
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-500">
                  Stress Index: {(results.night_heat_stress * 100).toFixed(0)}%
                </span>
                <Badge
                  variant="outline"
                  className={`${nightStress.color.replace(
                    "bg-",
                    "bg-opacity-10 border-"
                  )} ${nightStress.color.replace("bg-", "text-")}`}
                >
                  {nightStress.label}
                </Badge>
              </div>
            </div>
          </div>

          <div className="mt-8 space-y-6">
            <div className="p-4 rounded-lg border border-farm-green/20 bg-farm-green/5">
              <div className="flex items-start space-x-3">
                <CheckCircle className="h-6 w-6 text-farm-green flex-shrink-0 mt-0.5" />
                <div>
                  <h3 className="font-medium text-lg mb-2">Recommendation</h3>
                  <p className="text-gray-700">{results.recommendation}</p>
                </div>
              </div>
            </div>

            <div className="p-4 rounded-lg border border-farm-wheat/20 bg-farm-wheat/5">
              <div className="flex items-start space-x-3">
                <Info className="h-6 w-6 text-farm-wheat flex-shrink-0 mt-0.5" />
                <div>
                  <h3 className="font-medium text-lg mb-2">Rationale</h3>
                  <p className="text-gray-700">{results.rationale}</p>
                </div>
              </div>
            </div>
          </div>

          <div className="rounded-lg border border-gray-200 p-4 bg-gray-50/50">
            <h3 className="font-medium text-gray-700 mb-2 flex items-center">
              <AlertTriangle className="h-4 w-4 mr-2 text-farm-wheat" />
              Coming Soon
            </h3>
            <p className="text-sm text-gray-600">
              Future versions will include interactive maps, historical trends,
              crop-specific charts, and predictive modeling for optimal planting
              schedules.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ResultsDisplay;

// src/types.ts
export type CropType = "rice" | "cotton" | "maize" | "wheat";

export interface FarmFormData {
  location: string;
  cropType: CropType;
  fieldSize: number;
}

export interface StressResult {
  diurnal_heat_stress: number; // e.g. 0..1
  night_heat_stress: number; // e.g. 0..1
  recommendation: string;
  rationale: string;
}

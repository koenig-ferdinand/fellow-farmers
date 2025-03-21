// src/services/api.ts
export async function calculateDetailedStress(data: any): Promise<any> {
  return new Promise((resolve) => {
    // Mock some random results
    setTimeout(() => {
      resolve({
        diurnal_heat_stress: Math.random(), // 0..1
        night_heat_stress: Math.random(), // 0..1
        recommendation:
          "Apply mild irrigation in the afternoons. Consider extra N-fertilizer.",
        rationale:
          "Based on the temperature range and dryness index, your fields may need more water.",
      });
    }, 800);
  });
}

export async function getWeatherData(location: string): Promise<any> {
  return new Promise((resolve) => {
    // Mock weather data
    setTimeout(() => {
      resolve({
        location,
        forecast: "Sunny with scattered clouds",
        avgTemp: 25,
        rainfall: 12,
      });
    }, 500);
  });
}

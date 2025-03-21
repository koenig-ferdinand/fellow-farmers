/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx}",
    "./src/pages/**/*.{js,ts,jsx,tsx}",
    "./src/components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // Additional color keys used in your original code
      colors: {
        "air-blue-core": "#009ddc",
        "air-blue-dark": "#0082ba",
        "plant-green-core": "#4c9a2a",
        "sun-orange-mid": "#f4a03b",
        "farm-green": "#4c9a2a",
        "farm-light-green": "#a5d6a7",
        "farm-wheat": "#fbc02d",
      },
      keyframes: {
        "pulse-subtle": {
          "0%": { opacity: "0.6" },
          "50%": { opacity: "1" },
          "100%": { opacity: "0.6" },
        },
      },
      animation: {
        "pulse-subtle": "pulse-subtle 1.5s infinite",
      },
    },
  },
  plugins: [],
};

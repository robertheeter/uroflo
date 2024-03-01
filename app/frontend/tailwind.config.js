/** @type {import('tailwindcss').Config} */
export default {
  mode: "jit",
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      animation: {
        moveToLeft: "moveToLeft 1s 1s forwards",
      },
      keyframes: {
        moveToLeft: {
          "0%": { transform: "translateX(0)" },
          "100%": { transform: "translateX(-25%)" },
        },
        transitionDelay: {
          3: "3s",
        },
      },
    },
  },
  plugins: [],
};

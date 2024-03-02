/** @type {import('tailwindcss').Config} */
export default {
  mode: "jit",
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      animation: {
        moveToLeft: "moveToLeft 1s 1s forwards",
        fadeInMoveLeft: "fadeInMoveLeft 2s forwards",
      },
      keyframes: {
        moveToLeft: {
          "0%": { transform: "translateX(0)" },
          "100%": { transform: "translateX(-25%)" },
        },
        fadeInMoveLeft: {
          "0%": {
            opacity: 0,
            transform: "translateX(0)",
          },
          "50%": {
            opacity: 1,
          },
          "100%": {
            opacity: 1,
            transform: "translateX(-25%)", // replace with the actual distance you want the logo to move
          },
        },
      },
      transitionDelay: {
        3: "3s",
      },
    },
  },
  plugins: [],
};

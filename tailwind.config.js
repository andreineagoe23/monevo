/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        ink: {
          950: "#0B0B0F",
          900: "#111117",
          800: "#17171F",
          700: "#1F1F28",
          600: "#2A2A35",
        },
        paper: {
          50: "#FAF7F2",
          100: "#F3EFE7",
          200: "#E8E2D5",
          300: "#D9D1BE",
        },
        amber: {
          300: "#F2C97A",
          400: "#E7B35A",
          500: "#D99A3E",
          600: "#B87C28",
        },
        muted: {
          dark: "#8A8A95",
          light: "#6B6658",
        },
      },
      fontFamily: {
        sans: ["Satoshi", "Cabinet Grotesk", "Inter", "system-ui", "sans-serif"],
        display: ["Instrument Serif", "Zodiak", "Georgia", "serif"],
      },
      letterSpacing: {
        tightest: "-0.035em",
      },
      fontSize: {
        display: ["clamp(3rem, 8vw, 7rem)", { lineHeight: "1", letterSpacing: "-0.035em" }],
      },
      animation: {
        "fade-in": "fadeIn 0.6s ease-out",
        "slide-up": "slideUp 0.6s ease-out",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%": { transform: "translateY(24px)", opacity: "0" },
          "100%": { transform: "translateY(0)", opacity: "1" },
        },
      },
    },
  },
  plugins: [],
};

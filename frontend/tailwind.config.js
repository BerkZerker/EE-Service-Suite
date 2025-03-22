/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f5f8ff',
          100: '#e0ecff',
          200: '#c1d7ff',
          300: '#94bbff',
          400: '#629aff',
          500: '#3d77ff',
          600: '#2f56f5',
          700: '#1d3dd7',
          800: '#1e35ab',
          900: '#1d3285',
        },
        secondary: {
          50: '#f3f8fa',
          100: '#deedf2',
          200: '#bfdbe5',
          300: '#92c1d1',
          400: '#5fa0b6',
          500: '#3c7e9a',
          600: '#2e678a',
          700: '#28536f',
          800: '#25455c',
          900: '#213b4d',
        },
      },
    },
  },
  plugins: [],
}
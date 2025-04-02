/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Map theme names to CSS variables
        background: 'var(--color-background)',
        card: 'var(--color-card)',
        text: {
          DEFAULT: 'var(--color-text)', // Default text color
          primary: 'var(--color-text)', // Explicitly map text-primary if needed elsewhere
          secondary: 'var(--color-text-secondary, var(--color-text))', // Add secondary if needed, fallback to default
        },
        primary: {
          DEFAULT: 'var(--color-primary)',
          focus: 'var(--color-accent)', // Use accent for focus ring
          text: 'var(--color-primary-text)', // Text color for primary elements
        },
        secondary: 'var(--color-secondary)',
        accent: 'var(--color-accent)',
        border: 'var(--color-border)',
      },
    },
  },
  plugins: [],
}

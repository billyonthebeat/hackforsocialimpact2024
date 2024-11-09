/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      "./src/**/*.{js,jsx,ts,tsx}",
    ],
    theme: {
      extend: {
        colors: {
          'card': 'var(--card)',
          'card-foreground': 'var(--card-foreground)',
        },
      },
    },
    plugins: [],
  }
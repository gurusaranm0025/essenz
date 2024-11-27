/** @type {import('tailwindcss').Config} */
// import {defin} from 'tailwindcss'

export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    "./src/index.css"
  ],
  theme: {
    extend: {
      colors: {
        'ivory': '#FFFFF8',
        cream: '#FFF2E0',
        'light-sand': '#DAD5BE',
        'pale-wheat': '#E0D9B8',
        'golden-wheat': '#ADA261'
      }
    },
  },
  plugins: [],
}


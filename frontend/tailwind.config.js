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
        'golden-wheat': '#ADA261',

        'light-purple': '#C4C3E3',
        'dark-purple': '#504E76',
        'creamy-white': '#FDF8E2',
        'pixel-green': '#A3B565',
        'accent-red': '#F1642E',
        'warning-orange': '#FCDD9D',

        'whitey-white': '#FEFEFE',
        'greeny-dark-green': '#415111',
        'greeny-light-green': '#D2E186',
        'orangey-orang': '#FB8159'
      }
    },
  },
  plugins: [],
}


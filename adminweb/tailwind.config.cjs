
// const defaultTheme = require('tailwindcss/defaultTheme')

const colors = require("./src/cfg/colors.cjs")
const defaultTheme = require('tailwindcss/defaultTheme')

let colorMap = {
	white: colors.white,
	black: colors.black,
	transparent: "transparent",
	grey: colors.grey,
	red: colors.red,
	green: colors.green,
	//    purpel: colors.purple,
	deepPurpel: colors.deepPurple,
	blue: colors.blue,
	orange: colors.orange,
	deepOrange: colors.deepOrange,
	amber: colors.amber,
	//    brown: colors.grey,
	blueGrey: colors.blueGrey,

}

let colorMap2 = {
	theme: {
		primary: colorMap.blueGrey['600'],
		primaryDark: colorMap.blueGrey['800'],
		primaryLight: colorMap.blueGrey['200'],
		secondary: colorMap.orange['a700'],
		secondaryLight: colorMap.orange['a400'],
		background: colorMap.blueGrey['50'],
		surface: colorMap.white,
		error: colorMap.red['600'],
		onPrimary: colorMap.white,
		onPrimaryInactive: colorMap.grey['400'],
		onSecondary: colorMap.white,
		onSecondaryInactive: colorMap.grey['400'],
		onBackground: colorMap.black,
		onBackgroundInactive: colorMap.grey['500'],
		onSurface: colorMap.black,
		onSurfaceInactive: colorMap.grey['500'],
		onError: colorMap.black,
		onErrorInactive: colorMap.grey['500'],

	},
	...colorMap
}


const config = {
	mode: "jit",
	purge: [
		"./src/**/*.{html,js,svelte,ts}",
	],
	darkMode: false, // or 'media' or 'class'
	theme: {
		extend: {
			width: {
				"1/7": "14.2857143%",
				"2/7": "28.5714286%",
				"3/7": "42.8571429%",
				"4/7": "57.1428571%",
				"5/7": "71.4285714%",
			},
		},
		screens: {
			'xs': '475px',
			...defaultTheme.screens,
		},
		fontSize: {
			"5xl": "6rem",
			"4xl": "3.75rem",
			"3xl": "3rem",
			"2xl": "2.125rem",
			xl: "1.5rem",
			lg: "1.25rem",
			base: "1rem",
			sm: "0.875rem",
			xs: "0.75rem",
		},
		lineHeight: {
			none: 1,
			tight: 1.25,
			normal: 1.45,
			relaxed: 1.75,
			loose: 2,
		},
		colors: colorMap2,
		fontFamily: {
			sans: ['Roboto', 'sans-serif', 'ui-sans-serif'],
			serif: ['ui-serif', 'Georgia', 'Cambria', '"Times New Roman"', 'Times', 'serif'],
			mono: ['Menlo', 'ui-monospace', 'SFMono-Regular', 'Courier\ New', 'Monaco', 'monospace'],
		},
		zIndex: {
			'0': 0,
			'back': 0,
			'10': 10,
			'20': 20,
			'tools': 25,
			'30': 30,
			'overlay': 35,
			'40': 40,
			'front': 45,
			'50': 50,
			'modal': 100,
			'auto': 'auto'
		},
	},
	variants: {
		extend: {
			visibility: ['hover', 'focus'],
		},
		scrollSnapType: ['responsive'],
	},
	plugins: [
		require('tailwindcss-scroll-snap'),
		require('tailwindcss-elevation')(['responsive']),

	],
};

module.exports = config;

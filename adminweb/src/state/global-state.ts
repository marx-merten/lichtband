import watchMedia from "svelte-media";

const mediaqueries = {
    xs: "(max-width: 639px)",
    sm: "(min-width: 640px)",
    md: "(min-width: 768px)",
    lg: "(min-width: 1024px)",
    xl: "(min-width: 1280px)",
    xxl: "(min-width: 1536px)",
    short: "(max-height: 399px)",
    dark: "(prefers-color-scheme: dark)",
    noanimations: "(prefers-reduced-motion: reduce)"
};


export const media = watchMedia(mediaqueries);

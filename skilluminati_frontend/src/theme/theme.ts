// src/theme/theme.ts
import type { Theme } from "@emotion/react";

export type ThemeName = "light" | "dark";

export const darkTheme: Theme = {
  colors: {
    // page background
    background: "#05070B", // very dark, almost black
    // cards / panels
    surface: "#0D1015",
    surfaceAlt: "#11141A",
    // text
    text: "#F4F5F6",
    textMuted: "rgba(244,245,246,0.55)",
    // borders / separators
    border: "rgba(244,245,246,0.04)",
    // accent (like that blue button / progress)
    primary: "#3B82F6", // you can tweak to #4363ff if you want closer to the image
  },
};

export const lightTheme: Theme = {
  colors: {
    background: "#F5F5F5",
    surface: "#FFFFFF",
    surfaceAlt: "#F0F2F5",
    text: "#0F172A",
    textMuted: "#6B7280",
    border: "rgba(15,23,42,0.08)",
    primary: "#2563EB",
  },
};

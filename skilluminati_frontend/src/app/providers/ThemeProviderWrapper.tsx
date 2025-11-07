// src/context/ThemeProviderWrapper.tsx (or wherever you keep it)
import React, { createContext, useContext, useMemo, useState } from "react";
import type { Theme as EmotionTheme } from "@emotion/react";
import { ThemeProvider as EmotionThemeProvider } from "@emotion/react";
import {
  ThemeProvider as MUIThemeProvider,
  createTheme,
} from "@mui/material/styles";
import { darkTheme, lightTheme, type ThemeName } from "../../theme/theme";

type ThemeContextValue = {
  theme: EmotionTheme;
  setTheme: (name: ThemeName) => void;
  toggleTheme: () => void;
};

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined);
const THEME_KEY = "skilluminati_theme";

export const ThemeProviderWrapper: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [themeName, setThemeName] = useState<ThemeName>("dark");

  // load from storage / system
  React.useEffect(() => {
    const stored = localStorage.getItem(THEME_KEY) as ThemeName | null;
    if (stored) {
      setThemeName(stored);
    } else {
      const prefersDark = window.matchMedia?.(
        "(prefers-color-scheme: dark)"
      ).matches;
      if (prefersDark) setThemeName("dark");
    }
  }, []);

  // pick our emotion theme (your custom one)
  const emotionTheme = useMemo<EmotionTheme>(
    () => (themeName === "dark" ? darkTheme : lightTheme),
    [themeName]
  );

  // build a matching MUI theme so Container, Button, etc. don’t crash
  const muiTheme = useMemo(
    () =>
      createTheme({
        palette: {
          mode: themeName === "dark" ? "dark" : "light",
          background: {
            default:
              themeName === "dark"
                ? darkTheme.colors.background
                : lightTheme.colors.background,
            paper:
              themeName === "dark"
                ? darkTheme.colors.surface
                : lightTheme.colors.surface,
          },
          primary: {
            main:
              themeName === "dark"
                ? darkTheme.colors.primary
                : lightTheme.colors.primary,
          },
          text: {
            primary:
              themeName === "dark"
                ? darkTheme.colors.text
                : lightTheme.colors.text,
            secondary:
              themeName === "dark"
                ? darkTheme.colors.textMuted
                : lightTheme.colors.textMuted,
          },
        },
      }),
    [themeName]
  );

  // keep <html> class and css vars in sync
  React.useEffect(() => {
    const root = document.documentElement;
    if (themeName === "dark") root.classList.add("dark");
    else root.classList.remove("dark");
    localStorage.setItem(THEME_KEY, themeName);
  }, [themeName]);

  React.useEffect(() => {
    const root = document.documentElement;
    root.style.setProperty("--bg", emotionTheme.colors.background);
    root.style.setProperty("--surface", emotionTheme.colors.surface);
    root.style.setProperty("--surface-alt", emotionTheme.colors.surfaceAlt);
    root.style.setProperty("--text", emotionTheme.colors.text);
    root.style.setProperty("--text-muted", emotionTheme.colors.textMuted);
    root.style.setProperty("--border", emotionTheme.colors.border);
    root.style.setProperty("--primary", emotionTheme.colors.primary);
  }, [emotionTheme]);

  const setTheme = (name: ThemeName) => setThemeName(name);
  const toggleTheme = () =>
    setThemeName((prev) => (prev === "dark" ? "light" : "dark"));

  return (
    <ThemeContext.Provider
      value={{ theme: emotionTheme, setTheme, toggleTheme }}
    >
      {/* MUI needs its provider */}
      <MUIThemeProvider theme={muiTheme}>
        {/* Emotion theme for your custom styles */}
        <EmotionThemeProvider theme={emotionTheme}>
          {children}
        </EmotionThemeProvider>
      </MUIThemeProvider>
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const ctx = useContext(ThemeContext);
  if (!ctx)
    throw new Error("useTheme must be used within ThemeProviderWrapper");
  return ctx;
};

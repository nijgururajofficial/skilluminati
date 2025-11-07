// src/types/emotion.d.ts
import "@emotion/react";

declare module "@emotion/react" {
  export interface Theme {
    colors: {
      background: string;
      surface: string;
      surfaceAlt: string;
      text: string;
      textMuted: string;
      border: string;
      primary: string;
    };
  }
}

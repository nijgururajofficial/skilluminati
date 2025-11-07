// src/theme/typography.ts
export class AppTypography {
  // Homepage headline
  static homepageTitle = {
    fontFamily: `'Inter', 'Plus Jakarta Sans', 'Helvetica Neue', Arial, sans-serif`,
    fontWeight: 400,
    fontSize: "2.5rem", // 40px
    lineHeight: 1.2,
    letterSpacing: "-0.02em",
    color: "#FFFFFF",
    m: "2vh",
  };

  // Homepage Sub-Title
  static homepageSubTitle = {
    fontFamily: `'Inter', 'Plus Jakarta Sans', 'Helvetica Neue', Arial, sans-serif`,
    fontWeight: 600,
    fontSize: "4vw", // 40px
    lineHeight: 1.2,
    letterSpacing: "-0.02em",
    color: "#FFFFFF",
    mx: "2vh",
    my: "5vh",
  };

  // Dashboard greeting — "Hi, Alex! Ready to land your next role?"
  static dashboardTitle = {
    fontFamily: `'Inter', 'Plus Jakarta Sans', 'Helvetica Neue', Arial, sans-serif`,
    fontWeight: 600,
    fontSize: "1.75rem", // 28px
    lineHeight: 1.3,
    letterSpacing: "-0.01em",
    color: "#FFFFFF",
  };

  // Section titles — "Skill Progress", "Quick Actions"
  static sectionTitle = {
    fontFamily: `'Inter', 'Plus Jakarta Sans', 'Helvetica Neue', Arial, sans-serif`,
    fontWeight: 500,
    fontSize: "1.125rem", // 18px
    lineHeight: 1.4,
    color: "#E5E7EB",
  };

  // Body / descriptive text — e.g., “Let’s check your progress…”
  static bodyText = {
    fontFamily: `'Inter', 'Plus Jakarta Sans', 'Helvetica Neue', Arial, sans-serif`,
    fontWeight: 400,
    fontSize: "1rem", // 16px
    lineHeight: 1.6,
    color: "#9CA3AF",
  };

  // Small UI labels — “Remember me”, “Analyze New Job”, etc.
  static label = {
    fontFamily: `'Inter', 'Plus Jakarta Sans', 'Helvetica Neue', Arial, sans-serif`,
    fontWeight: 500,
    fontSize: "0.875rem", // 14px
    lineHeight: 1.4,
    color: "#9CA3AF",
  };

  // Button text
  static button = {
    fontFamily: `'Inter', 'Plus Jakarta Sans', 'Helvetica Neue', Arial, sans-serif`,
    fontWeight: 600,
    fontSize: "0.9375rem", // 15px
    lineHeight: 1.4,
    letterSpacing: "0.02em",
    color: "#FFFFFF",
  };

  // PAGE CONTAINER
  static jobAnalyzerContainer = {
    backgroundColor: "#0f172a",
    color: "#e2e8f0",
    minHeight: "100vh",
    padding: "40px",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    fontFamily: `'Inter', 'Plus Jakarta Sans', 'Helvetica Neue', Arial, sans-serif`,
  };

  // MAIN CARD WRAPPER
  static jobAnalyzerCard = {
    backgroundColor: "#111827",
    borderRadius: "20px",
    padding: "32px",
    maxWidth: "960px",
    width: "100%",
    boxShadow: "0 20px 40px rgba(0,0,0,0.25)",
    border: "1px solid rgba(255,255,255,0.06)",
  };

  // TITLE
  static jobAnalyzerTitle = {
    fontWeight: 600,
    fontSize: "1.8rem",
    color: "#f9fafb",
    mb: 1,
  };

  // SUBTITLE / DESCRIPTION
  static jobAnalyzerSubtitle = {
    fontWeight: 400,
    fontSize: "1rem",
    color: "rgba(226,232,240,0.7)",
    mb: 3,
  };

  // INPUT SECTION
  static jobAnalyzerInputCard = {
    backgroundColor: "#1f2937",
    borderRadius: "16px",
    padding: "24px",
    border: "1px solid rgba(255,255,255,0.06)",
    mb: 4,
  };

  static jobAnalyzerInputTabs = {
    display: "flex",
    gap: "8px",
    mb: 2,
  };

  static jobAnalyzerTabButton = {
    textTransform: "none",
    fontWeight: 500,
    color: "#cbd5e1",
    "&.Mui-selected": {
      color: "#3b82f6",
      backgroundColor: "rgba(59,130,246,0.1)",
    },
  };

  static jobAnalyzerTextarea = {
    width: "100%",
    backgroundColor: "#0f172a",
    color: "#e2e8f0",
    borderRadius: "12px",
    border: "1px solid rgba(255,255,255,0.1)",
    padding: "16px",
    fontSize: "0.95rem",
    "&::placeholder": {
      color: "rgba(226,232,240,0.4)",
    },
  };

  static jobAnalyzerAnalyzeButton = {
    backgroundColor: "#3b82f6",
    color: "#fff",
    textTransform: "none",
    fontWeight: 600,
    borderRadius: "10px",
    px: 3,
    py: 1.2,
    mt: 2,
    "&:hover": {
      backgroundColor: "#2563eb",
    },
  };

  // TOP METRICS BAR
  static jobAnalyzerMetricsBar = {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    fontSize: "0.95rem",
    color: "#94a3b8",
    backgroundColor: "#1f2937",
    borderRadius: "10px",
    px: 2,
    py: 1.5,
    mb: 3,
  };

  // SKILL CARDS
  static jobAnalyzerSkillCardsWrapper = {
    display: "flex",
    flexWrap: "wrap",
    gap: "20px",
    mb: 5,
  };

  static jobAnalyzerSkillCard = {
    backgroundColor: "#1f2937",
    borderRadius: "16px",
    padding: "20px",
    width: "280px",
    border: "1px solid rgba(255,255,255,0.08)",
    transition: "transform 0.2s ease, box-shadow 0.2s ease",
    "&:hover": {
      transform: "translateY(-4px)",
      boxShadow: "0 8px 20px rgba(0,0,0,0.4)",
    },
  };

  static jobAnalyzerSkillTitle = {
    fontWeight: 600,
    fontSize: "1.1rem",
    color: "#f9fafb",
    mb: 1,
  };

  static jobAnalyzerSkillMeta = {
    fontSize: "0.85rem",
    color: "#94a3b8",
    mb: 1,
  };

  static jobAnalyzerSkillLink = {
    fontSize: "0.85rem",
    color: "#3b82f6",
    cursor: "pointer",
    textDecoration: "none",
    "&:hover": {
      textDecoration: "underline",
    },
  };

  // TABLE SECTION
  static jobAnalyzerTableContainer = {
    backgroundColor: "#1f2937",
    borderRadius: "16px",
    border: "1px solid rgba(255,255,255,0.06)",
    overflow: "hidden",
    mb: 4,
  };

  static jobAnalyzerTableHeader = {
    backgroundColor: "rgba(255,255,255,0.05)",
    color: "#cbd5e1",
    fontWeight: 600,
    fontSize: "0.9rem",
  };

  static jobAnalyzerTableCell = {
    color: "#e2e8f0",
    fontSize: "0.9rem",
    borderColor: "rgba(255,255,255,0.05)",
  };

  // CALL-TO-ACTION
  static jobAnalyzerCTASection = {
    textAlign: "center",
    mt: 5,
  };

  static jobAnalyzerCTAButton = {
    backgroundColor: "#3b82f6",
    color: "#fff",
    textTransform: "none",
    fontWeight: 600,
    borderRadius: "12px",
    px: 3,
    py: 1.5,
    "&:hover": {
      backgroundColor: "#2563eb",
    },
  };

  static jobAnalyzerViewLink = {
    color: "#3b82f6",
    fontSize: "0.9rem",
    display: "inline-block",
    mt: 2,
    textDecoration: "none",
    "&:hover": {
      textDecoration: "underline",
    },
  };
}

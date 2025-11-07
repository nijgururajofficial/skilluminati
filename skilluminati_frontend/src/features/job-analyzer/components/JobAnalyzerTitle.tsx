import { Box, Chip, Typography } from "@mui/material";

export const JobAnalyzerTitle = () => {
  return (
    <Box mb={1}>
      <Chip
        label="Skilluminati"
        sx={{
          mb: 1.5,
          fontWeight: 600,
          letterSpacing: 1.2,
          bgcolor: "rgba(96,165,250,0.18)",
          color: "rgba(191,219,254,0.95)",
          borderRadius: 1,
          px: 1.5,
          py: 0.5,
          textTransform: "uppercase",
        }}
      />
      <Typography
        variant="h3"
        fontWeight={800}
        sx={{
          lineHeight: 1.1,
          background: "linear-gradient(135deg, #60a5fa 0%, #a855f7 50%, #f472b6 100%)",
          WebkitBackgroundClip: "text",
          WebkitTextFillColor: "transparent",
        }}
      >
        Decode the job. Focus your prep.
      </Typography>
      <Typography variant="body1" sx={{ opacity: 0.72, mt: 1.5, maxWidth: 520 }}>
        Paste the role you’re targeting and let Skilluminati surface the critical skills and what to do next.
      </Typography>
    </Box>
  );
};

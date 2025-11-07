import { Box, TextField, Typography } from "@mui/material";

type Props = {
  value: string;
  onChange: (val: string) => void;
};

export const JobAnalyzerInputJDField = ({ value, onChange }: Props) => {
  return (
    <Box>
      <Typography
        variant="subtitle2"
        sx={{ mb: 1, color: "rgba(255,255,255,0.76)", textTransform: "uppercase", letterSpacing: 1.1 }}
      >
        Job description
      </Typography>
      <TextField
        multiline
        minRows={8}
        maxRows={12}
        fullWidth
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Paste the job description here..."
        sx={{
          "& .MuiInputBase-root": {
            background: "rgba(15,23,42,0.35)",
            borderRadius: 3,
            color: "rgba(226,232,240,0.95)",
            border: "1px solid rgba(148,163,184,0.32)",
            boxShadow: "0 10px 30px rgba(15,23,42,0.25)",
          },
          "& .MuiInputBase-input": {
            overflowY: "auto",
          },
          "& .MuiOutlinedInput-notchedOutline": {
            borderColor: "transparent",
          },
          "& .MuiInputBase-root.Mui-focused .MuiOutlinedInput-notchedOutline": {
            borderColor: "rgba(96,165,250,0.85)",
          },
          "& textarea::placeholder": {
            color: "rgba(148,163,184,0.6)",
          },
        }}
      />
    </Box>
  );
};

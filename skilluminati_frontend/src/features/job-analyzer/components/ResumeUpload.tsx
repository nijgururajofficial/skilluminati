import { Box, Button, Chip, Stack, Typography } from "@mui/material";
import UploadFileIcon from "@mui/icons-material/UploadFile";
import CloseIcon from "@mui/icons-material/Close";
import type { ChangeEvent } from "react";

type ResumeUploadProps = {
  file: File | null;
  onSelect: (file: File | null) => void;
  disabled?: boolean;
  helperText?: string;
};

const ACCEPTED_FILE_TYPES = "application/pdf";

export const ResumeUpload = ({
  file,
  onSelect,
  disabled = false,
  helperText = "Attach a recent PDF resume to personalize the analysis.",
}: ResumeUploadProps) => {
  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (!selectedFile) {
      onSelect(null);
      return;
    }

    if (selectedFile.type !== ACCEPTED_FILE_TYPES) {
      // Let parent handle validation messaging if needed
      onSelect(null);
      return;
    }

    onSelect(selectedFile);
  };

  const handleClear = () => {
    if (disabled) return;
    onSelect(null);
  };

  return (
    <Stack spacing={1.5}>
      <Typography variant="subtitle2" sx={{ color: "rgba(255,255,255,0.7)" }}>
        Resume (optional)
      </Typography>
      <Button
        component="label"
        variant="outlined"
        size="large"
        startIcon={<UploadFileIcon />}
        disabled={disabled}
        sx={{
          justifyContent: "flex-start",
          textTransform: "none",
          color: "rgba(255,255,255,0.85)",
          borderColor: "rgba(148,163,184,0.35)",
          bgcolor: "rgba(15,23,42,0.25)",
          "&:hover": {
            borderColor: "rgba(96,165,250,0.9)",
            bgcolor: "rgba(37,99,235,0.08)",
          },
          "&.Mui-disabled": {
            borderColor: "rgba(148,163,184,0.15)",
            color: "rgba(148,163,184,0.35)",
          },
        }}
      >
        Upload PDF resume
        <input
          hidden
          type="file"
          accept="application/pdf"
          onChange={handleFileChange}
        />
      </Button>

      <Typography variant="caption" sx={{ color: "rgba(148,163,184,0.75)" }}>
        {helperText}
      </Typography>

      {file && (
        <Box>
          <Chip
            label={file.name}
            onDelete={disabled ? undefined : handleClear}
            deleteIcon={<CloseIcon />}
            sx={{
              bgcolor: "rgba(96,165,250,0.2)",
              color: "white",
              "& .MuiChip-deleteIcon": {
                color: "rgba(255,255,255,0.75)",
              },
            }}
          />
          <Typography
            variant="caption"
            sx={{ display: "block", mt: 0.5, color: "rgba(148,163,184,0.65)" }}
          >
            {Math.round(file.size / 1024)} KB · PDF
          </Typography>
        </Box>
      )}
    </Stack>
  );
};


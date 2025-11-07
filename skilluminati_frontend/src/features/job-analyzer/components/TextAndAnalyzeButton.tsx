import { Box, Button, CircularProgress, Typography } from "@mui/material";

type Props = {
  onAnalyze: () => void;
  disabled?: boolean;
  isLoading?: boolean;
};

export const TextAndAnalyzeButton = ({
  onAnalyze,
  disabled = false,
  isLoading = false,
}: Props) => {
  return (
    <Box mt={1}>
      <Typography variant="body2" sx={{ opacity: 0.7 }}>
        We look at responsibilities, requirements, and tool mentions.
      </Typography>
      <Button
        variant="contained"
        sx={{ mt: 2, minWidth: 180 }}
        onClick={onAnalyze}
        disabled={disabled || isLoading}
      >
        {isLoading ? (
          <>
            <CircularProgress size={18} sx={{ color: "white", mr: 1 }} />
            Analyzing…
          </>
        ) : (
          "Analyze job"
        )}
      </Button>
    </Box>
  );
};

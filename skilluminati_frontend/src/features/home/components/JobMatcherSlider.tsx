import { Box, Button, Typography } from "@mui/material";

export const JobMatcherSlider = () => {
  return (
    <Box
      display={"grid"}
      width={"70vw"}
      gridTemplateAreas={
        '"job-name-and-score-button circular-progress-indicator"'
      }
      gridTemplateColumns={"2fr 1fr"}
      sx={{ placeSelf: "center" }}
    >
      <Box gridArea={"job-name-and-score-button"}>
        <Typography variant="h5">
          Your Current Role Target <br />
          Product Data Analyst | Spotify
        </Typography>
        <Button variant="contained" sx={{ mt: 2 }}>
          Send
        </Button>
      </Box>
      <Box
        gridArea={"circular-progress-indicator"}
        sx={{ placeSelf: "center" }}
      >
        Put a circular Progress indicator here
      </Box>
    </Box>
  );
};

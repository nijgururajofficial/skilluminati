import { Box, Typography } from "@mui/material";

export const QuickActions = () => {
  return (
    <Box
      display="grid"
      gridTemplateColumns="0.2fr 1fr 0.2fr 1fr 0.2fr"
      gridTemplateAreas='"space-start continue-learning space-middle improve-your-skills space-end"'
      mt={2}
    >
      <Box gridArea={"space-start"}></Box>
      <Typography
        gridArea="continue-learning"
        bgcolor="primary.main"
        color="white"
        p={2}
        borderRadius={2}
        // sx={{ placeSelf: "center" }}
      >
        Continue learning
      </Typography>
      <Box gridArea={"space-middle"}></Box>
      <Typography
        gridArea="improve-your-skills"
        bgcolor="secondary.main"
        color="white"
        p={2}
        borderRadius={2}
        // sx={{ placeSelf: "center" }}
      >
        Improve your skills
      </Typography>
      <Box gridArea={"space-end"}></Box>
    </Box>
  );
};

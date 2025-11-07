import { Box, Typography } from "@mui/material";
import { AppTypography } from "../../../common/constants/AppTypography";
import { HomeSubTitle } from "./HomeSubTitle";

export const HomeTitle = () => {
  return (
    <Box>
      <Typography variant="h5" sx={AppTypography.dashboardTitle}>
        Hi, Rohan! <br /> Ready to land your next role?
      </Typography>
      <HomeSubTitle />
    </Box>
  );
};

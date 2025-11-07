import { Typography } from "@mui/material";
import { AppTypography } from "../../../common/constants/AppTypography";

export const HomeSubTitle = () => {
  return (
    <Typography variant="subtitle1" sx={AppTypography.bodyText}>
      Let's check your progress and skills for your target job.
    </Typography>
  );
};

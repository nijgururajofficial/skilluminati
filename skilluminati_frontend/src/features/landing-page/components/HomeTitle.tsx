import { Typography } from "@mui/material";
import { AppTypography } from "../../../common/constants/AppTypography";

export const HomeTitle = () => {
  return (
    <Typography sx={AppTypography.homepageSubTitle}>
      Turn any job description <br /> into a personalized <br />
      learning roadmap.
    </Typography>
  );
};

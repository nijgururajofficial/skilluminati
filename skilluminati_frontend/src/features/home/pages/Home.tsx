import { Box } from "@mui/material";
import { HomeNavbar } from "../components/HomeNavbar";
import { HomeTitle } from "../components/HomeTitle";
import { QuickActions } from "../components/QuickActions";
import { JobMatcherSlider } from "../components/JobMatcherSlider";

export const Home = () => {
  return (
    <Box
      display="flex"
      flexDirection="column"
      height={"100vh"}
      gap={2}
      mx={"4vw"}
      justifyContent="space-around" // 👈 evenly spreads vertical space
    >
      <HomeNavbar />
      <HomeTitle />
      <JobMatcherSlider></JobMatcherSlider>
      <QuickActions></QuickActions>
    </Box>
  );
};

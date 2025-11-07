import Container from "@mui/material/Container";
import { HomeTitle } from "../components/HomeTitle";
import { TopBar } from "../components/TopBar";
import { Registration } from "../../registration/pages/Registration";

export const LandingPage = () => {
  return (
    <Container
      disableGutters
      maxWidth={false}
      sx={{ width: "95%", mx: "2vw", justifySelf: "center" }}
    >
      <TopBar />
      <HomeTitle />
      <Registration firstTimeUser={false} />
    </Container>
  );
};

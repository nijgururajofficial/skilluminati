import { Box } from "@mui/material";
import { LoginWindow } from "../components/LoginWindow";
import { SignUpWindow } from "../components/SignUpWindow";

interface RegistrationProps {
  firstTimeUser: boolean;
}

export const Registration = ({ firstTimeUser }: RegistrationProps) => {
  return (
    <>
      <Box width={"50vw"} p={"3vw"} sx={{ placeSelf: "center" }}>
        {firstTimeUser ? (
          <SignUpWindow></SignUpWindow>
        ) : (
          <LoginWindow></LoginWindow>
        )}
      </Box>
    </>
  );
};

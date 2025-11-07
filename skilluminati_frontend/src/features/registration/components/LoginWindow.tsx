import { Box, Button, Link, Typography } from "@mui/material";
import { Constants } from "../../../constants/Constants";
import { useNavigate } from "react-router-dom";
import { InputTextFields } from "../../../common/components/InputTexFields";

export const LoginWindow = () => {
  const navigate = useNavigate();

  const handleSignUpClick = () => {
    navigate("/signup");
  };
  return (
    <Box m="4vw" sx={{ placeSelf: "center" }}>
      {Constants.LOGIN_INPUT_ATTRIBUTES.map((fieldName) => (
        <InputTextFields key={fieldName} name={fieldName} />
      ))}
      <Button
        variant="contained"
        sx={{ mt: 2, alignItems: "center", justifyContent: "center" }}
      >
        LOGIN
      </Button>
      <Box height={"2vh"}></Box>
      <Typography>
        Don't have an account?{" "}
        <Link
          component="button"
          onClick={handleSignUpClick}
          sx={{
            color: "#1976d2", // 👈 your chosen color (default MUI blue)
            fontWeight: "bold",
            textDecoration: "none",
            "&:hover": {
              textDecoration: "underline",
              color: "#1565c0", // slightly darker on hover
            },
          }}
        >
          Sign Up
        </Link>
      </Typography>
    </Box>
  );
};

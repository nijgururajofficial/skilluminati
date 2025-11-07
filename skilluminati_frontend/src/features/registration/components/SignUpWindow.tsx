import { Box, Button } from "@mui/material";
import { Constants } from "../../../constants/Constants";
import { InputTextFields } from "../../../common/components/InputTexFields";

export const SignUpWindow = () => {
  return (
    <Box m="4vw" sx={{ placeSelf: "center" }}>
      {Constants.SIGNUP_INPUT_ATTRIBUTES.map((fieldName) => (
        <InputTextFields key={fieldName} name={fieldName} />
      ))}
      <Button variant="contained" sx={{ mt: 2 }}>
        Send
      </Button>
    </Box>
  );
};

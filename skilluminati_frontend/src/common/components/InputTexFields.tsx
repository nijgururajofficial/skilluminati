import { Box, TextField, Typography } from "@mui/material";

interface InputTextFieldsProps {
  name: string;
}

export const InputTextFields = ({ name }: InputTextFieldsProps) => {
  return (
    <Box gridArea={"contact-form"}>
      <Typography height={"2vh"}>{name}</Typography>
      <Box height={"3vh"}></Box>
      <TextField></TextField>
      <Box height={"3vh"}></Box>
    </Box>
  );
};

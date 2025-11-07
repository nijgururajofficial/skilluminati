import { Box, Button } from "@mui/material";

export const HomeNavbar = () => {
  return (
    <Box
      display="flex"
      justifyContent="flex-end" // 👈 pushes button to right
      width="100%"
      mt={2}
    >
      <Button variant="contained" sx={{ width: "20vw" }}>
        Analyze New Job
      </Button>
    </Box>
  );
};

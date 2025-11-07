import { Chip } from "@mui/material";

export const TopSkillsFound = () => {
  const labelNames = ["SQL", "Python"];
  return (
    <>
      {labelNames.map((label) => (
        <Chip
          key={label}
          label={label}
          size="small"
          sx={{
            width: "50%", // expand across the container
            borderRadius: "9999px", // pill shape
            border: "1px solid #6BA3C8",
            color: "#9BD2FF",
            justifyContent: "center", // center the label text
          }}
        />
      ))}
    </>
  );
};

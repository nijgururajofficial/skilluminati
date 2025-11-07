import { Box, Typography } from "@mui/material";

type Props = {
  count: number;
  role?: string;
};

export const TopSkillsTitle = ({ count, role }: Props) => {
  return (
    <Box display="flex" alignItems="center" gap={2} mt={3}>
      <Typography variant="h6" fontWeight={600}>
        Top skills & tools
      </Typography>
      <Typography variant="body2" sx={{ opacity: 0.6 }}>
        Top skills highlighted: {count}
        {role ? ` · Role focus: ${role}` : null}
      </Typography>
    </Box>
  );
};

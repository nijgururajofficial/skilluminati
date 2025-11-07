import { Box, Chip, Typography } from "@mui/material";

type JDCardProps = {
  skill: {
    name: string;
    priority: string;
    importanceScore: number;
    rationale: string;
  };
};

export const JDCard = ({ skill }: JDCardProps) => {
  return (
    <Box
      sx={{
        background: "rgba(30,41,59,0.9)",
        border: "1px solid rgba(148,163,184,0.16)",
        borderRadius: 3,
        p: 2.5,
        height: "100%",
      }}
    >
      <Box
        display="flex"
        justifyContent="space-between"
        alignItems="flex-start"
        gap={1}
      >
        <Typography fontWeight={600}>{skill.name}</Typography>
        <Chip
          label={skill.priority}
          size="small"
          sx={{
            bgcolor: "rgba(96,165,250,0.2)",
            color: "rgba(191,219,254,0.95)",
          }}
        />
      </Box>

      <Typography
        variant="caption"
        sx={{ opacity: 0.7, display: "block", mt: 1 }}
      >
        Importance score: {skill.importanceScore}
      </Typography>

      <Typography variant="body2" sx={{ mt: 1 }}>
        {skill.rationale}
      </Typography>

      <Typography
        variant="body2"
        sx={{
          mt: 1.5,
          fontSize: 12,
          color: "rgba(96,165,250,0.9)",
          cursor: "pointer",
        }}
      >
        See skill context →
      </Typography>
    </Box>
  );
};

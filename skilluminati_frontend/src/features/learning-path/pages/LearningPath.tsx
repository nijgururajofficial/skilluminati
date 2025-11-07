import { Alert, Box, Button, Paper, Skeleton, Stack, Typography } from "@mui/material";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import RefreshIcon from "@mui/icons-material/Refresh";
import { useNavigate, useSearchParams } from "react-router-dom";
import { useLearningPath } from "../viewmodels/useLearningPath";

export const LearningPath = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const jdId = searchParams.get("jdId");
  const { roadmap, isLoading, error, refetch } = useLearningPath(jdId);

  const handleBackToAnalyzer = () => {
    navigate("/job-analyzer");
  };

  const handleRefresh = async () => {
    await refetch();
  };

  const showEmptyState = !jdId && !isLoading;

  return (
    <Box
      sx={{
        minHeight: "100vh",
        bgcolor: "#0b1120",
        color: "#e2e8f0",
        py: { xs: 4, md: 6 },
      }}
    >
      <Box sx={{ maxWidth: 960, mx: "auto", px: { xs: 2, md: 0 } }}>
        <Stack spacing={4}>
          <Stack direction={{ xs: "column", md: "row" }} justifyContent="space-between" gap={2}>
            <Box>
              <Typography variant="overline" sx={{ color: "rgba(148,163,184,0.7)" }}>
                Learning roadmap
              </Typography>
              <Typography variant="h4" fontWeight={700} sx={{ mt: 0.5 }}>
                {roadmap?.role ?? "Upskilling plan"}
              </Typography>
              <Typography variant="body2" sx={{ color: "rgba(148,163,184,0.75)", mt: 1 }}>
                A short, focused sequence of weekly milestones based on your JD analysis.
              </Typography>
            </Box>

            <Stack
              direction={{ xs: "column", sm: "row" }}
              spacing={2}
              alignItems={{ xs: "stretch", sm: "center" }}
            >
              <Button variant="text" startIcon={<ArrowBackIcon />} onClick={handleBackToAnalyzer}>
                Back to analyzer
              </Button>
              <Button
                variant="contained"
                color="primary"
                startIcon={<RefreshIcon />}
                onClick={handleRefresh}
                disabled={isLoading || !jdId}
              >
                Refresh
              </Button>
            </Stack>
          </Stack>

          {showEmptyState ? (
            <Paper
              elevation={0}
              sx={{
                p: { xs: 4, md: 5 },
                borderRadius: 2,
                bgcolor: "rgba(15,23,42,0.8)",
                border: "1px solid rgba(148,163,184,0.12)",
                textAlign: "center",
              }}
            >
              <Typography variant="h6" fontWeight={600} gutterBottom>
                No roadmap yet
              </Typography>
              <Typography variant="body2" sx={{ color: "rgba(148,163,184,0.75)" }}>
                Run the job analyzer and generate a plan to see weekly guidance here.
              </Typography>
            </Paper>
          ) : null}

          {error && (
            <Alert severity="error" variant="outlined">
              {error}
            </Alert>
          )}

          {isLoading ? (
            <Stack spacing={3}>
              {Array.from({ length: 3 }).map((_, idx) => (
                <Skeleton
                  key={`roadmap-skeleton-${idx}`}
                  variant="rectangular"
                  height={160}
                  sx={{ bgcolor: "rgba(30,41,59,0.85)", borderRadius: 2 }}
                />
              ))}
            </Stack>
          ) : roadmap ? (
            <Stack spacing={3}>
              <Paper
                elevation={0}
                sx={{
                  p: { xs: 3, md: 4 },
                  borderRadius: 2,
                  bgcolor: "rgba(15,23,42,0.8)",
                  border: "1px solid rgba(148,163,184,0.12)",
                }}
              >
                <Stack spacing={1.5}>
                  <Typography variant="subtitle2" sx={{ color: "rgba(148,163,184,0.75)" }}>
                    Overview
                  </Typography>
                  <Typography variant="h6" fontWeight={600}>
                    {roadmap.role}
                  </Typography>
                  <Typography variant="body2" sx={{ color: "rgba(148,163,184,0.75)" }}>
                    {roadmap.estimated_weeks} week plan · {roadmap.total_skills} skills in focus
                  </Typography>
                  {roadmap.jd_id ? (
                    <Typography variant="caption" sx={{ color: "rgba(148,163,184,0.6)" }}>
                      Reference ID: {roadmap.jd_id}
                    </Typography>
                  ) : null}
                </Stack>
              </Paper>

              {roadmap.phases.map((phase) => (
                <Paper
                  key={`phase-${phase.week}`}
                  elevation={0}
                  sx={{
                    p: { xs: 3, md: 4 },
                    borderRadius: 2,
                    bgcolor: "rgba(15,23,42,0.75)",
                    border: "1px solid rgba(148,163,184,0.12)",
                  }}
                >
                  <Stack spacing={2}>
                    <Stack direction={{ xs: "column", sm: "row" }} justifyContent="space-between" gap={2}>
                      <Typography variant="h6" fontWeight={600}>
                        Week {phase.week}
                      </Typography>
                      <Typography variant="body2" sx={{ color: "rgba(148,163,184,0.75)" }}>
                        {phase.description}
                      </Typography>
                    </Stack>

                    {phase.skills.length ? (
                      <Stack direction="row" spacing={1} flexWrap="wrap">
                        {phase.skills.map((skill) => (
                          <Box
                            key={`${phase.week}-${skill}`}
                            sx={{
                              px: 1,
                              py: 0.5,
                              borderRadius: 1,
                              bgcolor: "rgba(56,189,248,0.16)",
                              color: "rgba(165,243,252,0.95)",
                              fontSize: 12,
                              fontWeight: 500,
                            }}
                          >
                            {skill}
                          </Box>
                        ))}
                      </Stack>
                    ) : null}

                    {phase.resources.length ? (
                      <Stack spacing={1}>
                        <Typography variant="subtitle2" sx={{ color: "rgba(148,163,184,0.75)" }}>
                          Resources
                        </Typography>
                        {phase.resources.map((resource) => (
                          <Typography
                            key={`${phase.week}-${resource.title}`}
                            variant="body2"
                            sx={{ color: "rgba(226,232,240,0.85)" }}
                          >
                            • {resource.title} — {resource.description}
                          </Typography>
                        ))}
                      </Stack>
                    ) : null}

                    {phase.projects.length ? (
                      <Stack spacing={1}>
                        <Typography variant="subtitle2" sx={{ color: "rgba(148,163,184,0.75)" }}>
                          Practice
                        </Typography>
                        {phase.projects.map((project) => (
                          <Typography
                            key={`${phase.week}-project-${project.title}`}
                            variant="body2"
                            sx={{ color: "rgba(226,232,240,0.85)" }}
                          >
                            • {project.title}
                            {project.difficulty ? ` (${project.difficulty})` : ""} — {project.description}
                          </Typography>
                        ))}
                      </Stack>
                    ) : null}
                  </Stack>
                </Paper>
              ))}
            </Stack>
          ) : null}
        </Stack>
      </Box>
    </Box>
  );
};

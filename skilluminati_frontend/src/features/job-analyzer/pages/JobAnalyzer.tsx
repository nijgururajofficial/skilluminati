// src/pages/JobAnalyzer.tsx

import {
  Alert,
  Box,
  Button,
  Chip,
  Fade,
  LinearProgress,
  Paper,
  Skeleton,
  Stack,
  Typography,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import { JobAnalyzerTitle } from "../components/JobAnalyzerTitle";
import { JobAnalyzerInputJDField } from "../components/JobAnalyzerInputJDField";
import { ResumeUpload } from "../components/ResumeUpload";
import { TextAndAnalyzeButton } from "../components/TextAndAnalyzeButton";
import { useJobAnalyzer } from "../viewmodels/useJobAnalyzer";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import KeyboardArrowUpRoundedIcon from "@mui/icons-material/KeyboardArrowUpRounded";

export const JobAnalyzer = () => {
  const {
    jdText,
    setJdText,
    analysis,
    isLoading,
    error,
    handleAnalyze,
    resumeFile,
    setResumeFile,
  } = useJobAnalyzer();
  const navigate = useNavigate();

  const skillCount = analysis?.skills?.length ?? 0;
  const insightsCount = analysis?.companyInsights?.length ?? 0;
  const hasAnalysis = skillCount > 0 || insightsCount > 0;

  const handleGenerateRoadmap = () => {
    if (!analysis.jdId) return;
    navigate(`/learning-path?jdId=${encodeURIComponent(analysis.jdId)}`);
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        background:
          "radial-gradient(circle at 20% 20%, rgba(59,130,246,0.28), transparent 55%), radial-gradient(circle at 80% 0%, rgba(236,72,153,0.22), transparent 50%), #0b1120",
        color: "#e2e8f0",
        py: { xs: 4, md: 6 },
      }}
    >
      <Box sx={{ maxWidth: 960, mx: "auto", px: { xs: 2, md: 0 } }}>
        <Stack spacing={4}>
          <JobAnalyzerTitle />

          <Box
            sx={{
              display: "flex",
              flexDirection: { xs: "column", md: "row" },
              gap: { xs: 3, md: 4 },
            }}
          >
            <Paper
              elevation={0}
              sx={{
                flexBasis: { md: "45%" },
                flexGrow: { md: 0 },
                p: { xs: 3, md: 4 },
                bgcolor: "rgba(15,23,42,0.82)",
                borderRadius: 2,
                border: "1px solid rgba(148,163,184,0.16)",
                backdropFilter: "blur(12px)",
              }}
            >
              <Stack spacing={3}>
                <JobAnalyzerInputJDField value={jdText} onChange={setJdText} />

                <ResumeUpload file={resumeFile} onSelect={setResumeFile} disabled={isLoading} />

                <TextAndAnalyzeButton
                  onAnalyze={handleAnalyze}
                  disabled={!jdText.trim()}
                  isLoading={isLoading}
                />

                {error && (
                  <Alert severity="error" variant="outlined">
                    {error}
                  </Alert>
                )}
              </Stack>
            </Paper>

            <Paper
              elevation={0}
              sx={{
                flexGrow: 1,
                p: { xs: 3, md: 4 },
                bgcolor: "rgba(15,23,42,0.72)",
                borderRadius: 2,
                border: "1px solid rgba(148,163,184,0.16)",
                backdropFilter: "blur(12px)",
                minHeight: { md: 480 },
              }}
            >
              <Stack spacing={3} sx={{ height: "100%" }}>
                <Box>
                  <Typography variant="h6" fontWeight={600}>
                    {hasAnalysis ? "Role snapshot" : "Your results will appear here"}
                  </Typography>
                  {!hasAnalysis ? (
                    <Typography variant="body2" sx={{ color: "rgba(148,163,184,0.7)", mt: 0.5 }}>
                      Paste a JD and your results will drop in here.
                    </Typography>
                  ) : null}
                </Box>

                {isLoading ? (
                  <Stack spacing={2}>
                    {Array.from({ length: 4 }).map((_, idx) => (
                      <Skeleton
                        key={idx}
                        variant="rectangular"
                        height={72}
                        sx={{ bgcolor: "rgba(30,41,59,0.8)", borderRadius: 1.5 }}
                      />
                    ))}
                  </Stack>
                ) : hasAnalysis ? (
                  <Fade in>
                    <Stack spacing={3} sx={{ flexGrow: 1 }}>
                      <Stack spacing={1.5}>
                        <Stack direction={{ xs: "column", sm: "row" }} justifyContent="space-between" spacing={1.5}>
                          <Box>
                            <Typography variant="subtitle2" sx={{ color: "rgba(148,163,184,0.75)" }}>
                              Role focus
                            </Typography>
                            <Typography variant="h5" fontWeight={700}>
                              {analysis.role || "Role not specified"}
                            </Typography>
                          </Box>
                          {analysis.jdId ? (
                            <Chip
                              label={`Reference · ${analysis.jdId}`}
                              size="small"
                              sx={{
                                alignSelf: "flex-start",
                                bgcolor: "rgba(96,165,250,0.22)",
                                color: "rgba(191,219,254,0.95)",
                                borderRadius: 1,
                              }}
                            />
                          ) : null}
                        </Stack>

                        <Chip
                          label={`${skillCount} core skills`}
                          sx={{
                            bgcolor: "rgba(45,212,191,0.18)",
                            color: "rgba(204,251,241,0.95)",
                            borderRadius: 1,
                            fontWeight: 600,
                            width: "fit-content",
                          }}
                        />
                      </Stack>

                      {skillCount > 0 ? (
                        <Stack spacing={1.5}>
                          <Typography variant="subtitle2" sx={{ color: "rgba(148,163,184,0.75)" }}>
                            Priority skills
                          </Typography>
                          <Stack spacing={1.25}>
                            {analysis.skills?.map((skill) => {
                              const baseImportance = Number.isFinite(skill.importanceScore)
                                ? skill.importanceScore
                                : 0;
                              const importancePercent = Math.min(Math.max(baseImportance * 10, 0), 100);
                              return (
                                <Box
                                  key={skill.name}
                                  sx={{
                                    display: "flex",
                                    flexDirection: "column",
                                    gap: 1,
                                    p: 1.5,
                                    borderRadius: 2,
                                    bgcolor: "rgba(30,41,59,0.65)",
                                    border: "1px solid rgba(148,163,184,0.14)",
                                    boxShadow: "inset 0 1px 0 rgba(148,163,184,0.06)",
                                  }}
                                >
                                  <Stack direction={{ xs: "column", sm: "row" }} justifyContent="space-between" spacing={1}>
                                    <Stack spacing={0.5}>
                                      <Typography variant="subtitle1" fontWeight={600}>
                                        {skill.name}
                                      </Typography>
                                      {skill.rationale ? (
                                        <Typography variant="body2" sx={{ color: "rgba(148,163,184,0.78)" }}>
                                          {skill.rationale}
                                        </Typography>
                                      ) : null}
                                    </Stack>
                                    <Chip
                                      label={skill.priority}
                                      size="small"
                                      sx={{
                                        alignSelf: "flex-start",
                                        bgcolor: "rgba(59,130,246,0.18)",
                                        color: "rgba(191,219,254,0.95)",
                                        textTransform: "capitalize",
                                        borderRadius: 1,
                                      }}
                                    />
                                  </Stack>
                                  <Stack spacing={0.5}>
                                    <Stack direction="row" justifyContent="space-between" alignItems="center">
                                      <Typography variant="caption" sx={{ color: "rgba(148,163,184,0.7)" }}>
                                        Score
                                      </Typography>
                                      <Typography variant="caption" sx={{ color: "rgba(226,232,240,0.85)", fontWeight: 600 }}>
                                        {baseImportance}/10
                                      </Typography>
                                    </Stack>
                                    <LinearProgress
                                      variant="determinate"
                                      value={importancePercent}
                                      sx={{
                                        height: 6,
                                        borderRadius: 999,
                                        bgcolor: "rgba(148,163,184,0.2)",
                                        "& .MuiLinearProgress-bar": {
                                          borderRadius: 999,
                                          background: "linear-gradient(135deg, #38bdf8, #6366f1)",
                                        },
                                      }}
                                    />
                                  </Stack>
                                </Box>
                              );
                            })}
                          </Stack>
                        </Stack>
                      ) : null}

                      {insightsCount > 0 && analysis.companyInsights?.length ? (
                        <Stack spacing={1.25}>
                          {analysis.companyInsights.map((insight) => (
                            <Box
                              key={`${insight.title}-${insight.url}`}
                              sx={{
                                p: 1.25,
                                borderRadius: 2,
                                bgcolor: "rgba(30,41,59,0.65)",
                                border: "1px solid rgba(148,163,184,0.14)",
                              }}
                            >
                              <Typography variant="subtitle1" fontWeight={600}>
                                {insight.title}
                              </Typography>
                              {insight.content ? (
                                <Typography variant="body2" sx={{ color: "rgba(148,163,184,0.78)", mt: 0.5 }}>
                                  {insight.content}
                                </Typography>
                              ) : null}
                            </Box>
                          ))}
                        </Stack>
                      ) : null}

                      <Stack direction={{ xs: "column", sm: "row" }} spacing={2} mt="auto">
                        <Button
                          variant="contained"
                          color="primary"
                          disabled={!analysis.jdId || isLoading}
                          onClick={handleGenerateRoadmap}
                          sx={{ minWidth: 220 }}
                          endIcon={<ArrowForwardIcon fontSize="small" />}
                        >
                          View roadmap
                        </Button>
                        <Button
                          variant="text"
                          color="inherit"
                          disabled={isLoading}
                          onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
                          endIcon={<KeyboardArrowUpRoundedIcon fontSize="small" />}
                        >
                          Back to top
                        </Button>
                      </Stack>
                    </Stack>
                  </Fade>
                ) : (
                  <Typography variant="body2" sx={{ color: "rgba(148,163,184,0.75)" }}>
                    Once you run the analyzer, we’ll list the top skills and company context here.
                  </Typography>
                )}
              </Stack>
            </Paper>
          </Box>
        </Stack>
      </Box>
    </Box>
  );
};

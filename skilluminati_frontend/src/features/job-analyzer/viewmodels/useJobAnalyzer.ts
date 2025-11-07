// src/viewmodels/useJobAnalyzer.ts

import { useState } from "react";
import { analyzeJobDescription } from "../services/jobAnalyzerService";
import type { JobAnalysis } from "../types/jobAnalyzer";

const EMPTY_ANALYSIS: JobAnalysis = {
  role: "",
  jdId: "",
  skills: [],
  companyInsights: [],
};

export function useJobAnalyzer() {
  const [jdText, setJdText] = useState("");
  const [analysis, setAnalysis] = useState<JobAnalysis>(EMPTY_ANALYSIS);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [resumeFile, setResumeFile] = useState<File | null>(null);

  const handleAnalyze = async () => {
    if (!jdText.trim()) return;
    setIsLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem("access_token") ?? undefined;
      const result = await analyzeJobDescription(jdText, {
        token,
        resumeFile: resumeFile ?? undefined,
      });
      setAnalysis(result);
    } catch (err: any) {
      setError(err.message ?? "Something went wrong");
      setAnalysis(EMPTY_ANALYSIS);
    } finally {
      setIsLoading(false);
    }
  };

  return {
    jdText,
    setJdText,
    analysis,
    isLoading,
    error,
    handleAnalyze,
    resumeFile,
    setResumeFile,
  };
}

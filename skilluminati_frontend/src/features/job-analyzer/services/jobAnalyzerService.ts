// src/services/jobAnalyzerService.ts
import { API_BASE_URL } from "../../../config/api";
import type { JobAnalysis } from "../types/jobAnalyzer";

type AnalyzeJobDescriptionOptions = {
  token?: string;
  resumeFile?: File;
};

type AnalyzeJobDescriptionResponse = {
  role?: string;
  skills?: Array<{
    name: string;
    priority: string;
    importance_score: number;
    why: string;
  }>;
  jd_id?: string;
  company_insights?: Array<{
    title: string;
    url: string;
    content: string;
    skills_used: string[];
    relevance: string;
  }>;
};

export async function analyzeJobDescription(
  jdText: string,
  options: AnalyzeJobDescriptionOptions = {}
): Promise<JobAnalysis> {
  const { token, resumeFile } = options;

  const formData = new FormData();
  formData.append("jd_text", jdText);
  if (resumeFile) {
    formData.append("resume", resumeFile);
  }

  const response = await fetch(`${API_BASE_URL}/analyze-jd`, {
    method: "POST",
    headers: token ? { Authorization: `Bearer ${token}` } : undefined,
    body: formData,
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => null);
    const errorMessage =
      (errorBody && (errorBody.detail ?? errorBody.message)) ||
      "Failed to analyze job description";
    throw new Error(errorMessage);
  }

  const raw = (await response.json()) as AnalyzeJobDescriptionResponse;

  return {
    role: raw.role ?? "",
    jdId: raw.jd_id ?? "",
    skills:
      raw.skills?.map((skill) => ({
        name: skill.name,
        priority: skill.priority,
        importanceScore: skill.importance_score,
        rationale: skill.why,
      })) ?? [],
    companyInsights:
      raw.company_insights?.map((insight) => ({
        title: insight.title,
        url: insight.url,
        content: insight.content,
        skillsUsed: insight.skills_used,
        relevance: insight.relevance,
      })) ?? [],
  };
}

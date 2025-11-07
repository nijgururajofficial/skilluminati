// src/types/jobAnalyzer.ts

export interface AnalyzedSkill {
  name: string;
  priority: string;
  importanceScore: number;
  rationale: string;
}

export interface CompanyInsight {
  title: string;
  url: string;
  content: string;
  skillsUsed: string[];
  relevance: string;
}

export interface JobAnalysis {
  role: string;
  jdId: string;
  skills: AnalyzedSkill[];
  companyInsights: CompanyInsight[];
}

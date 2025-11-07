export interface RoadmapPhaseResource {
  type: string;
  title: string;
  url: string;
  description: string;
}

export interface RoadmapPhaseProject {
  title: string;
  description: string;
  difficulty: string;
}

export interface RoadmapPhase {
  week: number;
  skills: string[];
  resources: RoadmapPhaseResource[];
  projects: RoadmapPhaseProject[];
  description: string;
}

export interface RoadmapResponse {
  roadmap_id: string;
  jd_id: string;
  role: string;
  phases: RoadmapPhase[];
  total_skills: number;
  estimated_weeks: number;
}


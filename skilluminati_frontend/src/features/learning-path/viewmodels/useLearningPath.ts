import { useEffect, useState } from "react";
import { generateRoadmap } from "../services/roadmapService";
import type { RoadmapResponse } from "../types/roadmap";

interface UseLearningPathResult {
  roadmap: RoadmapResponse | null;
  isLoading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export const useLearningPath = (jdId: string | null): UseLearningPathResult => {
  const [roadmap, setRoadmap] = useState<RoadmapResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchRoadmap = async () => {
    if (!jdId) {
      setRoadmap(null);
      return;
    }

    setIsLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem("access_token") ?? undefined;
      const data = await generateRoadmap(jdId, { token });
      setRoadmap(data);
    } catch (err: any) {
      setError(err.message ?? "Failed to load roadmap");
      setRoadmap(null);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    void fetchRoadmap();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [jdId]);

  return {
    roadmap,
    isLoading,
    error,
    refetch: fetchRoadmap,
  };
};


import { API_BASE_URL } from "../../../config/api";
import type { RoadmapResponse } from "../types/roadmap";

type GenerateRoadmapOptions = {
  token?: string;
};

export async function generateRoadmap(
  jdId: string,
  options: GenerateRoadmapOptions = {}
): Promise<RoadmapResponse> {
  const { token } = options;

  const response = await fetch(`${API_BASE_URL}/generate-roadmap`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify({ jd_id: jdId }),
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => null);
    const errorMessage =
      (errorBody && (errorBody.detail ?? errorBody.message)) ||
      "Unable to generate roadmap";
    throw new Error(errorMessage);
  }

  return (await response.json()) as RoadmapResponse;
}


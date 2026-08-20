import type { AnalysisResult, GameSnapshot } from "./types";

const API = "http://127.0.0.1:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API}${path}`, options);
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail ?? `Request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export const api = {
  health: () => request<{ status: string; version: string }>("/health"),
  liveStatus: () => request<{ available: boolean }>("/v1/live/status"),
  analyzeLive: () => request<AnalysisResult>("/v1/live/analyze", { method: "POST" }),
  analyzeDemo: () => request<AnalysisResult>("/v1/demo/analyze", { method: "POST" }),
  demoSnapshot: () => request<GameSnapshot>("/v1/demo/snapshot"),
  liveSnapshot: () => request<GameSnapshot>("/v1/live/snapshot"),
};

export type Recommendation = {
  id: string;
  category: string;
  title: string;
  priority: number;
  confidence: number;
  summary: string;
  reasons: string[];
  evidence: Record<string, string | number | null>;
  counterfactual: string;
};

export type Features = {
  cs_per_minute: number;
  kda: number;
  health_ratio: number;
  level_delta: number;
  team_kill_delta: number;
  current_gold: number | null;
  recent_deaths: number;
  recent_kills: number;
  survival_risk: number;
  tempo_score: number;
  economy_pressure: number;
  data_completeness: number;
};

export type AnalysisResult = {
  engine_version: string;
  generated_at: string;
  active_player_id: string;
  features: Features;
  recommendations: Recommendation[];
  state_fingerprint: string;
};

export type GameSnapshot = {
  game_time: number;
  game_mode: string;
  map_name: string;
  active_player_id: string;
  players: Array<{
    riot_id: string;
    champion_name: string;
    team: string;
    level: number;
    is_active: boolean;
    score: { kills: number; deaths: number; assists: number; creep_score: number; ward_score: number; kda: number };
  }>;
  events: Array<{ event_id: number | null; event_name: string; event_time: number; actor: string | null; victim: string | null }>;
};

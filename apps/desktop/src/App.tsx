import { useCallback, useEffect, useMemo, useState } from "react";
import { api } from "./api";
import type { AnalysisResult, GameSnapshot, Recommendation } from "./types";

type Mode = "demo" | "live";

function pct(value: number) {
  return `${Math.round(value * 100)}%`;
}

function clock(seconds: number) {
  const minutes = Math.floor(seconds / 60);
  return `${minutes}:${String(Math.floor(seconds % 60)).padStart(2, "0")}`;
}

function Metric({ label, value, detail }: { label: string; value: string; detail: string }) {
  return (
    <article className="metric-card">
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{detail}</small>
    </article>
  );
}

function RecommendationCard({ recommendation, index }: { recommendation: Recommendation; index: number }) {
  return (
    <article className="recommendation-card">
      <div className="recommendation-rank">0{index + 1}</div>
      <div className="recommendation-body">
        <div className="recommendation-meta">
          <span className={`category category-${recommendation.category}`}>{recommendation.category}</span>
          <span>{pct(recommendation.confidence)} confidence</span>
          <span>{recommendation.priority} priority</span>
        </div>
        <h3>{recommendation.title}</h3>
        <p>{recommendation.summary}</p>
        <ul>
          {recommendation.reasons.slice(0, 3).map((reason) => <li key={reason}>{reason}</li>)}
        </ul>
        <details>
          <summary>Decision trace / counterfactual</summary>
          <p>{recommendation.counterfactual}</p>
        </details>
      </div>
    </article>
  );
}

export default function App() {
  const [mode, setMode] = useState<Mode>("demo");
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [snapshot, setSnapshot] = useState<GameSnapshot | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [backendOnline, setBackendOnline] = useState(false);

  const refresh = useCallback(async () => {
    setBusy(true);
    setError(null);
    try {
      const [nextAnalysis, nextSnapshot] = mode === "live"
        ? await Promise.all([api.analyzeLive(), api.liveSnapshot()])
        : await Promise.all([api.analyzeDemo(), api.demoSnapshot()]);
      setAnalysis(nextAnalysis);
      setSnapshot(nextSnapshot);
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "Unknown error");
    } finally {
      setBusy(false);
    }
  }, [mode]);

  useEffect(() => {
    api.health().then(() => setBackendOnline(true)).catch(() => setBackendOnline(false));
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  useEffect(() => {
    if (mode !== "live") return;
    const id = window.setInterval(refresh, 5000);
    return () => window.clearInterval(id);
  }, [mode, refresh]);

  const activeChampion = useMemo(
    () => snapshot?.players.find((player) => player.is_active || player.riot_id === snapshot.active_player_id)?.champion_name ?? "—",
    [snapshot],
  );

  return (
    <main className="shell">
      <header className="topbar">
        <div className="brand">
          <div className="brand-mark">RP</div>
          <div>
            <strong>RiftPilot</strong>
            <span>Explainable match intelligence</span>
          </div>
        </div>
        <div className="status-row">
          <span className={`status-dot ${backendOnline ? "online" : "offline"}`} />
          <span>{backendOnline ? "analytics online" : "analytics offline"}</span>
          <div className="mode-switch">
            <button className={mode === "demo" ? "active" : ""} onClick={() => setMode("demo")}>Demo</button>
            <button className={mode === "live" ? "active" : ""} onClick={() => setMode("live")}>Live</button>
          </div>
          <button className="refresh-button" disabled={busy} onClick={refresh}>{busy ? "Analyzing…" : "Refresh"}</button>
        </div>
      </header>

      <section className="hero-panel">
        <div>
          <span className="eyebrow">Current decision window</span>
          <h1>{analysis?.recommendations[0]?.title ?? "Waiting for match context"}</h1>
          <p>{analysis?.recommendations[0]?.summary ?? "Start the local analytics service to begin."}</p>
        </div>
        <div className="confidence-orb">
          <span>confidence</span>
          <strong>{analysis ? pct(analysis.recommendations[0]?.confidence ?? 0) : "—"}</strong>
          <small>{analysis?.state_fingerprint ?? "no state"}</small>
        </div>
      </section>

      {error && <div className="error-banner"><strong>Live context unavailable.</strong> {error} Switch to Demo to inspect the full product flow.</div>}

      <section className="context-strip">
        <div><span>Champion</span><strong>{activeChampion}</strong></div>
        <div><span>Game time</span><strong>{snapshot ? clock(snapshot.game_time) : "—"}</strong></div>
        <div><span>Mode</span><strong>{snapshot?.game_mode ?? "—"}</strong></div>
        <div><span>Source</span><strong>{mode === "live" ? "Live Client" : "Replay fixture"}</strong></div>
      </section>

      <section className="metrics-grid">
        <Metric label="Survival risk" value={analysis ? pct(analysis.features.survival_risk) : "—"} detail="health + recent deaths + level pressure" />
        <Metric label="Tempo score" value={analysis ? pct(analysis.features.tempo_score) : "—"} detail="momentum + health + recent combat" />
        <Metric label="Economy pressure" value={analysis ? pct(analysis.features.economy_pressure) : "—"} detail="held gold + income pace" />
        <Metric label="Data completeness" value={analysis ? pct(analysis.features.data_completeness) : "—"} detail="confidence is reduced when context is missing" />
      </section>

      <section className="workspace-grid">
        <div className="panel recommendations-panel">
          <div className="panel-heading">
            <div><span className="eyebrow">Decision stack</span><h2>What matters now</h2></div>
            <span>{analysis?.engine_version ?? "engine offline"}</span>
          </div>
          <div className="recommendation-list">
            {analysis?.recommendations.map((recommendation, index) => (
              <RecommendationCard key={recommendation.id} recommendation={recommendation} index={index} />
            ))}
          </div>
        </div>

        <aside className="right-column">
          <section className="panel">
            <div className="panel-heading"><div><span className="eyebrow">Scoreboard context</span><h2>Players</h2></div></div>
            <div className="scoreboard">
              {snapshot?.players.map((player) => (
                <div className={`player-row ${player.is_active ? "active-player" : ""}`} key={player.riot_id}>
                  <div><strong>{player.champion_name}</strong><span>{player.riot_id}</span></div>
                  <span>Lv {player.level}</span>
                  <span>{player.score.kills}/{player.score.deaths}/{player.score.assists}</span>
                  <span>{player.score.creep_score} CS</span>
                </div>
              ))}
            </div>
          </section>

          <section className="panel">
            <div className="panel-heading"><div><span className="eyebrow">Last events</span><h2>Combat trace</h2></div></div>
            <div className="timeline">
              {snapshot?.events.slice(-5).reverse().map((event) => (
                <div key={`${event.event_id}-${event.event_time}`}>
                  <span>{clock(event.event_time)}</span>
                  <p><strong>{event.event_name}</strong><br />{event.actor ?? "—"} → {event.victim ?? "—"}</p>
                </div>
              ))}
            </div>
          </section>
        </aside>
      </section>

      <footer>
        Local-first · Read-only live data · No memory reading · No gameplay automation · No hidden-information inference
      </footer>
    </main>
  );
}

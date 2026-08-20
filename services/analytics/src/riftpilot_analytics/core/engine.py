"""Explainable, uncertainty-aware decision engine."""

from __future__ import annotations

import hashlib
import json

from riftpilot_analytics.core.features import extract_features
from riftpilot_analytics.domain.models import (
    AnalysisResult,
    GameSnapshot,
    Recommendation,
    RecommendationCategory,
)

ENGINE_VERSION = "decision-engine/0.4"


def _confidence(base: float, completeness: float) -> float:
    return round(max(0.0, min(1.0, base * (0.65 + completeness * 0.35))), 3)


def _fingerprint(snapshot: GameSnapshot) -> str:
    compact = {
        "time_bucket": int(snapshot.game_time // 5),
        "active": snapshot.active_player_id,
        "players": [
            [p.riot_id, p.level, p.score.kills, p.score.deaths, p.score.assists, p.score.creep_score]
            for p in snapshot.players
        ],
        "events": len(snapshot.events),
    }
    return hashlib.sha256(json.dumps(compact, sort_keys=True).encode()).hexdigest()[:16]


class DecisionEngine:
    """Produces deterministic advice with explicit evidence instead of opaque scores."""

    def analyze(self, snapshot: GameSnapshot) -> AnalysisResult:
        features = extract_features(snapshot)
        recommendations: list[Recommendation] = []

        if features.health_ratio < 0.42 or features.survival_risk >= 0.62:
            recommendations.append(
                Recommendation(
                    id="stabilize-now",
                    category=RecommendationCategory.SURVIVAL,
                    title="Stabilize before taking the next high-variance fight",
                    priority=95,
                    confidence=_confidence(0.92, features.data_completeness),
                    summary="Your current state has elevated execution risk; protect tempo first.",
                    reasons=[
                        f"Health is {features.health_ratio:.0%}.",
                        f"Estimated contextual survival risk is {features.survival_risk:.0%}.",
                        f"Recent deaths in the last three minutes: {features.recent_deaths}.",
                    ],
                    evidence={"health_ratio": features.health_ratio, "survival_risk": features.survival_risk, "recent_deaths": features.recent_deaths},
                    counterfactual="If health and recent-death pressure recover, the engine will shift weight toward tempo and map pressure.",
                )
            )

        if features.current_gold is not None and features.current_gold >= 1150:
            priority = 88 if features.survival_risk >= 0.45 else 72
            recommendations.append(
                Recommendation(
                    id="convert-gold",
                    category=RecommendationCategory.ECONOMY,
                    title="Convert held gold into an actual power spike",
                    priority=priority,
                    confidence=_confidence(0.9, features.data_completeness),
                    summary="Unspent gold is latent power; a controlled reset can improve the next decision window.",
                    reasons=[f"You are holding approximately {features.current_gold:.0f} gold.", "Held gold does not contribute combat stats until spent.", "Reset value rises when survival risk is already elevated."],
                    evidence={"current_gold": features.current_gold, "survival_risk": features.survival_risk},
                    counterfactual="If held gold drops after a purchase, this recommendation disappears automatically.",
                )
            )

        if features.cs_per_minute < 5.5 and snapshot.game_time >= 480:
            recommendations.append(
                Recommendation(
                    id="recover-income",
                    category=RecommendationCategory.FARM,
                    title="Recover a safer income cycle before forcing tempo",
                    priority=70,
                    confidence=_confidence(0.78, features.data_completeness),
                    summary="Your current income pace is low enough that one clean farm cycle may outperform a forced play.",
                    reasons=[f"Current CS/min is {features.cs_per_minute:.2f}.", "The threshold is intentionally generic because role and lane are not inferred from hidden data."],
                    evidence={"cs_per_minute": features.cs_per_minute},
                    counterfactual="With a stronger CS/min pace or a high-tempo team state, the engine reduces this recommendation's weight.",
                )
            )

        if features.tempo_score >= 0.67 and features.survival_risk <= 0.42:
            recommendations.append(
                Recommendation(
                    id="use-tempo-window",
                    category=RecommendationCategory.TEMPO,
                    title="Use the current tempo window deliberately",
                    priority=82,
                    confidence=_confidence(0.82, features.data_completeness),
                    summary="The scoreboard, level context, and health state currently support proactive play.",
                    reasons=[f"Tempo score is {features.tempo_score:.0%}.", f"Team kill delta is {features.team_kill_delta:+d}.", f"Average enemy level delta is {features.level_delta:+.1f}."],
                    evidence={"tempo_score": features.tempo_score, "team_kill_delta": features.team_kill_delta, "level_delta": features.level_delta},
                    counterfactual="If health falls, recent deaths rise, or the level delta flips, the engine will prioritize stabilization instead.",
                )
            )

        if features.recent_deaths >= 2 or (features.kda < 1.0 and snapshot.game_time >= 600):
            recommendations.append(
                Recommendation(
                    id="lower-variance",
                    category=RecommendationCategory.VISION,
                    title="Lower variance: make the next play information-first",
                    priority=86,
                    confidence=_confidence(0.84, features.data_completeness),
                    summary="Repeated losses compound quickly; require better information before the next commitment.",
                    reasons=[f"KDA is {features.kda:.2f}.", f"Recent deaths: {features.recent_deaths}.", "Vision and teammate proximity are safer prerequisites than another blind contest."],
                    evidence={"kda": features.kda, "recent_deaths": features.recent_deaths},
                    counterfactual="A clean recovery window with no further deaths reduces the priority of this advice.",
                )
            )

        if not recommendations:
            recommendations.append(
                Recommendation(
                    id="hold-plan",
                    category=RecommendationCategory.TEMPO,
                    title="No emergency correction detected — keep the plan disciplined",
                    priority=55,
                    confidence=_confidence(0.72, features.data_completeness),
                    summary="The current snapshot has no dominant warning signal.",
                    reasons=[f"Survival risk is {features.survival_risk:.0%}.", f"Tempo score is {features.tempo_score:.0%}."],
                    evidence={"survival_risk": features.survival_risk, "tempo_score": features.tempo_score},
                    counterfactual="A major health, gold, scoreboard, or recent-combat change will trigger a more specific recommendation.",
                )
            )

        recommendations.sort(key=lambda rec: rec.priority, reverse=True)
        return AnalysisResult(engine_version=ENGINE_VERSION, active_player_id=snapshot.active_player_id, features=features, recommendations=recommendations[:5], state_fingerprint=_fingerprint(snapshot))

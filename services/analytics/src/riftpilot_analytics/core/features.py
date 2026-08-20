"""Feature engineering for deterministic, inspectable match context."""

from __future__ import annotations

from statistics import mean

from riftpilot_analytics.domain.models import ContextFeatures, DecisionSignal, GameSnapshot


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def _recent_combat(snapshot: GameSnapshot, active_id: str, window_seconds: float = 180.0) -> tuple[int, int]:
    cutoff = max(0.0, snapshot.game_time - window_seconds)
    recent_deaths = 0
    recent_kills = 0
    for event in snapshot.events:
        if event.event_time < cutoff or event.event_name.lower() != "championkill":
            continue
        if event.victim == active_id:
            recent_deaths += 1
        if event.actor == active_id:
            recent_kills += 1
    return recent_deaths, recent_kills


def extract_features(snapshot: GameSnapshot) -> ContextFeatures:
    player = snapshot.active_player()
    enemies = snapshot.enemies_of(player)
    allies = snapshot.allies_of(player)

    minutes = max(snapshot.game_time / 60.0, 1.0)
    cs_per_minute = round(player.score.creep_score / minutes, 2)
    enemy_avg_level = mean([enemy.level for enemy in enemies]) if enemies else float(player.level)
    level_delta = round(player.level - enemy_avg_level, 2)

    team_kills = player.score.kills + sum(ally.score.kills for ally in allies)
    enemy_kills = sum(enemy.score.kills for enemy in enemies)
    team_kill_delta = team_kills - enemy_kills
    recent_deaths, recent_kills = _recent_combat(snapshot, player.riot_id)

    health_ratio = player.stats.health_ratio if player.stats else 1.0
    death_pressure = _clamp(player.score.deaths / 8.0)
    recent_death_pressure = _clamp(recent_deaths / 2.0)
    level_pressure = _clamp(max(0.0, -level_delta) / 3.0)
    health_pressure = 1.0 - health_ratio
    survival_risk = _clamp(
        health_pressure * 0.38
        + death_pressure * 0.22
        + recent_death_pressure * 0.25
        + level_pressure * 0.15
    )

    momentum = _clamp(0.5 + (team_kill_delta / 20.0) + (level_delta / 8.0))
    health_tempo = _clamp((health_ratio - 0.35) / 0.65)
    recent_kill_bonus = _clamp(recent_kills / 2.0)
    tempo_score = _clamp(momentum * 0.5 + health_tempo * 0.35 + recent_kill_bonus * 0.15)

    gold = player.current_gold
    gold_pressure = _clamp((gold or 0.0) / 2200.0)
    farm_pressure = _clamp((6.5 - cs_per_minute) / 6.5)
    economy_pressure = _clamp(gold_pressure * 0.55 + farm_pressure * 0.45)

    completeness_fields = [
        player.stats is not None,
        player.current_gold is not None,
        len(snapshot.players) >= 2,
        snapshot.game_time > 0,
        bool(snapshot.events),
    ]
    data_completeness = round(sum(completeness_fields) / len(completeness_fields), 2)

    signals = [
        DecisionSignal(key="health_ratio", label="Current health", value=health_ratio, normalized=health_ratio, interpretation="Lower health increases immediate execution risk."),
        DecisionSignal(key="level_delta", label="Level delta vs enemies", value=level_delta, normalized=_clamp(0.5 + level_delta / 6.0), interpretation="Positive level delta usually creates a larger action window."),
        DecisionSignal(key="team_kill_delta", label="Team kill delta", value=float(team_kill_delta), normalized=_clamp(0.5 + team_kill_delta / 20.0), interpretation="A rough momentum signal, not a win-probability estimate."),
        DecisionSignal(key="cs_per_minute", label="CS per minute", value=cs_per_minute, normalized=_clamp(cs_per_minute / 9.0), interpretation="Income consistency signal; role and game context still matter."),
    ]

    return ContextFeatures(
        cs_per_minute=cs_per_minute,
        kda=player.score.kda,
        health_ratio=health_ratio,
        level_delta=level_delta,
        team_kill_delta=team_kill_delta,
        current_gold=gold,
        recent_deaths=recent_deaths,
        recent_kills=recent_kills,
        survival_risk=round(survival_risk, 4),
        tempo_score=round(tempo_score, 4),
        economy_pressure=round(economy_pressure, 4),
        data_completeness=data_completeness,
        signals=signals,
    )

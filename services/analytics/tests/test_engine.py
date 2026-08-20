from copy import deepcopy

from riftpilot_analytics.core.engine import DecisionEngine
from riftpilot_analytics.core.features import extract_features
from riftpilot_analytics.fixtures.demo import demo_snapshot


def test_demo_features_capture_risk_and_economy() -> None:
    features = extract_features(demo_snapshot())
    assert features.health_ratio < 0.4
    assert features.survival_risk > 0.5
    assert features.current_gold == 1480
    assert features.recent_deaths == 2
    assert features.data_completeness == 1.0


def test_engine_prioritizes_stabilization_and_gold_conversion() -> None:
    result = DecisionEngine().analyze(demo_snapshot())
    ids = [recommendation.id for recommendation in result.recommendations]
    assert ids[0] == "stabilize-now"
    assert "convert-gold" in ids
    assert "lower-variance" in ids
    assert len(result.state_fingerprint) == 16


def test_engine_can_analyze_neutral_state() -> None:
    snapshot = deepcopy(demo_snapshot())
    player = snapshot.active_player()
    player.stats.current_health = player.stats.max_health
    player.current_gold = 300
    player.score.deaths = 0
    player.score.kills = 4
    player.score.assists = 4
    player.score.creep_score = 150
    snapshot.events = []
    for enemy in snapshot.enemies_of(player):
        enemy.level = player.level
        enemy.score.kills = 0
    result = DecisionEngine().analyze(snapshot)
    assert result.recommendations
    assert result.features.survival_risk < 0.3

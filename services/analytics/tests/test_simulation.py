from riftpilot_analytics.core.simulation import simulate_defense
from riftpilot_analytics.domain.models import DefenseSimulationRequest


def test_armor_upgrade_reduces_physical_damage() -> None:
    result = simulate_defense(DefenseSimulationRequest(health=1000, armor=50, magic_resist=40, incoming_physical=1200, incoming_magic=0, incoming_true=0, add_armor=50))
    assert result.upgraded.effective_damage < result.baseline.effective_damage
    assert result.damage_reduction_gain > 0


def test_health_upgrade_can_flip_lethal_scenario() -> None:
    result = simulate_defense(DefenseSimulationRequest(health=600, armor=0, magic_resist=0, incoming_physical=700, incoming_magic=0, incoming_true=0, add_health=200))
    assert not result.baseline.survives
    assert result.upgraded.survives
    assert "flip" in result.verdict

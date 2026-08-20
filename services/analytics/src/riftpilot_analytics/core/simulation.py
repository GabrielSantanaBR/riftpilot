"""Counterfactual defensive-stat simulator."""

from __future__ import annotations

from riftpilot_analytics.domain.models import (
    DefenseScenario,
    DefenseSimulationRequest,
    DefenseSimulationResult,
)


def _damage_multiplier(resistance: float) -> float:
    if resistance >= 0:
        return 100.0 / (100.0 + resistance)
    return 2.0 - 100.0 / (100.0 - resistance)


def _scenario(*, health: float, armor: float, magic_resist: float, physical: float, magic: float, true_damage: float) -> DefenseScenario:
    effective = physical * _damage_multiplier(armor) + magic * _damage_multiplier(magic_resist) + true_damage
    remaining = health - effective
    return DefenseScenario(effective_damage=round(effective, 2), remaining_health=round(remaining, 2), survives=remaining > 0, survival_margin=round(remaining / health, 4))


def simulate_defense(request: DefenseSimulationRequest) -> DefenseSimulationResult:
    baseline = _scenario(health=request.health, armor=request.armor, magic_resist=request.magic_resist, physical=request.incoming_physical, magic=request.incoming_magic, true_damage=request.incoming_true)
    upgraded = _scenario(health=request.health + request.add_health, armor=request.armor + request.add_armor, magic_resist=request.magic_resist + request.add_magic_resist, physical=request.incoming_physical, magic=request.incoming_magic, true_damage=request.incoming_true)
    reduction_gain = baseline.effective_damage - upgraded.effective_damage
    margin_gain = upgraded.remaining_health - baseline.remaining_health
    if not baseline.survives and upgraded.survives:
        verdict = "The proposed defensive stats flip this scenario from lethal to survivable."
    elif margin_gain > 150:
        verdict = "The proposed defensive stats materially improve the survival margin."
    elif margin_gain > 0:
        verdict = "The proposed defensive stats help, but the survival gain is modest."
    else:
        verdict = "The proposed change does not improve this damage scenario."
    return DefenseSimulationResult(baseline=baseline, upgraded=upgraded, damage_reduction_gain=round(reduction_gain, 2), survival_margin_gain=round(margin_gain, 2), verdict=verdict)

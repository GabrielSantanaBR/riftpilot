"""Deterministic demo match used for portfolio reviews and UI development."""

from riftpilot_analytics.domain.models import (
    ChampionStats,
    GameEvent,
    GameSnapshot,
    ItemState,
    PlayerState,
    Score,
    SnapshotSource,
    Team,
)


def demo_snapshot() -> GameSnapshot:
    active_id = "RiftPilot Demo#BR1"
    return GameSnapshot(
        source=SnapshotSource.DEMO,
        game_time=1125.0,
        game_mode="CLASSIC",
        map_name="Summoner's Rift",
        active_player_id=active_id,
        players=[
            PlayerState(riot_id=active_id, champion_name="Orianna", team=Team.ORDER, level=11, is_active=True, score=Score(kills=3, deaths=5, assists=4, creep_score=118, ward_score=16.2), items=[ItemState(item_id=6657, name="Rod of Ages", price=2600), ItemState(item_id=3020, name="Sorcerer's Shoes", price=1100)], stats=ChampionStats(current_health=612, max_health=1780, armor=71, magic_resist=43, attack_damage=78, ability_power=164, move_speed=365, ability_haste=20), current_gold=1480),
            PlayerState(riot_id="AllyTop#BR1", champion_name="Gnar", team=Team.ORDER, level=12, score=Score(kills=2, deaths=3, assists=3, creep_score=137)),
            PlayerState(riot_id="AllyJungle#BR1", champion_name="Vi", team=Team.ORDER, level=10, score=Score(kills=4, deaths=4, assists=5, creep_score=94)),
            PlayerState(riot_id="EnemyMid#BR1", champion_name="Syndra", team=Team.CHAOS, level=12, score=Score(kills=7, deaths=2, assists=2, creep_score=146)),
            PlayerState(riot_id="EnemyJungle#BR1", champion_name="Lee Sin", team=Team.CHAOS, level=11, score=Score(kills=4, deaths=3, assists=6, creep_score=109)),
            PlayerState(riot_id="EnemyTop#BR1", champion_name="Renekton", team=Team.CHAOS, level=12, score=Score(kills=3, deaths=4, assists=3, creep_score=132)),
        ],
        events=[
            GameEvent(event_id=1, event_name="ChampionKill", event_time=978, actor="EnemyMid#BR1", victim=active_id),
            GameEvent(event_id=2, event_name="ChampionKill", event_time=1044, actor="EnemyJungle#BR1", victim=active_id),
            GameEvent(event_id=3, event_name="ChampionKill", event_time=1102, actor=active_id, victim="EnemyTop#BR1"),
        ],
    )

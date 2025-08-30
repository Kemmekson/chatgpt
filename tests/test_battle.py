from war_game.entities import Army, Faction, Province, Unit
from war_game.battle import resolve_battle


def test_stronger_army_wins():
    prov = Province("Test")
    f1 = Faction("F1")
    f2 = Faction("F2")
    strong = Army("Strong", [Unit("S", 5, 2, 10) for _ in range(3)], prov, f1)
    weak = Army("Weak", [Unit("W", 1, 1, 5) for _ in range(3)], prov, f2)
    f1.armies.append(strong)
    f2.armies.append(weak)

    winner, loser = resolve_battle(strong, weak)

    assert winner is strong
    assert loser is weak
    assert weak.is_defeated()

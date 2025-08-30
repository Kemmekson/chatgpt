from __future__ import annotations

import random
from typing import Tuple

from .entities import Army, Unit


def _unit_duel(attacker: Unit, defender: Unit) -> None:
    """Resolve one unit attacking another."""
    damage = max(1, attacker.attack - defender.defense)
    defender.health -= damage


def resolve_battle(attacker: Army, defender: Army) -> Tuple[Army, Army]:
    """Simulate a very simple deterministic battle.

    Returns a tuple ``(winner, loser)``.
    """

    atk_units = attacker.alive_units()
    def_units = defender.alive_units()

    while atk_units and def_units:
        atk = random.choice(atk_units)
        target = random.choice(def_units)
        _unit_duel(atk, target)
        def_units = defender.alive_units()
        if not def_units:
            break
        counter = random.choice(def_units)
        target = random.choice(atk_units)
        _unit_duel(counter, target)
        atk_units = attacker.alive_units()

    if attacker.is_defeated():
        return defender, attacker
    return attacker, defender

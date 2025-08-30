from __future__ import annotations

import random
from typing import Dict, List

from .battle import resolve_battle
from .entities import Army, Faction, Province, Unit


class Game:
    def __init__(self) -> None:
        self.provinces: Dict[str, Province] = {}
        self.factions: Dict[str, Faction] = {}
        self.player: Faction
        self.ai: Faction
        self.turn: int = 1
        self._setup_world()

    # --- setup ---
    def _setup_world(self) -> None:
        # Create provinces
        a = Province("A")
        b = Province("B")
        c = Province("C")
        d = Province("D")
        for p in (a, b, c, d):
            self.provinces[p.name] = p
        # Connect provinces
        a.add_neighbor(b)
        b.add_neighbor(c)
        c.add_neighbor(d)

        # Create factions
        self.player = Faction("Empire")
        self.ai = Faction("Orcs")
        self.factions[self.player.name] = self.player
        self.factions[self.ai.name] = self.ai

        # Assign starting provinces
        self.player.add_province(a)
        self.player.add_province(b)
        self.ai.add_province(c)
        self.ai.add_province(d)

        # Create armies
        def make_basic_army(name: str, location: Province, faction: Faction) -> Army:
            units = [Unit("Infantry", 5, 2, 10) for _ in range(5)]
            army = Army(name=name, units=units, location=location, faction=faction)
            faction.armies.append(army)
            return army

        make_basic_army("1st", a, self.player)
        make_basic_army("Waaagh", d, self.ai)

    # --- game logic ---
    def move_army(self, army: Army, destination: Province) -> None:
        if destination not in army.location.neighbors:
            print(f"{destination.name} is not adjacent to {army.location.name}")
            return
        print(f"Moving {army.name} to {destination.name}")
        army.location = destination
        if destination.owner and destination.owner is not army.faction:
            print("Battle! Armies clash in", destination.name)
            enemy_armies = [a for a in destination.owner.armies if a.location is destination]
            if enemy_armies:
                enemy = enemy_armies[0]
                winner, loser = resolve_battle(army, enemy)
                print(f"{winner.faction.name} wins the battle")
                loser.faction.armies.remove(loser)
                if loser.faction is destination.owner:
                    destination.owner.remove_province(destination)
                winner.faction.add_province(destination)

    def player_turn(self) -> None:
        print("\n--- Player Turn ---")
        while True:
            self.print_state()
            cmd = input("Command (move <army_index> <province>/end): ")
            if cmd.strip() == "end":
                break
            parts = cmd.split()
            if len(parts) != 3 or parts[0] != "move":
                print("Invalid command")
                continue
            try:
                idx = int(parts[1])
                army = self.player.armies[idx]
            except (ValueError, IndexError):
                print("Invalid army index")
                continue
            dest_name = parts[2].upper()
            dest = self.provinces.get(dest_name)
            if not dest:
                print("Unknown province")
                continue
            self.move_army(army, dest)

    def ai_turn(self) -> None:
        print("\n--- AI Turn ---")
        army = self.ai.armies[0]
        possible = [p for p in army.location.neighbors]
        dest = random.choice(possible)
        self.move_army(army, dest)

    def print_state(self) -> None:
        print(f"Turn {self.turn}")
        print("Provinces:")
        for p in self.provinces.values():
            owner = p.owner.name if p.owner else "Neutral"
            print(f"  {p.name}: {owner}")
        print("Player Armies:")
        for i, army in enumerate(self.player.armies):
            print(f"  [{i}] {army.name} at {army.location.name} ({len(army.alive_units())} units)")

    def check_victory(self) -> bool:
        if not self.ai.provinces or not self.ai.armies:
            print("You win!")
            return True
        if not self.player.provinces or not self.player.armies:
            print("You lost!")
            return True
        return False

    def run(self) -> None:
        while True:
            self.player_turn()
            if self.check_victory():
                break
            self.ai_turn()
            if self.check_victory():
                break
            self.turn += 1


if __name__ == "__main__":
    Game().run()

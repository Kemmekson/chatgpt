from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Unit:
    """A single unit participating in battles."""

    name: str
    attack: int
    defense: int
    health: int

    def is_alive(self) -> bool:
        return self.health > 0


@dataclass
class Army:
    """Collection of units that moves together."""

    name: str
    units: List[Unit]
    location: "Province"
    faction: "Faction"

    def alive_units(self) -> List[Unit]:
        return [u for u in self.units if u.is_alive()]

    def is_defeated(self) -> bool:
        return len(self.alive_units()) == 0


@dataclass
class Province:
    """A single location on the campaign map."""

    name: str
    neighbors: List["Province"] = field(default_factory=list)
    owner: Optional["Faction"] = None

    def add_neighbor(self, other: "Province") -> None:
        if other not in self.neighbors:
            self.neighbors.append(other)
            other.neighbors.append(self)


@dataclass
class Faction:
    """A player or AI controlled faction."""

    name: str
    armies: List[Army] = field(default_factory=list)
    provinces: List[Province] = field(default_factory=list)

    def add_province(self, province: Province) -> None:
        province.owner = self
        if province not in self.provinces:
            self.provinces.append(province)

    def remove_province(self, province: Province) -> None:
        if province in self.provinces:
            self.provinces.remove(province)
        if province.owner is self:
            province.owner = None

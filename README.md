# Simple Total War-like Game

This repository contains a very small text-based strategy game inspired by the campaign layer of *Total War: Warhammer 3*. It features factions, provinces, armies and a primitive battle simulator.

## Requirements

- Python 3.10+

## Running the Game

```bash
python -m war_game.game
```

The game presents a simple command line interface. Use `move <army_index> <province>` to move armies and `end` to finish your turn.

## Running Tests

```bash
pytest
```

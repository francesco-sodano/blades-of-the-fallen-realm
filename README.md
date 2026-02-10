# Blades of the Fallen Realm

<p align="center">
	<img src="docs_assets/Blades_of_the_Fallen_realm-Logo.jpg" alt="Blades of the Fallen Realm Logo">
</p>

A retro-style side-scrolling beat 'em up inspired by SEGA Golden Axe (1989), built with **PyGame**. Choose from three warriors — a banished king, an elven ranger, or a dwarven champion — and fight through 5 levels of Bogworts, Ironhides, and dark sorcery. Features combo combat, tiered magic, rideable mounts, and local 2-player co-op.



## Features

- **3 Playable Characters** — Theron Ashblade (Warrior), Sylara Windarrow (Ranger), Drunn Ironhelm (Berserker), each with unique stats, combos, and 3-tier magic abilities
- **Local 2-Player Co-op** — Drop-in co-op with independent lives, magic, and scoring; same-character allowed via palette swaps
- **5 Levels** — Journey from the Greenhollow to the Shadow Gate, each with unique environments, enemies, and a boss fight
- **Golden Axe Combat** — 3-hit combo chains, jump attacks, running attacks, throws, and tiered magic (Starstone Shards)
- **Rideable Mounts** — Commandeer Stoneward Destriers and enemy Snarlfangs for mounted combat
- **Camp Bonus Scenes** — Between levels, whack Pixi Scavengers for bonus items (homage to Golden Axe's gnome-kicking)
- **Pseudo-3D Plane** — Y-sorted depth rendering for classic beat 'em up perspective
- **HD Pixel Art** — Modern retro aesthetic at 960×540 resolution, 60 FPS

## World Lore

> *A thousand years ago, the Fallen Realm of Valdros was shattered by the Shadow — a nameless darkness that corrupted the land. Three ancient kingdoms fell: the Greywood of the elves, the Ironroot halls of the dwarves, and the throne of men at Stormwatch. Now the Dark Warden, a sorcerer-king who serves the Shadow, raises armies of Bogworts and Ironhides to claim what remains. Three warriors — a banished king, an elven ranger, and a dwarven champion — take up arms to carve a path from the last free village of Greenhollow to the Shadow Gate itself and end the darkness.*

## Characters

| Character | Archetype | Weapon | HP | Strength | Speed | Magic |
|---|---|---|---|---|---|---|
| **Theron Ashblade** | Warrior | Emberfang (flame sword) | 8/10 | 8/10 | 6/10 | 6/10 |
| **Sylara Windarrow** | Ranger | Bow & dual blades | 6/10 | 6/10 | 10/10 | 10/10 |
| **Drunn Ironhelm** | Berserker | Twin axes | 10/10 | 10/10 | 4/10 | 4/10 |

## Controls

| Action | Player 1 | Player 2 |
|---|---|---|
| Move | Arrow keys | WASD |
| Attack | Z | J |
| Jump | X | K |
| Magic | C | L |

Gamepad support: up to 2 gamepads auto-detected.

## Requirements

- Python 3.12.12+
- [uv](https://docs.astral.sh/uv/) package manager
- pygame-ce

## Installation

```bash
# Install uv if you haven't already
pip install uv

# Clone and setup the repository
git clone https://github.com/francesco-sodano/blades-of-the-fallen-realm.git
cd blades-of-the-fallen-realm

# Install Python 3.12.12, create venv, and sync all dependencies
uv python install 3.12.12
uv venv --python 3.12.12 .venv
uv sync --group dev
```

## Usage

```bash
uv run python -m blades_of_the_fallen_realm
```

## Development

This project uses [uv](https://docs.astral.sh/uv/) as the package manager and a [Dev Container](https://containers.dev/) for a consistent development environment.

### Quick start

1. Open the repo in VS Code and select **"Reopen in Container"**.
2. The dev container installs Python 3.12, creates a `.venv`, and syncs all dependencies automatically.

### Project structure

```
src/blades_of_the_fallen_realm/
├── engine/          # Core systems (game loop, camera, collision, rendering, input)
├── entities/        # Base entity, player, enemy, mount, pickup classes
├── characters/      # Theron, Sylara, Drunn character definitions
├── enemies/         # Enemy types + bosses/
│   └── bosses/
├── levels/          # Level data, spawn triggers, camp scenes
├── ui/              # HUD, menus, game over screen
├── utils/           # Spritesheet loader, debug tools
├── assets/          # Sprites, backgrounds, music, SFX
│   ├── sprites/
│   ├── backgrounds/
│   ├── ui/
│   ├── music/
│   └── sfx/
├── main.py          # Entry point
└── settings.py      # Game constants
tests/               # Tests (pytest)
scripts/             # Helper scripts
```

### Run tests

```bash
uv run pytest
```

### Format & lint

```bash
uv run black .
uv run mypy src/
```

## Docker

```bash
docker build -t blades_of_the_fallen_realm .
docker run --rm blades_of_the_fallen_realm
```

## Game Design

See [DESIGN.md](DESIGN.md) for the full game design document covering all characters, enemies, levels, mechanics, and technical specifications.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
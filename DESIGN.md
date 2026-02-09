# Blades of the Fallen Realm — Game Design Document

## Overview

A retro-style side-scrolling beat 'em up inspired by SEGA Golden Axe (1989), built with **PyGame (pygame-ce)**. Features **modern HD pixel art**, **single-player and local 2-player co-op**, 5 levels, 3 playable characters, combo combat, tiered magic, rideable mounts, and a camp bonus scene between levels.

---

## Technical Specs

| Spec | Value |
|---|---|
| Engine | PyGame (pygame-ce) |
| Language | Python 3.12+ |
| Resolution | 960×540 (16:9, base 480×270 scaled 2x) |
| Frame Rate | 60 FPS |
| Art Style | Modern HD pixel art |
| Players | 1-2 local co-op |
| Platform | Desktop (Windows/Mac/Linux) |

---

## World Lore

A thousand years ago, the Fallen Realm of Valdros was shattered by the Shadow — a nameless darkness that corrupted the land. Three ancient kingdoms fell: the Greywood of the elves, the Ironroot halls of the dwarves, and the throne of men at Stormwatch. Now the Dark Warden, a sorcerer-king who serves the Shadow, raises armies of Bogworts and Ironhides to claim what remains. Three warriors — a banished king, an elven ranger, and a dwarven champion — take up arms to carve a path from the last free village of Greenhollow to the Shadow Gate itself and end the darkness.

---

## Playable Characters

### Theron Ashblade — Warrior (Ax Battler archetype)

| Stat | Value |
|---|---|
| HP | 8/10 |
| Strength | 8/10 |
| Speed | 6/10 |
| Magic | 6/10 |

- Exiled king, wields the flame-forged sword *Emberfang*
- Balanced stats, 3-hit sword combo, strong throws
- **Magic tiers**:
  - Tier 1 (1-2 shards): *Emberfang's Flare* — short-range sword aura burst
  - Tier 2 (3-4 shards): *Oathbound Legion* — ghostly soldiers sweep across screen
  - Tier 3 (5+ shards): *Ashblade's Wrath* — full-screen fire wave, heavy damage
- **P2 palette**: Darker cloak, silver armor trim

### Sylara Windarrow — Ranger (Tyris Flare archetype)

| Stat | Value |
|---|---|
| HP | 6/10 |
| Strength | 6/10 |
| Speed | 10/10 |
| Magic | 10/10 |

- Elven archer from the Greywood, fastest character, strongest magic
- Ranged normal attack (bow), lower HP, agile combos
- **Magic tiers**:
  - Tier 1 (1-2 shards): *Greywood Volley* — volley of enchanted arrows
  - Tier 2 (3-4 shards): *Stormlight Barrage* — rain of arrows covers most of screen
  - Tier 3 (5+ shards): *Wrath of the Ancients* — massive light explosion, highest damage in game
- **P2 palette**: Grey outfit, silver hair

### Drunn Ironhelm — Berserker (Gilius archetype)

| Stat | Value |
|---|---|
| HP | 10/10 |
| Strength | 10/10 |
| Speed | 4/10 |
| Magic | 4/10 |

- Dwarven champion from the Ironroot Mines, twin-axe wielder
- Highest HP, strongest melee, slowest, weakest magic
- **Magic tiers**:
  - Tier 1 (1-2 shards): *Axe Quake* — ground pound, stuns nearby enemies
  - Tier 2 (3-4 shards): *Ironroot Fury* — whirlwind axe spin
  - Tier 3 (5+ shards): *Mountain's Wrath* — earthquake across screen, moderate damage
- **P2 palette**: Silver helm, blue armor trim

---

## Combat System

### Moves (All Characters)

| Move | Input (P1) | Input (P2) | Description |
|---|---|---|---|
| Walk | Arrows | WASD | 8-directional on pseudo-3D plane |
| Attack | Z | J | Combo chain: hit → hit → knockdown (3-hit) |
| Jump | X | K | Hop with height on Z-axis |
| Magic | C | L | Activate magic (consumes Starstone Shards) |
| Jump Attack | X then Z | K then J | Aerial downward strike |
| Running Attack | →→ + Z | →→ + J | Dash + strike |
| Throw | Z near enemy | J near enemy | Grab and toss directionally |
| Mount | ↑ + Z near mount | ↑ + J near mount | Mount a Stoneward Destrier or Snarlfang |
| Dismount | X while mounted | K while mounted | Jump off mount |

### Animation States

`IDLE`, `WALK`, `ATTACK1`, `ATTACK2`, `ATTACK3`, `JUMP`, `JUMP_ATTACK`, `MAGIC`, `HIT`, `KNOCKDOWN`, `GETUP`, `DEATH`, `MOUNT`, `MOUNT_ATTACK`

### Combo System

- 3-hit combo chain like Golden Axe: hit → hit → knockdown
- Input buffer: track last 3 inputs within 500ms window
- Running attack: double-tap direction + attack
- Jump attack: press attack while airborne for downward strike
- Throw: press attack when adjacent to enemy (within grab range)

---

## Enemy Roster

### Regular Enemies

| Enemy | Type | First Appears | Description |
|---|---|---|---|
| **Bogwort Grunt** | Melee | Level 1 | Green-skinned bog creature, 2-hit combo, low HP. Palette swaps (green/brown/grey) |
| **Bogwort Archer** | Ranged | Level 1 | Fires arrows from range, retreats when approached, low HP |
| **Bogwort Witch** | Caster | Level 1 | Rare, stays behind others, buffs nearby enemies with speed aura, very low HP |
| **Snarlfang Rider** | Mounted | Level 1 | Goblin on wolf-beast. Knock goblin off → ride the Snarlfang. Higher HP |
| **Bogwort Tunneler** | Melee | Level 2 | Pickaxe variant, slightly tougher than Grunt |
| **Hollow Bats** | Flying | Level 2 | Small flying enemies, swoop attacks |
| **Ironhide Brute** | Heavy melee | Level 3 | Armored, shield-bearing, 3-hit combo |
| **Ironhide Marksman** | Heavy ranged | Level 3 | Crossbow, slow but high damage |
| **Ironhide Ravager** | Charger | Level 4 | No armor, charging torch attacks, high damage |
| **Ashland Reaver** | Elite melee | Level 5 | Late-game elite orc |
| **Sandstalker Lancer** | Spear | Level 5 | Desert warrior, long reach |
| **Siege Troll** | Heavy | Level 5 | Large war troll |
| **Stone Troll** | Mini-boss | Level 2+ | Club attacks, rock throwing |

### Bosses

| Boss | Level | Mechanics |
|---|---|---|
| **The Hollow King** | 1 — Stormwatch Peak | Spectral warlord in black armor. Cursed flameblade charges, fear screech stun (close range), summons 2 Bogwort adds. 3 attack phases |
| **Gravelord Thusk** | 2 — Ironroot Depths | Massive troll. Club slam (area), throws rocks, charges. Slow but devastating |
| **Gorath the Branded** | 3 — Broken Shore | Elite Ironhide captain. Shield bash, bow shot (ranged phase), sword combo (melee phase), throws knife. Fast and relentless |
| **The Dark Warden's Fist** | 4 — Bastion Keep | Massive armored champion. Two-handed sword, ground slam, armor phase (must break armor before dealing HP damage) |
| **The Voice of Shadow** | 5 — Shadow Gate | Sorcerer lieutenant. Dark magic projectiles, ground corruption zones, summons enemy waves. 4 phases with increasing intensity |

### Enemy AI

- AI states: `IDLE`, `PATROL`, `APPROACH`, `ATTACK`, `RETREAT`, `HIT_STUN`, `KNOCKDOWN`, `DEATH`
- Simple behavior: if player in range → approach; if in attack range → attack; after attacking → brief retreat
- Flanking: enemies approach from both sides when multiple are present
- Co-op targeting: each enemy targets the **nearest player** (re-evaluates every 1-2 seconds)
- In co-op, enemies split between targets rather than all piling on one player

### Enemy Difficulty Scaling

- Across levels, enemies get palette swaps with increased HP/damage/speed
- Level 5 enemies have ~2x the stats of Level 1 equivalents
- Scaling factor: ~1.3x per level

---

## Levels

### Level 1: The Greenhollow to Stormwatch Peak

- **Setting**: Rolling green meadows → sparse trees → rocky ruins on a windswept peak
- **Parallax**: 3 layers — distant mountains, midground trees, foreground rocks
- **Enemies**: Bogwort Grunt, Bogwort Archer, Bogwort Witch, Snarlfang Rider
- **Waves**: 4-5 scroll-lock combat zones, 12-15 total enemies
- **Boss**: The Hollow King
- **Pace**: Tutorial level — introduces all basic mechanics gradually

### Level 2: Crystalveil to the Ironroot Depths

- **Setting**: Elven sanctuary entrance → deep dwarven mines, narrow caverns
- **Parallax**: Mine pillars, deep chasms, glowing ore veins
- **Enemies**: Bogwort Tunneler, Bogwort Archer, Hollow Bats, Stone Troll (mini-boss)
- **Boss**: Gravelord Thusk
- **New mechanic**: Narrow walkable depth band

### Level 3: The Greywood to Broken Shore

- **Setting**: Golden forest → dark riverside
- **Parallax**: Massive trees, dappled light → murky river banks
- **Enemies**: Ironhide Brute, Ironhide Marksman, Bogwort Scout
- **Boss**: Gorath the Branded
- **New mechanic**: Introduces Ironhide enemies (tougher, shield-bearing)
- **Mount**: Snarlfang riders and Stoneward Destriers available

### Level 4: The Stoneward Plains to Bastion Keep

- **Setting**: Open plains → fortress siege (wall defense)
- **Parallax**: Wide grasslands, distant fortress → stone walls, siege ladders
- **Enemies**: Ironhide Ravager, Ironhide Siege Climber, Bogwort Demolisher
- **Boss**: The Dark Warden's Fist
- **Mount**: Stoneward Destriers available on the plains section

### Level 5: The Ashlands to the Shadow Gate

- **Setting**: Open battlefield → volcanic dark terrain → obsidian fortress gate
- **Parallax**: Scorched earth, lava glow, ash clouds → obsidian gate
- **Enemies**: Ashland Reaver, Sandstalker Lancer, Siege Troll (largest enemy variety)
- **Boss**: The Voice of Shadow (final boss)
- **Pace**: 30-35 total enemies, most intense level

---

## Items & Pickups

| Item | Effect | Source |
|---|---|---|
| **Starstone Shard** | +1 magic charge (max 9) | Dropped by Bogwort Witches, or from Pixi Scavengers in camp scenes |
| **Hearthloaf** | Small health restore | Rare enemy drops |
| **Lifeleaf** | Full health restore | Very rare, 1-2 per level |

- Pickups are **first-come, first-served** in co-op (not duplicated)
- Health items heal only the player who picks them up

---

## Mounts: Stoneward Destrier

- Armored warhorse from the Stoneward Plains
- Press ↑ + Attack near a riderless mount to ride
- **Mounted state**: Faster movement, mounted attack (lance charge / trampling)
- Mount has its own HP — takes damage for the player
- Dismount on mount death or player input
- Available in Levels 1, 3, and 4
- In co-op, encounters spawn **2 mounts** so both players can ride
- Enemy Snarlfangs can also be commandeered after knocking off their rider

---

## Camp Scene (Between Levels)

- Campfire rest scene after each level (4 total, between levels 1→2, 2→3, 3→4, 4→5)
- **Pixi Scavengers** — small impish creatures that run around stealing supplies
- Players whack them to get Starstone Shards and Hearthloaf drops
- **15-second timed bonus phase**
- In co-op: 2-3 Pixis spawn instead of 1-2
- Direct homage to Golden Axe's gnome-kicking camp scenes

---

## 2-Player Co-op System

### Controls

| | Player 1 | Player 2 |
|---|---|---|
| Move | Arrow keys | WASD |
| Attack | Z | J |
| Jump | X | K |
| Magic | C | L |

- Either player can alternatively use a gamepad (auto-detect up to 2 via `pygame.joystick`)

### Drop-In Join

- Player 2 presses their Attack key (J or gamepad button) on the title screen to join
- Game works as single-player until P2 joins
- **No mid-level join** — P2 must join before character select

### Character Select

- Sequential: P1 picks first, then P2
- **Same character allowed** — P2 gets an alternate palette swap
- If P2 never joined, skip P2 selection

### Camera

- Tracks the **midpoint** between both players
- **Boundary leash**: neither player can move more than ~400px off-screen edge
- Scroll-lock zones function the same for both players

### Player Lifecycle

- Each player has **independent**: HP, lives (3 each), magic shards, score
- When a player loses all lives → spectator (camera follows surviving player)
- **Game over only when both players are dead**
- Continue screen: each player gets their own 10-second countdown independently (3 continues each)

### Enemy AI in Co-op

- Each enemy targets the **nearest player** (re-evaluates every 1-2 seconds)
- Enemies split between targets rather than all piling on one player
- Spawn waves are **1.5x larger** in co-op (max 8 enemies on screen vs 6 in solo)
- Boss HP increases by **40%**
- If Player 2 loses all lives, spawns revert to single-player counts

### Collision Rules

- **No friendly fire** — players cannot damage each other
- **Players walk through each other** — no body-blocking
- Thrown enemies CAN hit the other player's targets (cooperative crowd control)

---

## HUD Layout

```
┌──────────────────────────────────────────────────────────┐
│ [P1 Portrait] ██████████ HP          HP ██████████ [P2]  │
│               ✦✦✦✦✦○○○○ Shards  Shards ✦✦✦○○○○○○       │
│               Score: 12400          Score: 9800          │
│                                                          │
│                        [GAME AREA]                       │
│                                                          │
│                         GO →                             │
└──────────────────────────────────────────────────────────┘
```

- P1: top-left. P2: top-right (mirrored)
- Health bar is segmented (Golden Axe style)
- Shard count shows filled/empty icons (max 9)
- "GO →" centered, appears when scroll unlocks

---

## Game Flow

```
TITLE SCREEN → CHARACTER SELECT (P1, then P2 if joined)
    → LEVEL 1 → CAMP → LEVEL 2 → CAMP → LEVEL 3 → CAMP → LEVEL 4 → CAMP → LEVEL 5
        → ENDING SCREEN / HIGH SCORE
    (on death → CONTINUE SCREEN → resume or GAME OVER)
```

### Game States

`MENU` → `CHARACTER_SELECT` → `PLAYING` → `CAMP` → `PAUSED` → `GAME_OVER`

---

## Progression & Balance

| Parameter | Value |
|---|---|
| Starting lives | 3 per player |
| Extra lives | At 50,000 and 100,000 points |
| Continues | 3 per player (10-second countdown) |
| Level 1 enemies | 12-15 total + boss |
| Level 5 enemies | 30-35 total + boss |
| Enemy scaling per level | ~1.3x HP/damage/speed |
| Max on-screen enemies (solo) | 6 |
| Max on-screen enemies (co-op) | 8 |
| Target Level 1 clear time | 5-8 minutes |
| Player stat upgrades | None (roguelike purity) |
| Death respawn | In place with brief invincibility |

---

## Scoring

| Event | Points |
|---|---|
| Bogwort Grunt kill | 100 |
| Bogwort Archer kill | 150 |
| Bogwort Witch kill | 200 |
| Snarlfang Rider kill | 250 |
| Ironhide Brute kill | 300 |
| Ironhide Ravager kill | 350 |
| Stone Troll kill | 500 |
| Boss kill | 2,000 |
| No-damage wave bonus | 500 |
| Time bonus (level end) | Variable |

- High score saved locally (JSON file)
- Per-player scores in co-op

---

## Audio Plan

### Sound Effects

- Hit impacts: 3 variations (avoid repetition)
- Enemy death cries
- Magic activation (escalating sound per tier)
- Mount gallop loop
- Menu select/confirm
- Pickup chimes (distinct for Shards vs health items)

### Music

- Each level gets a BGM track (epic orchestral-inspired chiptune/retro)
- Boss fights switch to an intense variant
- Camp scene: calm melody
- Title screen: heroic theme
- Game over: somber

### Visual Effects

- Screen shake on heavy hits and magic (3-frame, configurable intensity)
- Screen flash on magic activation and boss death
- Enemy death: blink and fall flat
- Boss death: extended sequence with screen flash

---

## Debug Mode

- Toggle with **F1**
- Hitbox/hurtbox visualization (colored rectangles)
- FPS counter
- Enemy AI state labels
- Spawn zone markers
- Player position/velocity readout

---

## Key Design Decisions

| Decision | Rationale |
|---|---|
| PyGame over Phaser | User preference; simpler Python workflow |
| Drop-in co-op (no mid-level join) | Keeps implementation simple, matches Golden Axe arcade |
| Same character allowed in co-op | Palette swaps are easier than restricting choice |
| No friendly fire | Keeps co-op fun; avoids griefing |
| Shared pickups, not duplicated | Creates authentic arcade resource competition |
| Leash camera over split-screen | Split-screen breaks the aesthetic; leash forces cooperation |
| Stoneward Destriers over flying mounts | Ground mounts integrate cleanly with horizontal scrolling |
| Starstone Shards from drops + Pixi Scavengers | Keeps both loot flow and iconic camp scene gnome-kicking |
| 5 levels | Matches Golden Axe's length; each introduces 1-2 new enemy types |
| Voice of Shadow as final boss | A sorcerer boss with summons is mechanically richer than a giant dark lord |
| No IP references | All names, lore, and locations are original to avoid copyright issues |

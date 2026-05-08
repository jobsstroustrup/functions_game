# Math Kills Monsters: Functions Game

A pygame-based educational game where players construct mathematical functions in real-time via keyboard input to target and defeat enemies. The more sophisticated your function, the stronger the attack. This is a creative fusion of math fluency and game mechanics.

## Project Overview

**Status**: Alpha 4.0 (completed, 2020)
**Author**: Zhenyu He (Peking University, undergraduate)
**Codebase**: ~1,309 lines Python (pygame framework)

## Core Features

- **Custom DSL (Domain-Specific Language)**
  - Keyboard input (e=exp, l=ln, s=sin, a=arcsin, d=reciprocal) maps to token stream
  - Real-time symbolic simplification (auto-cancels inverse pairs: ln of e, arcsin of sin, etc.)
  - Non-linear cost model penalizing nested functions (exponential scaling)

- **Game Mechanics**
  - 9 enemy types with distinct behavior patterns (static, circular motion, rushers, splitters, healers)
  - 4 progress-bar types (HP, MP, cost, percentage)
  - Complete coordinate system abstraction (world to screen physics)
  - 60 FPS gameplay with event-driven state machine

- **Educational Design**
  - 11-level tutorial curriculum (knowledge sequencing)
  - Each level teaches one math operation via fixed target-point lists
  - Progression: single ops, basic composition, nested functions

## Architecture

| File | Lines | Responsibility |
|------|-------|---|
| `main.py` | 334 | Game loop, state machine (menu/battle/pause/end/tutorial) |
| `func.py` | 178 | DSL engine (stream, simplification, evaluation, cost model) |
| `graph.py` | 329 | Rendering, coordinate transforms, UI bars |
| `enemy.py` | 236 | Enemy class hierarchy (9 types) |
| `story*.py` | ~200 | Story/tutorial level definitions |

## Author Contributions

**Zhenyu He (vault: hzy)**
- Designed and implemented the complete DSL engine (`func.py`)
- Coordinate system abstraction and rendering pipeline (`graph.py`)
- Enemy class hierarchy and 9-enemy behavior design (`enemy.py`)
- Tutorial curriculum design and knowledge sequencing (`story1.py`)
- All artwork (8 PNG) and audio (2 OGG/MP3) assets created by Zhenyu He
- Full design and implementation across all subsystems

## Technologies

- Python 3 | pygame | Object-oriented design (OOP inheritance)
- Symbolic algebra (simplification rules) | Game balance design

## Distinctive Characteristics

1. **DSL as game interface**: keyboard keys map to function-building language, not traditional game controls
2. **Symbolic algebra in real-time**: the `simp_stream` function performs automatic algebraic simplification
3. **Educational intentionality**: tutorial levels deliberately sequence math concepts from basic to complex
4. **Physics intuition**: cost model uses non-linear exponential scaling to incentivize elegant expressions

## License

GNU General Public License v3 (see `Alpha4.0/Alpha4.0/main.py` header)

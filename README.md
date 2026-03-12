# Pokémon Game

A 2D top-down Pokémon-style game built with Python and Pygame.

## Features

- Animated player character with directional sprites (up, down, left, right)
- Smooth, delta-time-based movement for consistent speed regardless of framerate
- Tiled grassy map background
- Randomly placed Pokémon on the map, selected from a sprite sheet of starter Pokémon
- Keyboard controls for movement and escape to quit

## Requirements

- Python 3.x
- [Pygame](https://www.pygame.org/) (`pip install pygame`)

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/rowkav09/Pokemon-game.git
   cd Pokemon-game
   ```

2. Install dependencies:
   ```bash
   pip install pygame
   ```

3. Run the latest version of the game:
   ```bash
   python "Main Script V2.py"
   ```

## Controls

| Key | Action |
|-----|--------|
| ← Arrow | Move left |
| → Arrow | Move right |
| ↑ Arrow | Move up |
| ↓ Arrow | Move down |
| Escape | Quit the game |

## Project Structure

```
Pokemon-game/
├── Main Script.py        # Original version of the game
├── Main Script V2.py     # Improved version with delta-time movement and Pokémon sprites
├── images/
│   ├── trainer_sheet.png          # Player character sprite sheet
│   └── 3d_starter_sheet.png       # Pokémon sprite sheet
└── maps/
    └── grassy.jpg                 # Map background tile
```

## Credits

Original project by [bubse](https://github.com/bubse).


[Hacker Terminal Simulator (Ciph3rSt3@lth)](https://replit.com/@cassiansl29/CipherStealth?v=1)

A text-based terminal game that simulates a retro hacking experience with ASCII graphics.

## Current update 0.1
- Just released!
- Working on adding content to VOIDBORN

## Features

- Home Terminal interface with basic commands
- Secret remote server to discover and connect to
- ASCII Snake game that you can play inside the terminal
- Authentic-looking terminal effects and animations

## Coming Soon

- More content
- Tetris

## Installation Instructions

### Prerequisites

- Python 3.11 or higher
- Required Python packages (cryptography, etc.)

### Option 1: Run on Replit (Recommended)

1. Visit the project on Replit: [CipherStealth](https://replit.com/@cassiansl29/CipherStealth?v=1)
3. Click the "Fork" button to create your own copy
4. Press the "Run" button to start the game

### Option 2: Local Installation

1. Clone the repository:
   ```
   git clone https://github.com/YourUsername/hacker-terminal-simulator.git
   cd hacker-terminal-simulator
   ```

2. Install dependencies:
   ```
   pip install cryptography
   ```

3. Run the game:
   ```
   python main.py
   ```

## How to Play

1. Start the game with `python main.py`
2. Use these commands in the home terminal:
   - `dir` - List directory contents
   - `cd` - Change directory
   - `type` - Display file contents
   - `run` - Run a program (e.g., 'run snake.exe')
   - `cls` - Clear screen
   - `help` - Show help message
   - `ip_connect <ip>` - Connect to a remote server
   - `exit` - Exit the terminal

3. Explore the directories to find clues and hidden secrets
4. Try playing the Snake game in the GAMES directory

## Project Structure

```
├── src
│   ├── ascii_games.py    # ASCII games like Snake
│   ├── crypto_utils.py   # Cryptography utilities
│   ├── log_generator.py  # Random log generator
│   ├── remote_server.py  # Remote server simulation
│   └── terminal_effects.py # Terminal visual effects
└── main.py               # Main game entry point
```

## Tips

- Look for clues in text files
- The remote server might have valuable information
- Use WASD keys to control the Snake game

## Deployment on Replit

This game is designed to run on Replit. To deploy your own version:

1. Fork the project
2. Go to the "Deployment" tab
3. Click "Deploy" to make it accessible online

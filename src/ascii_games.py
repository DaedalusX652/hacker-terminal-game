import os
import sys
import time
import random
import threading
import queue
from typing import List, Tuple, Optional

# Handle platform-specific imports
if os.name == 'nt':
    import msvcrt
else:
    msvcrt = None

class SnakeGame:
    def __init__(self, width: int = 20, height: int = 10):
        self.width = width
        self.height = height
        self.snake: List[Tuple[int, int]] = [(width // 2, height // 2)]
        self.direction = (1, 0)  # Starting direction: right
        self.food = self._spawn_food()
        self.score = 0
        self.game_over = False
        self._input_queue = queue.Queue()

    def _spawn_food(self) -> Tuple[int, int]:
        """Spawn food at a random location not occupied by the snake."""
        while True:
            food = (random.randint(0, self.width - 1), 
                   random.randint(0, self.height - 1))
            if food not in self.snake:
                return food

    def _get_input(self):
        """Get keyboard input without blocking."""
        while not self.game_over:
            if os.name == 'nt':  # Windows
                if msvcrt and msvcrt.kbhit():
                    key = msvcrt.getch()
                    self._input_queue.put(key)
            else:  # Unix-like
                import select
                try:
                    if select.select([sys.stdin], [], [], 0.1)[0]:
                        key = sys.stdin.read(1)
                        self._input_queue.put(key)
                except:
                    pass  # Handle any potential select errors
            time.sleep(0.1)

    def start(self):
        """Start the game."""
        if not os.name == 'nt':
            # Set up Unix terminal
            import termios
            import tty
            old_settings = termios.tcgetattr(sys.stdin)
            try:
                tty.setraw(sys.stdin.fileno())

                # Start input thread
                input_thread = threading.Thread(target=self._get_input)
                input_thread.daemon = True
                input_thread.start()

                self._game_loop()
            finally:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        else:
            # Windows version
            input_thread = threading.Thread(target=self._get_input)
            input_thread.daemon = True
            input_thread.start()
            self._game_loop()

    def _game_loop(self):
        """Main game loop."""
        while not self.game_over:
            # Draw the game
            self._draw()

            # Handle input
            try:
                while not self._input_queue.empty():
                    key = self._input_queue.get_nowait()
                    self._handle_input(key)
            except queue.Empty:
                pass

            # Move snake
            new_head = (
                (self.snake[0][0] + self.direction[0]) % self.width,
                (self.snake[0][1] + self.direction[1]) % self.height
            )

            # Check collision with self
            if new_head in self.snake:
                self.game_over = True
                break

            self.snake.insert(0, new_head)

            # Check if food eaten
            if new_head == self.food:
                self.score += 1
                self.food = self._spawn_food()
            else:
                self.snake.pop()

            time.sleep(0.2)  # Game speed

        # Game over screen
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\nGame Over! Score: {self.score}")
        print("\nPress Enter to exit...")
        sys.exit(0)

    def _handle_input(self, key):
        """Handle keyboard input."""
        if isinstance(key, bytes):
            key = key.lower()
        else:
            key = key.lower().encode()

        # Direction mappings
        directions = {
            b'w': (0, -1),  # Up
            b'a': (-1, 0),  # Left
            b's': (0, 1),   # Down
            b'd': (1, 0),   # Right
        }

        if key in directions:
            # Don't allow reversing direction
            new_dir = directions[key]
            if (new_dir[0] != -self.direction[0] or 
                new_dir[1] != -self.direction[1]):
                self.direction = new_dir

    def _draw(self):
        """Draw the game board."""
        os.system('cls' if os.name == 'nt' else 'clear')

        # Draw top border with cool ASCII art
        print('╔' + '═' * (self.width * 2) + '╗')

        for y in range(self.height):
            print('║', end='')
            for x in range(self.width):
                pos = (x, y)
                if pos == self.snake[0]:
                    print('██', end='')  # Snake head
                elif pos in self.snake:
                    print('██', end='')  # Snake body
                elif pos == self.food:
                    print('◆ ', end='')  # Food
                else:
                    print('  ', end='')  # Empty space
            print('║')

        # Draw bottom border
        print('╚' + '═' * (self.width * 2) + '╝')
        print(f'\nScore: {self.score}')
        print('\nUse WASD to move, Ctrl+C to exit')
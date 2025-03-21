import os
import sys
import time
import random
import threading
import queue
from typing import List, Tuple

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
            try:
                if sys.stdin.isatty():
                    import termios
                    import tty
                    import select

                    # Save the terminal settings
                    old_settings = termios.tcgetattr(sys.stdin)
                    try:
                        # Set the terminal to raw mode
                        tty.setraw(sys.stdin.fileno())

                        if select.select([sys.stdin], [], [], 0.1)[0]:
                            key = sys.stdin.read(1)
                            if key == '\x03':  # Ctrl+C
                                self.game_over = True
                                break
                            self._input_queue.put(key)
                    finally:
                        # Restore terminal settings
                        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            except Exception:
                time.sleep(0.1)
                continue

    def start(self):
        """Start the game."""
        try:
            # Start input thread
            input_thread = threading.Thread(target=self._get_input)
            input_thread.daemon = True
            input_thread.start()

            self._game_loop()
        except KeyboardInterrupt:
            self.game_over = True
        finally:
            if os.name != 'nt':
                # Restore terminal
                os.system('stty sane')

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

    def _handle_input(self, key):
        """Handle keyboard input."""
        # Direction mappings
        directions = {
            'w': (0, -1),   # Up
            'a': (-1, 0),   # Left
            's': (0, 1),    # Down
            'd': (1, 0),    # Right
            'W': (0, -1),   # Up
            'A': (-1, 0),   # Left
            'S': (0, 1),    # Down
            'D': (1, 0),    # Right
        }

        if key in directions:
            new_dir = directions[key]
            # Don't allow reversing direction
            if (new_dir[0] != -self.direction[0] or 
                new_dir[1] != -self.direction[1]):
                self.direction = new_dir

    def _draw(self):
        """Draw the game board."""
        os.system('cls' if os.name == 'nt' else 'clear')

        # Draw top border
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
import os
import time
import random
import sys
import select
import termios
import tty

class SnakeGame:
    def __init__(self, width=20, height=10):
        self.width = width
        self.height = height
        self.snake = [(width // 2, height // 2)]
        self.direction = (1, 0)  # (x, y) Right direction initially
        self.food = self._place_food()
        self.score = 0
        self.game_over = False
        
    def _place_food(self):
        """Place food at a random position not occupied by the snake."""
        while True:
            food = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            if food not in self.snake:
                return food
                
    def _get_key(self, timeout=0.1):
        """Get a keypress without waiting for enter."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            rlist, _, _ = select.select([sys.stdin], [], [], timeout)
            if rlist:
                return sys.stdin.read(1)
            else:
                return None
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            
    def _update_direction(self, key):
        """Update the snake's direction based on keyboard input."""
        if key == 'w' and self.direction != (0, 1):  # Up
            self.direction = (0, -1)
        elif key == 's' and self.direction != (0, -1):  # Down
            self.direction = (0, 1)
        elif key == 'a' and self.direction != (1, 0):  # Left
            self.direction = (-1, 0)
        elif key == 'd' and self.direction != (-1, 0):  # Right
            self.direction = (1, 0)
        elif key == 'q':  # Quit
            self.game_over = True
            
    def _move_snake(self):
        """Move the snake in its current direction."""
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % self.width, (head_y + dy) % self.height)
        
        # Check if snake hits itself
        if new_head in self.snake:
            self.game_over = True
            return
            
        self.snake.insert(0, new_head)
        
        # Check if snake eats food
        if new_head == self.food:
            self.score += 1
            self.food = self._place_food()
        else:
            self.snake.pop()
            
    def _draw_game(self):
        """Draw the current game state."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Draw top border
        print("+" + "-" * self.width + "+")
        
        # Draw game area
        for y in range(self.height):
            line = "|"
            for x in range(self.width):
                if (x, y) == self.snake[0]:
                    line += "O"  # Snake head
                elif (x, y) in self.snake[1:]:
                    line += "o"  # Snake body
                elif (x, y) == self.food:
                    line += "X"  # Food
                else:
                    line += " "  # Empty space
            line += "|"
            print(line)
            
        # Draw bottom border
        print("+" + "-" * self.width + "+")
        print(f"Score: {self.score} | Use WASD to move, Q to quit")
        
    def start(self):
        """Start the game loop."""
        try:
            while not self.game_over:
                self._draw_game()
                key = self._get_key(0.1)
                if key:
                    self._update_direction(key)
                self._move_snake()
                time.sleep(0.1)
                
            print(f"\nGame Over! Final Score: {self.score}")
            print("Press any key to exit...")
            self._get_key()
            
        except Exception as e:
            print(f"Game error: {str(e)}")
        finally:
            # Reset terminal
            os.system('cls' if os.name == 'nt' else 'clear')

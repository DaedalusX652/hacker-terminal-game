import sys
import time
import random
from typing import List

class TerminalEffects:
    @staticmethod
    def type_text(text: str, min_speed: float = 0.01, max_speed: float = 0.05) -> None:
        """Simulate typing effect for text output."""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(random.uniform(min_speed, max_speed))
        sys.stdout.write('\n')

    @staticmethod
    def progress_bar(duration: int, prefix: str = '') -> None:
        """Display an animated progress bar."""
        bar_width = 40
        for i in range(bar_width + 1):
            progress = float(i) / bar_width
            block = '█' * i + '░' * (bar_width - i)
            percentage = int(progress * 100)
            sys.stdout.write(f'\r{prefix} |{block}| {percentage}%')
            sys.stdout.flush()
            time.sleep(duration/bar_width/2)  # Reduced sleep time
        sys.stdout.write('\n')

    @staticmethod
    def matrix_effect(duration: float = 1.0) -> None:
        """Create a simple Matrix-like rain effect."""
        characters = "01"
        width = 70

        end_time = time.time() + duration
        while time.time() < end_time:
            line = ''.join(random.choice(characters) for _ in range(width))
            sys.stdout.write(f"\033[1;32m{line}\033[0m\n")
            sys.stdout.flush()
            time.sleep(0.03)  # Reduced sleep time

    @staticmethod
    def clear_screen() -> None:
        """Clear the terminal screen."""
        sys.stdout.write('\033[2J\033[H')
        sys.stdout.flush()

    @staticmethod
    def blink_text(text: str, times: int = 3) -> None:
        """Make text blink in the terminal."""
        for _ in range(times):
            sys.stdout.write('\r' + ' ' * len(text))
            sys.stdout.flush()
            time.sleep(0.2)  # Reduced sleep time
            sys.stdout.write('\r' + text)
            sys.stdout.flush()
            time.sleep(0.2)  # Reduced sleep time
        sys.stdout.write('\n')
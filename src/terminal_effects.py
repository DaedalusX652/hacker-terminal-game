
import sys
import time
import random
import os
from typing import List

class TerminalEffects:
    def __init__(self):
        self.width = 80
        self.height = 24

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        return ""

    def type_text(self, text: str, delay: float = 0.02, newline: bool = True):
        """Type text with a delay between characters."""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        if newline:
            sys.stdout.write("\n")
        sys.stdout.flush()

    def progress_bar(self, duration: float, message: str = "Loading"):
        """Display a progress bar that fills over the specified duration."""
        width = 40
        sys.stdout.write(f"\n{message}: [" + " " * width + "] 0%")
        sys.stdout.flush()

        for i in range(width + 1):
            time.sleep(duration / width)
            percent = int((i / width) * 100)
            bar = "=" * i + " " * (width - i)
            sys.stdout.write(f"\r{message}: [{bar}] {percent}%")
            sys.stdout.flush()
        sys.stdout.write("\n")

    def matrix_effect(self, duration: float = 2.0):
        """Display a Matrix-like effect for the specified duration."""
        chars = "01"
        cols = self.width
        rows = 10
        
        start_time = time.time()
        while time.time() - start_time < duration:
            # Generate a random line of characters
            line = "".join(random.choice(chars) for _ in range(cols))
            sys.stdout.write("\033[32m" + line + "\033[0m\n")
            sys.stdout.flush()
            time.sleep(0.05)
            
        self.clear_screen()

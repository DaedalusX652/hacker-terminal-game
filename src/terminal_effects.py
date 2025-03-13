
import sys
import time
import random
import os
from typing import List

class TerminalEffects:
    def __init__(self):
        self.width = 80
        self.height = 24
        # Get actual terminal dimensions if possible
        try:
            columns, lines = os.get_terminal_size()
            self.width = columns
            self.height = lines
        except:
            pass  # Use defaults if fails

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        return ""

    def type_text(self, text: str, delay: float = 0.02, newline: bool = True):
        """Type text with a delay between characters."""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            # Reduce delay for spaces to make it feel more natural
            time.sleep(delay if char != ' ' else delay/2)
        if newline:
            sys.stdout.write("\n")
        sys.stdout.flush()

    def progress_bar(self, duration: float, message: str = "Loading"):
        """Display a progress bar that fills over the specified duration."""
        width = min(40, self.width - 20)  # Ensure it fits in the terminal
        
        # Pre-calculate some values for efficiency
        steps = width + 1
        sleep_time = duration / steps
        
        sys.stdout.write(f"\n{message}: [" + " " * width + "] 0%")
        sys.stdout.flush()

        for i in range(steps):
            time.sleep(sleep_time)
            percent = int((i / width) * 100)
            bar = "=" * i + " " * (width - i)
            sys.stdout.write(f"\r{message}: [{bar}] {percent}%")
            sys.stdout.flush()
        sys.stdout.write("\n")

    def matrix_effect(self, duration: float = 2.0):
        """Display a Matrix-like effect for the specified duration."""
        chars = "01"
        cols = self.width
        rows = min(10, self.height - 2)
        
        # Pre-generate some random lines for efficiency
        all_lines = []
        for _ in range(rows * 2):  # Generate extra lines for variation
            all_lines.append("".join(random.choice(chars) for _ in range(cols)))
        
        start_time = time.time()
        line_index = 0
        
        while time.time() - start_time < duration:
            # Use pre-generated lines with some randomization
            line = all_lines[line_index % len(all_lines)]
            line_index += 1
            
            # Occasionally modify some characters for more randomness
            if random.random() > 0.7:
                pos = random.randint(0, cols-1)
                line = line[:pos] + random.choice(chars) + line[pos+1:]
                
            sys.stdout.write("\033[32m" + line + "\033[0m\n")
            sys.stdout.flush()
            time.sleep(0.05)
            
        self.clear_screen()

#!/usr/bin/env python3
import os
import sys
import time
from typing import List
from src.crypto_utils import CryptoOperations
from src.terminal_effects import TerminalEffects
from src.log_generator import LogGenerator
from src.remote_server import RemoteServer
from src.ascii_games import SnakeGame

def display_home_computer():
    effects = TerminalEffects()
    effects.clear_screen()
    effects.type_text("\033[1;32m=== HOME TERMINAL ===\033[0m")
    effects.type_text("\nJust another boring night...")
    time.sleep(0.5)  # Reduced delay
    effects.type_text("\nScrolling through old files...")
    time.sleep(0.3)  # Reduced delay
    effects.type_text("\nType 'help' for available commands.\n")

class HomeComputer:
    def __init__(self):
        self.effects = TerminalEffects()
        self.files = {
            'DOCUMENTS': {
                'todo.txt': "1. Clean up old files\n2. Update security software\n3. Check that weird network glitch",
                'work.txt': "Just normal boring work stuff...\nDeadlines...\nMeetings...",
                'SECRETS.txt': """/////////////////////////////////////////////////
FOUND THIS WHILE DIGGING THROUGH OLD ARCHIVES
SOMETHING'S NOT RIGHT WITH THIS SERVER

IP: 192.168.13.666

STRANGE LOGS ABOUT SHADOWS AND VOID
MOST FILES ENCRYPTED

USE ip_connect TO ACCESS - NO PASSWORD NEEDED
WHOEVER FINDS THIS, BE CAREFUL
///////////////////////////////////////////////"""
            },
            'GAMES': {
                'snake.exe': "[ASCII Snake Game - Type 'run snake.exe' to play]",
                'tetris.exe': "[Coming soon...]"
            },
            'SYSTEM': {
                'config.sys': "[SYSTEM FILE]",
                'autoexec.bat': "[SYSTEM FILE]"
            }
        }
        self.current_dir = 'C:'

    def handle_command(self, command: str) -> str:
        """Process user commands and return output."""
        try:
            parts = command.strip().split()
            if not parts:
                return ""

            cmd = parts[0].lower()
            args = parts[1:] if len(parts) > 1 else []

            commands = {
                'dir': self._dir,
                'cd': self._cd,
                'type': self._type,
                'cls': lambda _: self.effects.clear_screen() or "",
                'run': self._run,
                'help': lambda _: """Available commands:
dir      - List directory contents
cd       - Change directory
type     - Display file contents
run      - Run a program (e.g., 'run snake.exe')
cls      - Clear screen
help     - Show this help message
ip_connect <ip> - Connect to remote server
exit     - Exit terminal""",
                'ip_connect': lambda _: None
            }

            if cmd in commands:
                return commands[cmd](args)
            return f"Bad command or file name: {parts[0]}"
        except Exception as e:
            return f"Command error: {str(e)}"

    def _dir(self, args: List[str] = None) -> str:
        folder = 'C:' if self.current_dir == 'C:' else self.current_dir.split('\\')[-1]
        output = [
            " Volume in drive C is HOME_DISK",
            f" Directory of {self.current_dir}",
            ""
        ]

        if folder == 'C:':
            for d in ['DOCUMENTS', 'GAMES', 'SYSTEM']:
                output.append(f"<DIR>          {d}")
        elif folder in self.files:
            for filename in sorted(self.files[folder].keys()):
                output.append(f"         {filename}")

        num_files = len(self.files.get(folder, {}))
        output.extend([
            "",
            f"     {num_files} File(s)",
            "     0 bytes free"
        ])
        return "\n".join(output)

    def _cd(self, args: List[str]) -> str:
        if not args:
            self.current_dir = 'C:'
            return ""

        path = args[0].upper()
        if path in ['..', '\\', '/']:
            self.current_dir = 'C:'
            return ""
        elif path in ['DOCUMENTS', 'GAMES', 'SYSTEM']:
            self.current_dir = f'C:\\{path}'
            return ""

        return f"Invalid directory {args[0]}"

    def _type(self, args: List[str]) -> str:
        if not args:
            return "Missing filename"

        filename = args[0]
        folder = 'C:' if self.current_dir == 'C:' else self.current_dir.split('\\')[-1]

        if folder == 'C:':
            return f"File not found - {filename}"

        if folder in self.files:
            for f in self.files[folder].keys():
                if f.upper() == filename.upper():
                    return self.files[folder][f]

        return f"File not found - {filename}"

    def _run(self, args: List[str]) -> str:
        if not args:
            return "Missing program name"

        if self.current_dir != 'C:\\GAMES':
            return "Can only run programs from C:\\GAMES"

        program = args[0].lower()
        if program == 'snake.exe':
            try:
                game = SnakeGame()
                self.effects.clear_screen()
                game.start()
                self.effects.clear_screen()
                return "Game session ended"
            except Exception as e:
                return f"Error running game: {str(e)}"
        elif program == 'tetris.exe':
            return "Tetris coming soon..."

        return f"Cannot run {program}"

def connect_to_server(ip):
    effects = TerminalEffects()
    effects.type_text(f"\n\n[+] Attempting connection to {ip}...")
    effects.progress_bar(1, "Establishing connection")
    effects.matrix_effect(1.0)
    return True

def main():
    effects = TerminalEffects()
    home_pc = HomeComputer()

    try:
        # Start with home computer scene
        display_home_computer()

        while True:
            try:
                # Show proper DOS-style directory prompt
                prompt = f"\033[1;36m{home_pc.current_dir}> \033[0m"
                command = input(prompt).strip()

                if command.lower() == "exit":
                    effects.type_text("\nTerminating session... Goodbye!")
                    break

                if command.startswith("ip_connect"):
                    parts = command.split()
                    if len(parts) != 2:
                        print("Syntax error. Usage: ip_connect <ip>")
                        continue

                    if parts[1] == "192.168.13.666":
                        if connect_to_server("192.168.13.666"):
                            crypto = CryptoOperations()
                            log_gen = LogGenerator()
                            remote_server = RemoteServer()

                            if remote_server.start_session():
                                while True:
                                    try:
                                        user_input = input(f"\033[1;36m{remote_server.current_path}>\033[0m ")
                                        if user_input.lower() == 'exit':
                                            effects.type_text("\n[!] Connection terminated")
                                            break

                                        output = remote_server.handle_command(user_input)
                                        if output:
                                            print(output)
                                    except KeyboardInterrupt:
                                        print("\n\033[1;31m[!] Command interrupted\033[0m")
                                        continue
                    else:
                        print(f"Connection failed: Could not reach {parts[1]}")
                else:
                    output = home_pc.handle_command(command)
                    if output is not None:
                        print(output)

            except Exception as e:
                print(f"\033[1;31mCommand error: {str(e)}\033[0m")
                continue

    except KeyboardInterrupt:
        effects.clear_screen()
        effects.type_text("\n\033[1;31m[!] EMERGENCY SHUTDOWN INITIATED\033[0m")
        effects.progress_bar(1, "Cleaning up")
        effects.type_text("\033[1;31m[!] SYSTEM TERMINATED\033[0m")
        sys.exit(0)
    except Exception as e:
        print(f"\033[1;31m[ERROR] An unexpected error occurred: {str(e)}\033[0m")
        sys.exit(1)

if __name__ == "__main__":
    main()
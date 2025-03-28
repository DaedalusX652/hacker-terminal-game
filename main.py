#!/usr/bin/env python3
import os
import sys
import time
from typing import List, Dict
from src.crypto_utils import CryptoOperations
from src.terminal_effects import TerminalEffects
from src.log_generator import LogGenerator
from src.remote_server import RemoteServer
from src.ascii_games import SnakeGame

def display_home_computer():
    effects = TerminalEffects()
    effects.clear_screen()
    effects.type_text("Award BIOS v4.51PG, An Energy Star Ally")
    effects.type_text("Copyright (C) 1984-1996, Award Software, Inc.")
    time.sleep(0.5)
    effects.clear_screen()
    effects.type_text("Intel Pentium Processor 166MHz")
    effects.type_text("Memory Test: 8192K OK  ")
    effects.clear_screen()
    time.sleep(0.5)
    effects.type_text("Press DEL to enter Setup")
    time.sleep(0.00001)
    effects.clear_screen()
    effects.type_text("Starting MS-DOS...")
    time.sleep(0.5)
    effects.clear_screen()
    effects.type_text("HIMEM is testing extended memory...done. ")
    effects.type_text("Loading MS-DOS... ")
    effects.type_text("DEVICE=C:/DOS/HIMEM.SYS /TESTMEM:OFF")
    effects.type_text("DEVICE=C:/DOS/EMM386.EXE NOEMS")
    effects.type_text("DEVICE=C:/DOS/OAKCDROM.SYS /D:MSCD001")
    time.sleep(0.5)
    effects.clear_screen()
    effects.type_text("C:/> PATH C:/DOS")
    effects.type_text("C:/> PROMPT $P$G ")
    effects.type_text("C:/> SET BLASTER=A220 I5 D1 H5 P330 T6 ")
    effects.type_text("C:/> LH C:/DOS/MSCDEX.EXE /D:MSCD001")
    time.sleep(0.5)
    effects.clear_screen()
    effects.type_text("C:/> REM ██████.EXE detected")
    effects.type_text("C:/> REM System error. Replace user.")
    time.sleep(0.8)
    effects.clear_screen()
    effects.type_text("C:/> REM Do not look at the screen.")
    time.sleep(0.8)
    effects.clear_screen()
    effects.type_text("C:/> REMEM Do not look at the screen.")
    time.sleep(0.8)
    effects.clear_screen()
    effects.type_text("C:/> REMEMBER Do not look at the screen.")
    time.sleep(0.8)
    effects.clear_screen()
    time.sleep(1.2)
    effects.type_text("Bootup successful")
    effects.type_text("\nType 'help' for available commands")

class HomeComputer:
    def __init__(self):
        self.effects = TerminalEffects()
        # Simplified directory structure
        self.files = {
            'DOCUMENTS': ['todo.txt', 'awman.txt', 'IAMWAITING.PLS'],
            'GAMES': ['snake.exe', 'tetris.exe'],
            'SYSTEM': ['config.sys', 'autoexec.bat']
        }

        self.file_contents = {
            'todo.txt': "1. Pay bills\n2. Update security software\n3. Check that weird network glitch",
            'awman.txt': "Just normal boring work stuff...\nDeadlines...\nMeetings...",
            'IAMWAITING.PLS': """FOUND THIS WHILE DIGGING THROUGH OLD ARCHIVES
SOMETHING'S NOT RIGHT WITH THIS SERVER

IP: 192.168.13.666

STRANGE LOGS ABOUT SHADOWS AND VOID
MOST FILES ENCRYPTED

USE ip_connect TO ACCESS - NO PASSWORD NEEDED
WHOEVER FINDS THIS, BE CAREFUL""",
            'snake.exe': "[ASCII Snake Game - Type 'run snake.exe' to play]",
            'tetris.exe': "[Coming soon...]",
            'config.sys': "[SYSTEM FILE]",
            'autoexec.bat': "[SYSTEM FILE]"
        }
        self.current_dir = 'C:'

    def _dir(self, args=None):
        """List directory contents."""
        output = [
            " Volume in drive C is HOME_DISK",
            f" Directory of {self.current_dir}",
            ""
        ]

        if self.current_dir == 'C:':
            for dirname in sorted(self.files.keys()):
                output.append(f"<DIR>          {dirname}")
            output.extend([
                "",
                "     0 File(s)",
                f"     {len(self.files)} Dir(s)     0 bytes free"
            ])
        else:
            dirname = self.current_dir.split('\\')[-1]
            if dirname in self.files:
                for filename in sorted(self.files[dirname]):
                    output.append(f"         {filename}")
                output.extend([
                    "",
                    f"     {len(self.files[dirname])} File(s)",
                    "     0 bytes free"
                ])

        return "\n".join(output)

    def _cd(self, args):
        """Change directory."""
        if not args:
            self.current_dir = 'C:'
            return ""

        path = args[0].upper()
        if path in ['..', '\\', '/']:
            self.current_dir = 'C:'
            return ""

        if path in self.files:
            self.current_dir = f'C:\\{path}'
            return ""

        return f"Invalid directory {args[0]}"

    def _type(self, args):
        """Display file contents."""
        if not args:
            return "Missing filename"

        filename = args[0]
        if self.current_dir == 'C:':
            return f"File not found - {filename}"

        dirname = self.current_dir.split('\\')[-1]
        if dirname in self.files:
            for f in self.files[dirname]:
                if f.upper() == filename.upper():
                    return self.file_contents[f]

        return f"File not found - {filename}"

    def _run(self, args):
        """Run a program (game)."""
        if not args:
            return "Missing program name"

        if self.current_dir != 'C:\\GAMES':
            return "File found in GAMES"

        program = args[0].lower()
        if program == 'snake.exe':
            try:
                effects = TerminalEffects()
                effects.clear_screen()
                game = SnakeGame(width=20, height=10)
                game.start()
                return "Game session ended"
            except Exception as e:
                return f"Error running game: {str(e)}"
        elif program == 'tetris.exe':
            return "Tetris coming soon..."

        return f"Cannot run {program}"

    def update_security(self):
        """Simulate a security update."""
        effects = self.effects
        effects.clear_screen()
        effects.type_text("\n[+] Initiating security system update...")
        time.sleep(1)
        effects.type_text("\n[+] Running system diagnostics...")
        effects.progress_bar(0.5, "Checking security status")  # Fake progress bar
        time.sleep(1)
        effects.type_text("\n[+] Security Update Complete: Critical System Checks Passed!")
        effects.type_text("\n[+] Running command for further security analysis...")
        effects.progress_bar(0.3, "YOU SHOULD NOT BE HERE")  # Fake command execution progress
        time.sleep(1)
        effects.type_text("\n[+] F0LL0W TH3 SH3P3RD")
        time.sleep(0.5)
        effects.clear_screen()

    def handle_command(self, command: str) -> str:
        """Process user commands and return output."""
        command = command.strip()

        # Handle empty or numeric-only inputs
        if not command or command.isdigit():
            return ""

        parts = command.split()
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
exit     - Exit terminal
secure-pc - Check for security updates""",
            'ip_connect': lambda _: None,
            'secure-pc': lambda _: self.update_security()
        }

        if cmd in commands:
            return commands[cmd](args)
        return f"Bad command or file name: {parts[0]}"

def connect_to_server(ip):
    effects = TerminalEffects()
    effects.type_text(f"\n\n[+] Attempting connection to {ip}...")
    effects.progress_bar(0.8, "Establishing connection")  # Reduced time for better UX
    effects.matrix_effect(0.8)  # Reduced time for better UX
    return True

def main():
    effects = TerminalEffects()
    home_pc = HomeComputer()

    try:
        display_home_computer()

        while True:
            try:
                command = input(f"{home_pc.current_dir}> ").strip()

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
                                        user_input = input(f"{remote_server.current_path}> ")
                                        if user_input.lower() == 'exit':
                                            effects.type_text("\n[!] Connection terminated")
                                            break

                                        output = remote_server.handle_command(user_input)
                                        if output:
                                            print(output)
                                    except KeyboardInterrupt:
                                        print("\n[!] Command interrupted")
                                        continue
                    else:
                        print(f"Connection failed: Could not reach {parts[1]}")
                else:
                    output = home_pc.handle_command(command)
                    if output:
                        print(output)

            except Exception as e:
                print(f"Command error: {str(e)}")
                continue

    except KeyboardInterrupt:
        effects.clear_screen()
        effects.type_text("\n[!] EMERGENCY SHUTDOWN INITIATED")
        effects.progress_bar(1, "Cleaning up")
        effects.type_text("[!] SYSTEM TERMINATED")
        sys.exit(0)

if __name__ == "__main__":
    main()

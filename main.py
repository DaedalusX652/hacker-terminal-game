#!/usr/bin/env python3
import sys
import time
from src.crypto_utils import CryptoOperations
from src.terminal_effects import TerminalEffects
from src.log_generator import LogGenerator
from src.remote_server import RemoteServer

def display_home_computer():
    effects = TerminalEffects()
    effects.clear_screen()
    effects.type_text("\033[1;32m=== HOME TERMINAL ===\033[0m")
    effects.type_text("\nJust another boring night...")
    time.sleep(1)
    effects.type_text("\nScrolling through old files...")
    time.sleep(0.5)
    effects.type_text("\n[!] Wait... what's this? Found a strange file...")
    time.sleep(0.5)

    # Display the mysterious SECRETS.txt content
    effects.type_text("\n\nOpening SECRETS.txt...")
    effects.progress_bar(1, "Decoding file")

    secret_content = """
    /////////////////////////////////////////////////
    FOUND THIS WHILE DIGGING THROUGH OLD ARCHIVES
    SOMETHING'S NOT RIGHT WITH THIS SERVER

    IP: 192.168.13.666

    STRANGE LOGS ABOUT SHADOWS AND VOID
    MOST FILES ENCRYPTED

    USE ip_connect TO ACCESS - NO PASSWORD NEEDED
    WHOEVER FINDS THIS, BE CAREFUL
    /////////////////////////////////////////////////
    """
    effects.type_text(secret_content)
    effects.type_text("\nType 'help' for available commands...")

def connect_to_server(ip):
    effects = TerminalEffects()
    effects.type_text(f"\n\n[+] Attempting connection to {ip}...")
    effects.progress_bar(1, "Establishing connection")
    effects.matrix_effect(1.0)
    return True

def main():
    effects = TerminalEffects()
    print("[DEBUG] Terminal effects initialized")

    try:
        # Start with home computer scene
        display_home_computer()

        while True:
            command = input("\033[1;36mC:\\HOME> \033[0m").strip().lower()  # DOS-style prompt

            if command == "exit":
                effects.type_text("\nTerminating session... Goodbye!")
                break
            elif command == "help":
                print("\nAvailable commands:")
                print("- ip_connect <ip>  : Connect to a remote server")
                print("- cls             : Clear the screen")
                print("- help            : Show this help message")
                print("- exit            : Exit the terminal")
            elif command == "cls":
                effects.clear_screen()
            elif command.startswith("ip_connect"):
                parts = command.split()
                if len(parts) != 2:
                    print("Syntax error. Usage: ip_connect <ip>")
                    continue

                if parts[1] == "192.168.13.666":
                    if connect_to_server("192.168.13.666"):
                        # Initialize remote server components
                        crypto = CryptoOperations()
                        log_gen = LogGenerator()
                        remote_server = RemoteServer()
                        print("[DEBUG] All components initialized successfully")

                        # Start remote server session
                        remote_server.start_session()

                        # Interactive terminal loop for remote server
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
                print("Bad command or file name")  # Classic DOS error message

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
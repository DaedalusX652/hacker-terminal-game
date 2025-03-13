#!/usr/bin/env python3
import sys
import time
import random
from src.crypto_utils import CryptoOperations
from src.terminal_effects import TerminalEffects
from src.log_generator import LogGenerator
from src.remote_server import RemoteServer

def main():
    # Initialize components outside try block to ensure availability in except block
    effects = TerminalEffects()
    print("[DEBUG] Terminal effects initialized")

    try:
        # Initialize other components
        crypto = CryptoOperations()
        log_gen = LogGenerator()
        remote_server = RemoteServer()
        print("[DEBUG] All components initialized successfully")

        # Clear screen and show initial animation
        effects.clear_screen()
        print("[DEBUG] Screen cleared")
        effects.type_text("\033[1;32m=== CYBER SECURITY TERMINAL v2.0 ===\033[0m")
        print("[DEBUG] Title displayed")
        effects.progress_bar(1, "Initializing systems")
        print("[DEBUG] Initial screen setup complete")

        # Generate and display encryption demo
        key = crypto.generate_key()
        secret_message = "Critical system data: Authorization codes delta-seven-gamma"
        print("[DEBUG] Starting encryption demo")

        effects.type_text("\n[+] Generating encryption keys...")
        effects.progress_bar(0.5, "Generating RSA keypair")
        print("[DEBUG] Key generation progress bar complete")

        # Perform encryption
        print("[DEBUG] Attempting encryption")
        encrypted_msg, enc_success = crypto.encrypt_message(secret_message, key)
        if not enc_success:
            raise Exception("Encryption failed")
        print("[DEBUG] Encryption successful")

        effects.type_text("\n[+] Encryption Results:")
        print(f"\033[1;33mKey (base64): {key.decode()}\033[0m")
        print(f"\033[1;34mEncrypted: {encrypted_msg.decode()}\033[0m")

        # Matrix effect transition
        print("[DEBUG] Starting matrix effect")
        effects.type_text("\n[+] Initializing system monitoring...")
        effects.matrix_effect(1.0)
        print("[DEBUG] Matrix effect complete")

        # Start remote server session
        print("[DEBUG] Starting remote server session")
        remote_server.start_session()

        # Interactive terminal loop
        while True:
            try:
                user_input = input(f"\033[1;36m{remote_server.current_path}>\033[0m ")
                if user_input.lower() == 'exit':
                    break

                output = remote_server.handle_command(user_input)
                if output:
                    print(output)

                # Randomly show background events
                if random.random() < 0.2:  # 20% chance for each command
                    log_entry = log_gen.generate_log()
                    effects.type_text(f"\033[1;32m{log_entry}\033[0m")

            except KeyboardInterrupt:
                print("\n\033[1;31m[!] Command interrupted\033[0m")
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
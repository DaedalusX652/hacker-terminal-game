import random
import time
from typing import List, Dict, Optional
from dataclasses import dataclass
from .terminal_effects import TerminalEffects
from .crypto_utils import CryptoOperations

@dataclass
class FileNode:
    name: str
    content: str
    is_encrypted: bool = False
    is_hidden: bool = False
    permissions: str = "rw-r--r--"

class RemoteServer:
    def __init__(self):
        self.effects = TerminalEffects()
        self.crypto = CryptoOperations()
        self.current_path = "/"
        self.command_history: List[str] = []
        self._initialize_filesystem()

    def _initialize_filesystem(self):
        """Initialize the virtual filesystem with secrets and encrypted data."""
        self.filesystem: Dict[str, Dict[str, FileNode]] = {
            "/": {},
            "/home": {},
            "/home/admin": {},
            "/home/researcher": {},
            "/home/security": {},
            "/var": {},
            "/var/log": {},
            "/etc": {},
            "/secret": {},
            "/research": {},
            "/research/logs": {},
            "/research/classified": {},
            "/devices": {},
            "/devices/terminals": {},
            "/blackbox": {}
        }

        # Add system files and employee accounts
        self._add_file("/etc/passwd", """root:x:0:0:root:/root:/bin/bash
admin:x:1000:1000:System Administrator:/home/admin:/bin/bash
researcher:x:1001:1001:Lead Researcher:/home/researcher:/bin/bash
security:x:1002:1002:Security Officer:/home/security:/bin/bash
blackbox:x:1003:1003:BlackBox System:/blackbox:/sbin/nologin""")

        # Add shadow file with encrypted passwords
        self._add_file("/etc/shadow", """root:$6$xyz...encrypted...:19432:0:99999:7:::
admin:$6$saltstring$encrypted_hash:19432:0:99999:7:::
researcher:$6$another$different_hash:19432:0:99999:7:::
security:$6$classified$top_secret_hash:19432:0:99999:7:::""", True)

        # Add bash history with suspicious commands
        self._add_file("/home/admin/.bash_history", """cd /research/logs
cat experiment_001.log
cd /research/classified
chmod 600 void_incursion.log
ssh blackbox@localhost
./activate_containment.sh
tail -f /var/log/void.log""", True)

        # Add suspicious security logs
        self._add_file("/var/log/auth.log", """Failed login attempt from 192.168.1.100
Successful login for admin
[ALERT] Privilege escalation detected
[WARNING] Multiple failed attempts to access /blackbox
[CRITICAL] Containment field fluctuation detected""")

        # Research Logs
        self._add_file("/research/logs/experiment_001.log", """
VOIDBORN Research Log - Experiment 001
Date: 2024-12-03

Initial observations of the shadow anomaly detected in Sector 7. The entity appears to be composed of non-baryonic matter, completely absorbing all incident light. Team members report intense feelings of unease and disorientation when within 50 meters of the anomaly.

UPDATE: The shadow's behavior has become increasingly erratic. We've lost contact with Dr. Chen's team after they attempted to collect samples.

WARNING: DO NOT ATTEMPT DIRECT CONTACT WITH THE ENTITY.
""")

        self._add_file("/research/logs/experiment_002.log", """
VOIDBORN Research Log - Experiment 002
Date: 2024-12-15

The void creatures are getting stronger. They're no longer confined to Sector 7. Security footage shows them phasing through solid matter. The containment protocols have failed.

Dr. Peterson's latest theory suggests they're not just shadows - they're tears in reality itself. The void is bleeding through.

STATUS: CONTAINMENT BREACH IMMINENT
""", True)

        # Add device terminal logs
        self._add_file("/devices/terminals/containment_001.log", """
CONTAINMENT FIELD TERMINAL - SECTOR 7
STATUS: CRITICAL FAILURE

Field strength: 12% and dropping
Void energy readings: OFF THE SCALE
Last operator: Dr. Sarah Chen
Last entry: "They're coming through. God help us all."
""", True)

        # Add black box data
        self._add_file("/blackbox/containment_data.bin", """
01001000 01000101 01001100 01010000 00100000 
01010100 01001000 01000101 01011001 00100000 
01000001 01010010 01000101 00100000 01001000 
01000101 01010010 01000101
""", True)

        self._add_file("/blackbox/README.txt", """
BLACK BOX SYSTEM - CLASSIFIED
Access Level: OMEGA

This system contains critical void containment data.
DO NOT ATTEMPT TO DECRYPT WITHOUT AUTHORIZATION.
""")

        # Original research logs
        self._add_file("/research/classified/void_incursion.log", """
CLASSIFIED - LEVEL OMEGA
Date: 2024-12-20

They're not just studying us. They're hunting us. The shadows have intelligence - maybe even consciousness. Each incursion grows larger, and the entities are becoming more organized.

I've seen what lies beyond the tears they create. There's a vast darkness out there, watching, waiting. If anyone finds this log, SHUT DOWN THE FACILITY. The barrier between our world and theirs is weakening.

The void hungers.

Last transmission from Dr. Sarah Chen
""", True)

        self._add_file("/research/classified/.final_warning", """
T̷h̷e̷y̷'̷r̷e̷ ̷h̷e̷r̷e̷.̷ ̷T̷h̷e̷y̷'̷r̷e̷ ̷i̷n̷s̷i̷d̷e̷ ̷t̷h̷e̷ ̷w̷a̷l̷l̷s̷.̷ ̷D̷o̷n̷'̷t̷ ̷l̷o̷o̷k̷ ̷a̷t̷ ̷t̷h̷e̷ ̷s̷h̷a̷d̷o̷w̷s̷.̷ ̷T̷h̷e̷y̷ ̷l̷o̷o̷k̷ ̷b̷a̷c̷k̷.̷
""", True)

        # Add original secret files
        self._add_file("/secret/codes.txt", "LAUNCH CODES: DELTA-SEVEN-ALPHA-NINER", True)
        self._add_file("/secret/.hidden_vault", "Bitcoin wallet: 3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy", True)

    def _add_file(self, path: str, content: str, is_hidden: bool = False):
        """Add a file to the virtual filesystem."""
        directory = "/".join(path.split("/")[:-1])
        filename = path.split("/")[-1]
        if directory not in self.filesystem:
            self.filesystem[directory] = {}

        is_encrypted = random.random() < 0.3 and not path.endswith(("passwd", "auth.log"))
        if is_encrypted:
            key = self.crypto.generate_key()
            encrypted_content, _ = self.crypto.encrypt_message(content, key)
            content = f"ENCRYPTED[{encrypted_content.decode()}]"

        self.filesystem[directory][filename] = FileNode(
            name=filename,
            content=content,
            is_encrypted=is_encrypted,
            is_hidden=is_hidden
        )

    def handle_command(self, command: str) -> str:
        """Process user commands and return output."""
        self.command_history.append(command)
        parts = command.strip().split()

        if not parts:
            return ""

        cmd = parts[0].lower()  # Make commands case-insensitive
        args = parts[1:] if len(parts) > 1 else []

        # DOS to Unix command mapping
        dos_to_unix = {
            'dir': 'ls',
            'type': 'cat',
            'cls': 'clear',
            'cd..': 'cd ..'
        }

        # Convert DOS commands to Unix equivalents
        if cmd in dos_to_unix:
            cmd = dos_to_unix[cmd]
            if cmd == 'cd ..' and not args:
                args = ['..']

        commands = {
            'ls': self._ls,
            'cd': self._cd,
            'cat': self._cat,
            'pwd': self._pwd,
            'help': self._help,
            'clear': self._clear
        }

        if cmd in commands:
            return commands[cmd](args)
        return f"Bad command or file name: {cmd}"  # DOS-style error message

    def _ls(self, args: List[str]) -> str:
        """List directory contents."""
        path = args[0] if args else self.current_path
        if path not in self.filesystem:
            return f"ls: cannot access '{path}': No such file or directory"

        files = self.filesystem[path]
        output = []
        for name, node in files.items():
            if not node.is_hidden:
                output.append(f"{node.permissions} {name}")
        return "\n".join(output) if output else ""

    def _cd(self, args: List[str]) -> str:
        """Change directory."""
        if not args:
            self.current_path = "/"
            return ""

        new_path = args[0]
        if new_path.startswith("/"):
            full_path = new_path
        else:
            full_path = f"{self.current_path.rstrip('/')}/{new_path}"

        # Normalize the path
        full_path = full_path.replace("//", "/")
        if full_path in self.filesystem:
            self.current_path = full_path
            return ""
        return f"cd: {new_path}: No such file or directory"

    def _cat(self, args: List[str]) -> str:
        """Display file contents."""
        if not args:
            return "Usage: cat <file>"

        filepath = args[0]
        if not filepath.startswith('/'):
            filepath = f"{self.current_path.rstrip('/')}/{filepath}"

        directory = "/".join(filepath.split("/")[:-1])
        filename = filepath.split("/")[-1]

        if directory not in self.filesystem or filename not in self.filesystem[directory]:
            return f"cat: {filepath}: No such file or directory"

        file_node = self.filesystem[directory][filename]
        if file_node.is_encrypted:
            return f"Error: File is encrypted. Requires decryption key."
        return file_node.content

    def _pwd(self, args: List[str]) -> str:
        """Print working directory."""
        return self.current_path

    def _help(self, args: List[str]) -> str:
        """Display help information."""
        return """Available commands:
ls, dir     - List directory contents
cd, cd..    - Change directory
cat, type   - Display file contents
pwd         - Print working directory
cls, clear  - Clear screen
help        - Show this help message
exit        - Exit current session"""

    def _clear(self, args: List[str]) -> str:
        """Clear the screen."""
        self.effects.clear_screen()
        return ""

    def start_session(self):
        """Start an interactive session with the remote server."""
        self.effects.clear_screen()
        self.effects.type_text("\033[1;31m=== CONNECTING TO REMOTE SERVER ===\033[0m")
        self.effects.progress_bar(1, "Establishing secure connection")

        # ASCII art for VOIDBORN server
        server_art = """
        ===================
        |    VOIDBORN    |
        |  ============  |
        |  ||  ||  ||   |
        |  ||  ||  ||   |
        ===================
        """
        self.effects.type_text(server_art)
        self.effects.type_text("\033[1;32mConnection established. Type 'help' for available commands.\033[0m\n")
        return True
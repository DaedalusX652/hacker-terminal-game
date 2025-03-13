import random
import time
from typing import List, Dict
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
        self.current_path = "/"
        self.effects = TerminalEffects()
        self.crypto = CryptoOperations()

        # Initialize filesystem structure first
        self.filesystem = {}
        self._init_directory_structure()
        self._initialize_filesystem()

    def _init_directory_structure(self):
        """Initialize all directories first"""
        directories = [
            "/",
            "/home",
            "/home/admin",
            "/home/researcher",
            "/home/security",
            "/var",
            "/var/log",
            "/etc",
            "/secret",
            "/research",
            "/research/logs",
            "/research/classified",
            "/devices",
            "/devices/terminals",
            "/blackbox"
        ]
        for directory in directories:
            self.filesystem[directory] = {}

    def _initialize_filesystem(self):
        """Initialize the filesystem with interesting content."""
        # System files
        self._add_file("/etc/passwd", """root:x:0:0:root:/root:/bin/bash
admin:x:1000:1000:System Administrator:/home/admin:/bin/bash
researcher:x:1001:1001:Lead Researcher:/home/researcher:/bin/bash
security:x:1002:1002:Security Officer:/home/security:/bin/bash
blackbox:x:1003:1003:BlackBox System:/blackbox:/sbin/nologin""")

        self._add_file("/etc/shadow", """root:$6$xyz...encrypted...:19432:0:99999:7:::
admin:$6$saltstring$encrypted_hash:19432:0:99999:7:::
researcher:$6$another$different_hash:19432:0:99999:7:::""", True)

        # Research logs
        self._add_file("/research/logs/experiment_001.log", """
VOIDBORN Research Log - Experiment 001
Date: 2024-12-03

Initial observations of the shadow anomaly detected in Sector 7. 
The entity appears to be composed of non-baryonic matter, completely absorbing all incident light.
Team members report intense feelings of unease and disorientation when within 50 meters of the anomaly.

UPDATE: The shadow's behavior has become increasingly erratic. 
We've lost contact with Dr. Chen's team after they attempted to collect samples.

WARNING: DO NOT ATTEMPT DIRECT CONTACT WITH THE ENTITY.""")

        self._add_file("/research/logs/experiment_002.log", """
VOIDBORN Research Log - Experiment 002
Date: 2024-12-15

The void creatures are getting stronger. They're no longer confined to Sector 7.
Security footage shows them phasing through solid matter.
The containment protocols are failing.

Dr. Peterson's latest theory suggests they're not just shadows - they're tears in reality itself.
The void is bleeding through.

STATUS: CONTAINMENT BREACH IMMINENT""", True)

        # Security logs
        self._add_file("/var/log/auth.log", """
[WARNING] Multiple failed attempts to access /blackbox
[CRITICAL] Containment field fluctuation detected
[ALERT] Unauthorized access attempt to research/classified
[WARNING] Multiple login failures for user: admin
[CRITICAL] Security breach detected in Sector 7""")

        # Classified research
        self._add_file("/research/classified/void_incursion.log", """
CLASSIFIED - LEVEL OMEGA
Date: 2024-12-20

They're not just studying us. They're hunting us.
The shadows have intelligence - maybe even consciousness.
Each incursion grows larger, and the entities are becoming more organized.

I've seen what lies beyond the tears they create.
There's a vast darkness out there, watching, waiting.
If anyone finds this log, SHUT DOWN THE FACILITY.
The barrier between our world and theirs is weakening.

The void hungers.

- Last transmission from Dr. Sarah Chen""", True)

        # Black box data
        self._add_file("/blackbox/data.bin", """
01010110 01001111 01001001 01000100 00100000
01000011 01001111 01001101 01001001 01001110 
01000111 00100000 01010100 01001000 01010010 
01001111 01010101 01000111 01001000""", True)

        self._add_file("/blackbox/README.txt", """
BLACK BOX SYSTEM - CLASSIFIED
Access Level: OMEGA

This system contains critical void containment data.
DO NOT ATTEMPT TO DECRYPT WITHOUT AUTHORIZATION.""")

        # Hidden files
        self._add_file("/research/classified/.final_warning", """
T̷h̷e̷y̷'̷r̷e̷ ̷h̷e̷r̷e̷.̷ ̷T̷h̷e̷y̷'̷r̷e̷ ̷i̷n̷s̷i̷d̷e̷ ̷t̷h̷e̷ ̷w̷a̷l̷l̷s̷.̷
D̷o̷n̷'̷t̷ ̷l̷o̷o̷k̷ ̷a̷t̷ ̷t̷h̷e̷ ̷s̷h̷a̷d̷o̷w̷s̷.̷
T̷h̷e̷y̷ ̷l̷o̷o̷k̷ ̷b̷a̷c̷k̷.̷""", True)

    def _add_file(self, path: str, content: str, is_encrypted: bool = False):
        """Add a file to the filesystem."""
        directory = "/".join(path.split("/")[:-1])
        if not directory:
            directory = "/"
        filename = path.split("/")[-1]

        # Ensure the directory exists
        if directory not in self.filesystem:
            self.filesystem[directory] = {}

        # Create the file node
        self.filesystem[directory][filename] = FileNode(
            name=filename,
            content=content,
            is_encrypted=is_encrypted,
            is_hidden=filename.startswith('.')
        )

    def _normalize_path(self, path: str) -> str:
        """Convert any path to absolute path."""
        if not path.startswith('/'):
            path = f"{self.current_path.rstrip('/')}/{path}"

        # Handle .. and .
        parts = []
        for part in path.split('/'):
            if part == '.' or not part:
                continue
            if part == '..':
                if parts:
                    parts.pop()
                continue
            parts.append(part)

        return '/' + '/'.join(parts)

    def handle_command(self, command: str) -> str:
        """Process user commands and return output."""
        parts = command.strip().split()
        if not parts:
            return ""

        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []

        commands = {
            'list': self._list_contents,
            'cd': self._cd,
            'cat': self._cat,
            'pwd': self._pwd,
            'clear': self._clear,
            'help': self._help
        }

        if cmd in commands:
            return commands[cmd](args)
        return f"Unknown command: {cmd}"

    def _list_contents(self, args: List[str]) -> str:
        """List directory contents."""
        path = args[0] if args else self.current_path
        path = self._normalize_path(path)

        if path not in self.filesystem:
            return f"list: cannot access '{path}': No such file or directory"

        output = []

        # Get immediate subdirectories
        subdirs = [d.split("/")[-1] for d in sorted(self.filesystem.keys())
                  if d.startswith(path + "/") and d.count("/") == path.count("/") + 1]

        # Add directories
        for dirname in subdirs:
            output.append(f"<DIR>    {dirname}")

        # Add files from current directory
        for filename, node in sorted(self.filesystem[path].items()):
            if not node.is_hidden:
                encrypted_marker = "[ENCRYPTED] " if node.is_encrypted else ""
                output.append(f"<FILE>   {encrypted_marker}{filename}")

        # Format output
        if output:
            header = f"\nDirectory of {path}\n"
            footer = f"\n{len(output)} item(s)\n"
            return header + "\n".join(output) + footer
        return "Directory is empty"

    def _cd(self, args: List[str]) -> str:
        """Change directory."""
        if not args:
            self.current_path = "/"
            return ""

        new_path = self._normalize_path(args[0])

        if new_path in self.filesystem:
            self.current_path = new_path
            return ""
        return f"cd: {args[0]}: No such file or directory"

    def _cat(self, args: List[str]) -> str:
        """Display file contents."""
        if not args:
            return "Usage: cat <file>"

        path = self._normalize_path(args[0])
        directory = "/".join(path.split("/")[:-1]) or "/"
        filename = path.split("/")[-1]

        if directory not in self.filesystem or filename not in self.filesystem[directory]:
            return f"cat: {args[0]}: No such file or directory"

        file_node = self.filesystem[directory][filename]
        if file_node.is_encrypted:
            return f"Error: File is encrypted. Access denied."
        return file_node.content

    def _pwd(self, args: List[str]) -> str:
        """Print working directory."""
        return self.current_path

    def _help(self, args: List[str]) -> str:
        """Display help information."""
        return """Available commands:
list    - List directory contents
cd      - Change directory
cat     - Display file contents
pwd     - Print working directory
clear   - Clear screen
help    - Show this help message
exit    - Exit session"""

    def _clear(self, args: List[str]) -> str:
        """Clear the screen."""
        self.effects.clear_screen()
        return ""

    def start_session(self):
        """Start an interactive session with the remote server."""
        self.effects.clear_screen()
        self.effects.type_text("\033[1;31m=== CONNECTING TO REMOTE SERVER ===\033[0m")
        self.effects.progress_bar(1, "Establishing secure connection")

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
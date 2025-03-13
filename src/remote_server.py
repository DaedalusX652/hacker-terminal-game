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
            "/var": {},
            "/var/log": {},
            "/etc": {},
            "/secret": {}
        }

        # Add interesting files
        self._add_file("/etc/passwd", "root:x:0:0:root:/root:/bin/bash\nadmin:x:1000:1000::/home/admin:/bin/bash")
        self._add_file("/home/admin/.bash_history", "ssh-keygen\ncd /secret\necho 'launch_codes' > codes.txt\nchmod 600 codes.txt", True)
        self._add_file("/var/log/auth.log", "Failed login attempt from 192.168.1.100\nSuccessful login for admin\nPrivilege escalation detected")
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

        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else []

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
        return f"Command not found: {cmd}"

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
            return "Usage: cd <directory>"
        
        new_path = args[0]
        if new_path.startswith("/"):
            full_path = new_path
        else:
            full_path = f"{self.current_path.rstrip('/')}/{new_path}"

        if full_path in self.filesystem:
            self.current_path = full_path
            return ""
        return f"cd: {new_path}: No such file or directory"

    def _cat(self, args: List[str]) -> str:
        """Display file contents."""
        if not args:
            return "Usage: cat <file>"
        
        path = args[0]
        directory = "/".join(path.split("/")[:-1]) or self.current_path
        filename = path.split("/")[-1]

        if directory not in self.filesystem or filename not in self.filesystem[directory]:
            return f"cat: {path}: No such file or directory"

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
ls      - List directory contents
cd      - Change directory
cat     - Display file contents
pwd     - Print working directory
clear   - Clear screen
help    - Show this help message"""

    def _clear(self, args: List[str]) -> str:
        """Clear the screen."""
        self.effects.clear_screen()
        return ""

    def start_session(self):
        """Start an interactive session with the remote server."""
        self.effects.clear_screen()
        self.effects.type_text("\033[1;31m=== CONNECTING TO REMOTE SERVER ===\033[0m")
        self.effects.progress_bar(1, "Establishing secure connection")
        
        # ASCII art for old server
        server_art = """
        ===================
        |  OLD-SEC-SERVER |
        |  ============   |
        |  ||  ||  ||    |
        |  ||  ||  ||    |
        ===================
        """
        self.effects.type_text(server_art)
        self.effects.type_text("\033[1;32mConnection established. Use 'help' for available commands.\033[0m\n")
        return True

import random
import time
import datetime
from typing import List, Dict
from dataclasses import dataclass
from .terminal_effects import TerminalEffects

@dataclass
class FileNode:
    name: str
    content: str
    permissions: str = "rw-r--r--"
    created_date: str = "2024-12-01"
    modified_date: str = "2024-12-01"
    file_size: int = 0
    owner: str = "root"
    type: str = "txt"  # txt, log, bin, dat, etc.

class RemoteServer:
    def __init__(self):
        self.current_path = "/home"  # Changed from "/" to "/home"
        self.effects = TerminalEffects()

        # Initialize filesystem structure first
        self.filesystem = {}
        self._init_directory_structure()
        self._initialize_filesystem()

    def _init_directory_structure(self):
        """Initialize all directories with a more comprehensive structure"""
        directories = [
            # Root and core system directories
            "/",
            "/root",

            # Home directories
            "/home",
            "/home/admin",
            "/home/researcher",
            "/home/security",

            # System configuration and logs
            "/etc",
            "/var",
            "/var/log",
            "/var/tmp",

            # Research and classified areas
            "/research",
            "/research/logs",
            "/research/classified",
            "/research/data",

            # Security and sensitive areas
            "/secret",
            "/blackbox",
            "/devices",
            "/devices/terminals",
            "/security",

            # Temporary directories
            "/tmp"
        ]

        for directory in directories:
            # Ensure each directory is initialized in the filesystem
            if directory not in self.filesystem:
                self.filesystem[directory] = {}

    def _add_file(self, path: str, content: str, 
                  permissions: str = "rw-r--r--",
                  owner: str = "root", file_type: str = None):
        """
        Add a file to the filesystem with extended properties.

        Args:
            path: Full file path including filename
            content: Text content of the file
            permissions: Unix-style permission string
            owner: File owner username
            file_type: Optional file type override (default: derived from filename)
        """
        directory = "/".join(path.split("/")[:-1])
        if not directory:
            directory = "/"
        filename = path.split("/")[-1]

        # Auto-detect file type from extension if not provided
        if file_type is None:
            if "." in filename:
                file_type = filename.split(".")[-1]
            else:
                file_type = "txt"  # Default

        # Calculate a realistic file size
        file_size = len(content) + random.randint(10, 100)  # Add some variability

        # Generate creation and modified dates
        base_date = time.strftime('%Y-%m-%d')
        modified_offset = random.randint(0, 30)  # Days ago
        created_offset = random.randint(modified_offset, 60)  # Even earlier

        modified_date = (datetime.datetime.now() - 
                        datetime.timedelta(days=modified_offset)).strftime('%Y-%m-%d')
        created_date = (datetime.datetime.now() - 
                        datetime.timedelta(days=created_offset)).strftime('%Y-%m-%d')

        # Ensure the directory exists
        if directory not in self.filesystem:
            self.filesystem[directory] = {}

        # Create the file node with extended properties
        self.filesystem[directory][filename] = FileNode(
            name=filename,
            content=content,
            permissions=permissions,
            created_date=created_date,
            modified_date=modified_date,
            file_size=file_size,
            owner=owner,
            type=file_type
        )

    def add_file_series(self, base_path: str, prefix: str, 
                         contents: list):
        """
        Add a series of related files with incrementing numbers.

        Args:
            base_path: Base directory path
            prefix: Filename prefix
            contents: List of file contents
        """
        for i, content in enumerate(contents, 1):
            # Format with leading zeros: 001, 002, etc.
            file_num = f"{i:03d}"
            path = f"{base_path.rstrip('/')}/{prefix}_{file_num}.txt"
            self._add_file(path, content)

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
researcher:$6$another$different_hash:19432:0:99999:7:::""")

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

STATUS: CONTAINMENT BREACH IMMINENT""")

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

- Last transmission from Dr. Sarah Chen""")

        # Black box data
        self._add_file("/blackbox/data.bin", """
01010110 01001111 01001001 01000100 00100000
01000011 01001111 01001101 01001110 01000111 
00100000 01010100 01001000 01010010 01001111 
01010101 01000111 01001000""")

        self._add_file("/blackbox/README.txt", """
BLACK BOX SYSTEM - CLASSIFIED
Access Level: OMEGA

This system contains critical void containment data.
DO NOT ATTEMPT TO DECRYPT WITHOUT AUTHORIZATION.""")

        # Admin directory content
        self._add_file("/home/admin/access_log.txt", """
ACCESS LOG: ADMINISTRATOR
Date: 2024-12-22

Latest system access:
- Security clearance: OMEGA
- Access attempts: 7 (3 unauthorized)
- System modifications: Updated firewall rules, modified containment protocols

NOTE: Someone has been trying to access the main server. Check logs.
""")

        self._add_file("/home/admin/security_override.dat", """
SECURITY PROTOCOL OVERRIDE
Authorization: ADMIN LEVEL OMEGA

These protocols can be used to manually override containment field settings
in the event of primary system failure.

WARNING: Improper use may result in complete containment failure.
""")

        # Researcher directory content
        self._add_file("/home/researcher/experiment_log_042.txt", """
VOIDBORN Research Log - Experiment 042
Date: 2024-12-18
Researcher: Dr. Marcus Winters

SUBJECT: Void Entity Audio Response Testing

OBSERVATIONS:
- Entity responds to low frequency sounds (30-80 Hz)
- Entity retreats from high frequency sounds (15,000+ Hz)
- Entity became agitated when exposed to human speech recordings

ANALYSIS:
The void entity appears to have some form of audio sensory perception.
Its reactions suggest it may use sound waves for navigation or perception.

CONCLUSION:
We may be able to develop sonic barriers to contain the entities.

FOLLOW-UP:
Test different sound patterns to see if we can reliably repel the entities.

STATUS: ONGOING
""")

        self._add_file("/home/researcher/entity_profile.dat", """
ENTITY CLASSIFICATION: VOID SHADOW
Origin: Unknown dimension/reality
Composition: Non-baryonic matter with quantum field disruption properties

CAPABILITIES:
- Phase through conventional matter
- Absorb electromagnetic radiation
- Disrupt electrical systems
- Limited mimicry of observed entities
- Possible telepathic interference

WEAKNESSES:
- High-frequency sound waves
- Certain electromagnetic frequencies
- Quantum stabilized barrier fields

THREAT ASSESSMENT: EXTREME
""")

        # Security directory content
        self._add_file("/home/security/incident_report_17.txt", """
SECURITY INCIDENT REPORT: 17
Date: 2024-12-19
Officer: Lt. Sarah Chen
Clearance: BETA

INCIDENT TYPE: Containment Breach

DESCRIPTION:
At 0300 hours, a void entity breached containment in Sector 7. 
The breach occurred during power fluctuation caused by storm activity.
Two research assistants were present but escaped unharmed.

RESPONSE MEASURES:
- Emergency containment protocols activated
- Sector 7 locked down and evacuated
- Sonic barriers deployed
- Security team dispatched with prototype repulsion equipment

CURRENT STATUS:
Entity contained but still active within Sector 7.
Area remains under quarantine until further notice.

RECOMMENDATIONS:
Upgrade power backup systems. Current generators proved inadequate
during extended outages.
""")

        self._add_file("/home/security/containment_protocol_V7.dat", """
CONTAINMENT PROTOCOL: V7
Classification: OMEGA
Authorization: Security Level ALPHA Required

TARGET: Void Entities (All Classifications)

PROCEDURES:
1. Establish quantum stabilized barrier field
2. Deploy sonic emitters at 18,000 Hz
3. Activate electromagnetic pulse generators at specified frequencies
4. Monitor for reality fractures and seal immediately

EMERGENCY MEASURES:
In case of complete containment failure, initiate facility self-destruct
sequence. Authorization codes in secure vault.

NOTE: New entities appear more resistant to sonic deterrents.
""")

        self._add_file("/var/log/security_recent.log", """
[2024-12-22 03:14:22] [ALERT] Security breach detected in Sector 9
[2024-12-22 03:15:44] [WARNING] Unauthorized access attempt from 192.168.13.201
[2024-12-22 04:22:10] [CRITICAL] Containment failure in Sector 7 East Wing
[2024-12-22 06:45:33] [NOTICE] Security scan completed: Multiple anomalies detected
[2024-12-22 07:12:58] [ERROR] System BACKUP_GEN_3 failed security check
[2024-12-22 08:30:17] [INFO] Security patrol reported shadow movement in hallway B
""")

    def _normalize_path(self, path: str) -> str:
        """Convert any path to absolute path with optimized processing."""
        # Quick return for root
        if path == '/':
            return '/'

        # Handle relative paths
        if not path.startswith('/'):
            path = f"{self.current_path.rstrip('/')}/{path}"

        # Optimize common cases
        if '.' not in path:
            return path

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
            'dir': self._list_contents,  # Changed from 'list' to 'dir'
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
            output.append(f"<FILE>   {filename}")

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
        return file_node.content

    def _pwd(self, args: List[str]) -> str:
        """Print working directory."""
        return self.current_path

    def _help(self, args: List[str]) -> str:
        """Display help information."""
        return """Available commands:
dir     - List directory contents
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
        |  Voidborn Tech  |
        |  Main Labs Ser. |
        |  =============  |
        |   || || || ||   |
        |   || || || ||   |
        ===================
        """
        self.effects.type_text(server_art)
        self.effects.type_text("\033[1;32mConnection established. Starting in home directory. Type 'help' for available commands.\033[0m\n")
        return True
import random
import time
from typing import List

class LogGenerator:
    def __init__(self):
        self.ip_addresses = [
            "192.168.1.", "10.0.0.", "172.16.0.", "8.8.8.",
            "1.1.1.", "176.32.98.", "205.251.242.", "52.216.100."
        ]
        
        self.usernames = [
            "root", "admin", "system", "user", "guest",
            "postgres", "apache", "nginx", "service"
        ]
        
        self.processes = [
            "sshd", "httpd", "nginx", "mysql", "postgresql",
            "mongodb", "redis", "systemd", "cron"
        ]

    def generate_ip(self) -> str:
        """Generate a random IP address."""
        base = random.choice(self.ip_addresses)
        return f"{base}{random.randint(1, 254)}"

    def generate_port(self) -> int:
        """Generate a random port number."""
        return random.randint(1024, 65535)

    def generate_timestamp(self) -> str:
        """Generate a current timestamp."""
        return time.strftime('%Y-%m-%d %H:%M:%S')

    def generate_log(self) -> str:
        """Generate a realistic-looking log entry."""
        log_types = [
            lambda: f"[NETWORK] Connection attempt from {self.generate_ip()}:{self.generate_port()}",
            lambda: f"[FIREWALL] Blocked suspicious traffic from {self.generate_ip()}",
            lambda: f"[AUTH] Failed login attempt for user '{random.choice(self.usernames)}'",
            lambda: f"[SYSTEM] Process '{random.choice(self.processes)}' spawned with PID {random.randint(1000, 9999)}",
            lambda: f"[CRYPTO] Generating new {random.choice(['RSA', 'AES', 'ECC'])} key pair",
            lambda: f"[EXPLOIT] Buffer overflow attempt detected in {random.choice(self.processes)}",
            lambda: f"[SCAN] Port scan detected from {self.generate_ip()}",
            lambda: f"[ACCESS] Privilege escalation attempt detected for user '{random.choice(self.usernames)}'",
            lambda: f"[DATABASE] SQL injection attempt blocked from {self.generate_ip()}",
            lambda: f"[MALWARE] Suspicious file activity detected in /tmp/{random.randint(1000, 9999)}.exe"
        ]
        
        timestamp = self.generate_timestamp()
        log_entry = random.choice(log_types)()
        return f"{timestamp} {log_entry}"

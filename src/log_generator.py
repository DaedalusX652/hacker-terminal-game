import random
import time
from typing import List, Callable, Dict
from functools import lru_cache

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
        
        # Pre-generate some IP addresses for performance
        self._cached_ips = [self.generate_ip() for _ in range(20)]
        self._ip_index = 0

    def generate_ip(self) -> str:
        """Generate a random IP address."""
        # Use cached IPs with occasional regeneration for variation
        if random.random() > 0.7:  # 30% chance to generate new IP
            base = random.choice(self.ip_addresses)
            return f"{base}{random.randint(1, 254)}"
        else:
            # Use pre-generated IPs in a round-robin fashion
            ip = self._cached_ips[self._ip_index]
            self._ip_index = (self._ip_index + 1) % len(self._cached_ips)
            return ip

    @lru_cache(maxsize=16)
    def generate_port(self) -> int:
        """Generate a random port number."""
        return random.randint(1024, 65535)

    def generate_timestamp(self) -> str:
        """Generate a current timestamp."""
        return time.strftime('%Y-%m-%d %H:%M:%S')
        
    # Pre-define log type functions for better performance
    def _log_network(self) -> str:
        return f"[NETWORK] Connection attempt from {self.generate_ip()}:{self.generate_port()}"
        
    def _log_firewall(self) -> str:
        return f"[FIREWALL] Blocked suspicious traffic from {self.generate_ip()}"
        
    def _log_auth(self) -> str:
        return f"[AUTH] Failed login attempt for user '{random.choice(self.usernames)}'"
        
    def _log_system(self) -> str:
        return f"[SYSTEM] Process '{random.choice(self.processes)}' spawned with PID {random.randint(1000, 9999)}"
        
    def _log_crypto(self) -> str:
        return f"[CRYPTO] Generating new {random.choice(['RSA', 'AES', 'ECC'])} key pair"
        
    def _log_exploit(self) -> str:
        return f"[EXPLOIT] Buffer overflow attempt detected in {random.choice(self.processes)}"
        
    def _log_scan(self) -> str:
        return f"[SCAN] Port scan detected from {self.generate_ip()}"
        
    def _log_access(self) -> str:
        return f"[ACCESS] Privilege escalation attempt detected for user '{random.choice(self.usernames)}'"
        
    def _log_database(self) -> str:
        return f"[DATABASE] SQL injection attempt blocked from {self.generate_ip()}"
        
    def _log_malware(self) -> str:
        return f"[MALWARE] Suspicious file activity detected in /tmp/{random.randint(1000, 9999)}.exe"

    def generate_log(self) -> str:
        """Generate a realistic-looking log entry."""
        log_types = [
            self._log_network, self._log_firewall, self._log_auth, 
            self._log_system, self._log_crypto, self._log_exploit,
            self._log_scan, self._log_access, self._log_database,
            self._log_malware
        ]
        
        timestamp = self.generate_timestamp()
        log_entry = random.choice(log_types)()
        return f"{timestamp} {log_entry}"

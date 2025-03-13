
import hashlib
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from typing import Tuple, Union

class CryptoOperations:
    def __init__(self):
        self.key = self._generate_key()
        self.cipher = Fernet(self.key)
        
    @staticmethod
    def generate_key() -> bytes:
        """Generate a new Fernet encryption key."""
        return Fernet.generate_key()
        
    def _generate_key(self):
        """Generate a secure key for encryption/decryption."""
        # In a real application, this would be stored securely
        salt = b'game_salt_fixed'
        password = b'voidborn_secure_password'
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key
    
    def encrypt(self, data: str) -> str:
        """Encrypt a string and return the encrypted string."""
        if not data:
            return ""
        encrypted = self.cipher.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
        
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt an encrypted string."""
        if not encrypted_data:
            return ""
        try:
            data = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted = self.cipher.decrypt(data)
            return decrypted.decode()
        except Exception:
            return "[Decryption failed - Invalid data or key]"
    
    def encrypt_message(self, message: str, key: bytes) -> Tuple[bytes, bool]:
        """
        Encrypt a message using Fernet symmetric encryption.
        Returns tuple of (encrypted_message, success)
        """
        try:
            cipher = Fernet(key)
            return cipher.encrypt(message.encode()), True
        except Exception as e:
            print(f"\033[1;31mEncryption error: {str(e)}\033[0m")
            return b"", False

    def decrypt_message(self, encrypted_message: bytes, key: bytes) -> Tuple[str, bool]:
        """
        Decrypt a message using Fernet symmetric encryption.
        Returns tuple of (decrypted_message, success)
        """
        try:
            cipher = Fernet(key)
            decrypted = cipher.decrypt(encrypted_message)
            return decrypted.decode(), True
        except Exception as e:
            print(f"\033[1;31mDecryption error: {str(e)}\033[0m")
            return "", False

    def hash_password(self, password: str) -> str:
        """Create a secure hash of a password."""
        salt = os.urandom(16)
        hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return base64.b64encode(salt + hashed).decode()
        
    def verify_password(self, stored_hash: str, provided_password: str) -> bool:
        """Verify a password against its hash."""
        try:
            decoded = base64.b64decode(stored_hash)
            salt = decoded[:16]
            stored_password_hash = decoded[16:]
            hash_attempt = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 100000)
            return hash_attempt == stored_password_hash
        except Exception:
            return False
            
    @staticmethod
    def hash_data(data: str) -> str:
        """Generate SHA-256 hash of input data."""
        return hashlib.sha256(data.encode()).hexdigest()

    @staticmethod
    def generate_multiple_hashes(data: str) -> dict:
        """Generate multiple hash types for input data."""
        return {
            'md5': hashlib.md5(data.encode()).hexdigest(),
            'sha1': hashlib.sha1(data.encode()).hexdigest(), 
            'sha256': hashlib.sha256(data.encode()).hexdigest(),
            'sha512': hashlib.sha512(data.encode()).hexdigest()
        }

import hashlib
import base64
from cryptography.fernet import Fernet
from typing import Tuple, Union

class CryptoOperations:
    @staticmethod
    def generate_key() -> bytes:
        """Generate a new Fernet encryption key."""
        return Fernet.generate_key()

    @staticmethod
    def encrypt_message(message: str, key: bytes) -> Tuple[bytes, bool]:
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

    @staticmethod
    def decrypt_message(encrypted_message: bytes, key: bytes) -> Tuple[str, bool]:
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

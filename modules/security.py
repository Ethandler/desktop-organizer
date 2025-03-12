import hashlib
from cryptography.fernet import Fernet
from pathlib import Path
import getpass

class FileVault:
    def __init__(self):
        self.key_store = {}
        
    def generate_key(self, password: str) -> bytes:
        salt = hashlib.sha256(password.encode()).digest()
        key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return Fernet.generate_key()
    
    def encrypt_file(self, path: Path, password: str) -> None:
        key = self.generate_key(password)
        fernet = Fernet(key)
        
        with open(path, 'rb') as f:
            data = f.read()
            
        encrypted = fernet.encrypt(data)
        with open(path.with_suffix('.enc'), 'wb') as f:
            f.write(encrypted)
            
        path.unlink()
        self.key_store[path.name] = key
        
    def decrypt_file(self, path: Path, password: str) -> None:
        key = self.generate_key(password)
        fernet = Fernet(key)
        
        with open(path, 'rb') as f:
            data = f.read()
            
        decrypted = fernet.decrypt(data)
        original_path = path.with_suffix('')
        with open(original_path, 'wb') as f:
            f.write(decrypted)
            
        path.unlink()
        
    def is_encrypted(self, path: Path) -> bool:
        return path.suffix == '.enc'
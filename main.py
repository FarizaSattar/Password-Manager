from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import os

class PasswordManager:
    def __init__(self, key):
        self.key = key

    def pad(self, data):
        return data + b'\0' * (AES.block_size - len(data) % AES.block_size)

    def encrypt(self, raw):
        raw = self.pad(raw)
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(enc[AES.block_size:]))

    def unpad(self, data):
        return data.rstrip(b'\0')

    def store_password(self, service, username, password):
        encrypted_password = self.encrypt(password.encode('utf-8'))
        with open(f"{service}.txt", 'wb') as f:
            f.write(encrypted_password)
        print(f"Password for {service} stored successfully!")

    def retrieve_password(self, service):
        try:
            with open(f"{service}.txt", 'rb') as f:
                encrypted_password = f.read()
            password = self.decrypt(encrypted_password).decode('utf-8')
            return password
        except FileNotFoundError:
            return None

# Example usage
if __name__ == "__main__":
    key = os.urandom(32)  # 256-bit random key
    manager = PasswordManager(key)

    service = input("Enter service name: ")
    username = input("Enter username: ")
    password = input("Enter password: ")

    manager.store_password(service, username, password)
    retrieved_password = manager.retrieve_password(service)
    if retrieved_password:
        print(f"Retrieved password for {service}: {retrieved_password}")
    else:
        print(f"No password found for {service}")

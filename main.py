import sqlite3
from cryptography.fernet import Fernet
import os

# Generate and save a key for encryption
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Load the encryption key
def load_key():
    return open("secret.key", "rb").read()

# Encrypt the password
def encrypt_password(password, key):
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password

# Decrypt the password
def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password).decode()
    return decrypted_password

# Initialize the database
def init_db():
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS passwords
                 (id INTEGER PRIMARY KEY, service TEXT, encrypted_password BLOB)''')
    conn.commit()
    conn.close()

# Add a new password to the database
def add_password(service, password):
    key = load_key()
    encrypted_password = encrypt_password(password, key)
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute("INSERT INTO passwords (service, encrypted_password) VALUES (?, ?)", (service, encrypted_password))
    conn.commit()
    conn.close()

# Retrieve a password
def get_password(service):
    key = load_key()
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute("SELECT encrypted_password FROM passwords WHERE service=?", (service,))
    result = c.fetchone()
    conn.close()
    if result:
        return decrypt_password(result[0], key)
    else:
        return None

# Main application loop
def main():
    generate_key()
    init_db()

    while True:
        print("\nPassword Manager")
        print("1. Add a password")
        print("2. Get a password")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            service = input("Enter the service name: ")
            password = input("Enter the password: ")
            add_password(service, password)
            print(f"Password for {service} added.")

        elif choice == "2":
            service = input("Enter the service name: ")
            password = get_password(service)
            if password:
                print(f"Password for {service}: {password}")
            else:
                print(f"No password found for {service}.")

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

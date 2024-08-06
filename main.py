import sqlite3  # Import SQLite3 for database operations
from cryptography.fernet import Fernet  # Import Fernet for encryption and decryption
import os  # Import os for file operations

# Generate and save a key for encryption
def generate_key():
    key = Fernet.generate_key()  # Generate a new encryption key
    with open("secret.key", "wb") as key_file:  # Open a file to store the key
        key_file.write(key)  # Write the key to the file

# Load the encryption key from a file
def load_key():
    return open("secret.key", "rb").read()  # Read and return the encryption key from the file

# Encrypt the password using the provided encryption key
def encrypt_password(password, key):
    f = Fernet(key)  # Create a Fernet object with the encryption key
    encrypted_password = f.encrypt(password.encode())  # Encrypt the password
    return encrypted_password  # Return the encrypted password

# Decrypt the password using the provided encryption key
def decrypt_password(encrypted_password, key):
    f = Fernet(key)  # Create a Fernet object with the encryption key
    decrypted_password = f.decrypt(encrypted_password).decode()  # Decrypt the password
    return decrypted_password  # Return the decrypted password

# Initialize the database and create a table for storing passwords
def init_db():
    conn = sqlite3.connect('passwords.db')  # Connect to the SQLite database (or create it if it doesn't exist)
    c = conn.cursor()  # Create a cursor object to interact with the database
    c.execute('''CREATE TABLE IF NOT EXISTS passwords
                 (id INTEGER PRIMARY KEY, service TEXT, encrypted_password BLOB)''')  # Create a table for passwords
    conn.commit()  # Commit the transaction
    conn.close()  # Close the database connection

# Add a new password to the database
def add_password(service, password):
    key = load_key()  # Load the encryption key
    encrypted_password = encrypt_password(password, key)  # Encrypt the password
    conn = sqlite3.connect('passwords.db')  # Connect to the database
    c = conn.cursor()  # Create a cursor object
    c.execute("INSERT INTO passwords (service, encrypted_password) VALUES (?, ?)", (service, encrypted_password))  # Insert the service and encrypted password into the database
    conn.commit()  # Commit the transaction
    conn.close()  # Close the database connection

# Retrieve a password from the database
def get_password(service):
    key = load_key()  # Load the encryption key
    conn = sqlite3.connect('passwords.db')  # Connect to the database
    c = conn.cursor()  # Create a cursor object
    c.execute("SELECT encrypted_password FROM passwords WHERE service=?", (service,))  # Query for the encrypted password of the given service
    result = c.fetchone()  # Fetch the result
    conn.close()  # Close the database connection
    if result:
        return decrypt_password(result[0], key)  # Decrypt and return the password if found
    else:
        return None  # Return None if no password is found for the given service

# Main application loop
def main():
    generate_key()  # Generate and save a new encryption key (only run once in a real scenario)
    init_db()  # Initialize the database

    while True:
        # Display the menu options
        print("\nPassword Manager")
        print("1. Add a password")
        print("2. Get a password")
        print("3. Exit")
        choice = input("Enter your choice: ")  # Get user input

        if choice == "1":
            service = input("Enter the service name: ")  # Prompt for the service name
            password = input("Enter the password: ")  # Prompt for the password
            add_password(service, password)  # Add the password to the database
            print(f"Password for {service} added.")  # Confirm the addition

        elif choice == "2":
            service = input("Enter the service name: ")  # Prompt for the service name
            password = get_password(service)  # Retrieve the password from the database
            if password:
                print(f"Password for {service}: {password}")  # Display the retrieved password
            else:
                print(f"No password found for {service}.")  # Inform the user if no password is found

        elif choice == "3":
            print("Exiting...")  # Exit message
            break  # Exit the loop and end the program

        else:
            print("Invalid choice. Please try again.")  # Error message for invalid menu choice

if __name__ == "__main__":
    main()  # Run the main application loop

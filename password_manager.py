#!/usr/bin/env python3

import base64
import getpass
import os
import sys

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# --- Configuration ---
# Define constants for file names and cryptographic parameters.
# This makes the code cleaner and easier to modify.
SALT_FILE = "salt.bin"
PASSWORDS_FILE = "passwords.txt"
KDF_ITERATIONS = 480000  # Increased iterations for stronger key derivation.

# --- Key and Salt Management ---


def get_salt() -> bytes:
    """
    Retrieves the salt from SALT_FILE. If the file doesn't exist,
    it generates a new salt, saves it, and returns it. The salt is crucial
    for the key derivation process and is safe to store publicly.
    """
    if os.path.exists(SALT_FILE):
        with open(SALT_FILE, "rb") as f:
            return f.read()
    else:
        # Generate a new cryptographically secure random salt.
        salt = os.urandom(16)
        with open(SALT_FILE, "wb") as f:
            f.write(salt)
        print(f"New salt created and saved to {SALT_FILE}.")
        return salt


def derive_key(password: str, salt: bytes) -> bytes:
    """
    Derives a Fernet-compatible key from a master password and a salt using PBKDF2.
    PBKDF2 is a standard algorithm for securely deriving keys from passwords.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=KDF_ITERATIONS,
        backend=default_backend(),
    )
    # Fernet keys must be 32 url-safe base64-encoded bytes.
    return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))


# --- New First-Time Setup Function ---


def first_time_setup() -> str:
    """
    Guides the user through creating and confirming their master password
    for the first time. This is only run when passwords.txt is not found.
    """
    print("--- Welcome to Password Manager ---")
    print("This appears to be your first time running the program.")
    print("Please create a master password. This password will be used to encrypt")
    print("all your other passwords. DO NOT FORGET IT.\n")
    while True:
        # Prompt for new password using getpass to hide input.
        password = getpass.getpass("Create Master Password: ")
        if not password:
            print("Password cannot be empty. Please try again.")
            continue

        # Prompt for confirmation.
        confirm_password = getpass.getpass("Confirm Master Password: ")

        # Check if they match.
        if password == confirm_password:
            print("\nMaster password set successfully!")
            # Create the password file to mark setup as complete.
            with open(PASSWORDS_FILE, "w"):
                pass  # Just create an empty file.
            return password
        else:
            print("\nPasswords do not match. Please try again.")


# --- Core Password Management Functions ---


def view_passwords(fer: Fernet) -> None:
    """Decrypts and displays all stored passwords."""
    try:
        with open(PASSWORDS_FILE, "r") as f:
            print("-" * 40)
            lines = f.readlines()
            if not lines:
                print("No passwords found. Use 'add' to save one.")
            else:
                for line in lines:
                    data = line.rstrip()
                    if "|" not in data:
                        continue
                    user, pswd_encrypted = data.split("|", 1)
                    try:
                        # Decrypt the password. Use correct encoding.
                        pswd_decrypted = fer.decrypt(
                            pswd_encrypted.encode("utf-8")
                        ).decode("utf-8")
                        print(
                            f"Account: {user.strip():<20} | Password: {pswd_decrypted}"
                        )
                    except InvalidToken:
                        # This error occurs if the master password is wrong.
                        print(
                            f"Account: {user.strip():<20} | [DECRYPTION FAILED - WRONG MASTER PASSWORD?]"
                        )
            print("-" * 40)
    except FileNotFoundError:
        # This case should now only be hit if the file is deleted after setup.
        print("Password file not found. It may have been deleted.")


def add_password(fer: Fernet) -> None:
    """Prompts user for new credentials and saves them encrypted."""
    name = input("Account Name: ")
    # Use getpass to hide password input.
    pswd = getpass.getpass("Password: ")

    if not name or not pswd:
        print("Account name and password cannot be empty.")
        return

    with open(PASSWORDS_FILE, "a") as f:
        # Encrypt the password. Use correct encoding.
        encrypted_pswd = fer.encrypt(pswd.encode("utf-8")).decode("utf-8")
        f.write(f"{name} | {encrypted_pswd}\n")
    print(f"Password for '{name}' added successfully.")


def save_generated_password(ac: str, password: str, master_password: str) -> None:
    """
    Saves a password generated from the other script.
    This function handles its own key derivation.
    """
    salt = get_salt()
    key = derive_key(master_password, salt)
    fer = Fernet(key)

    name = ac or "Default"
    with open(PASSWORDS_FILE, "a") as f:
        encrypted_pswd = fer.encrypt(password.encode("utf-8")).decode("utf-8")
        f.write(f"{name} | {encrypted_pswd}\n")


# --- Main Application Logic ---


def main() -> None:
    """Main loop for the interactive password manager."""
    try:
        salt = get_salt()

        # Check if this is the first run by looking for the passwords file.
        if not os.path.exists(PASSWORDS_FILE):
            master_password = first_time_setup()
        else:
            # If not the first run, just ask for the password.
            master_password = getpass.getpass("Please enter your master password: ")

        if not master_password:
            print("Master password cannot be empty.", file=sys.stderr)
            sys.exit(1)

        key = derive_key(master_password, salt)
        fer = Fernet(key)

        print("\nWelcome!")

    except Exception as e:
        print(f"An error occurred during setup: {e}", file=sys.stderr)
        sys.exit(1)

    while True:
        try:
            mode = (
                input("\nChoose an option: [V]iew, [A]dd, [Q]uit\n> ").lower().strip()
            )
            if mode in ("q", "quit"):
                break
            elif mode in ("v", "view"):
                view_passwords(fer)
            elif mode in ("a", "add"):
                add_password(fer)
            else:
                print("Invalid option, please try again.")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)
            break


if __name__ == "__main__":
    main()

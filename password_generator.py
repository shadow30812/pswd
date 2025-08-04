#!/usr/bin/env python3

import argparse
import getpass
import secrets
import string
import sys

# Import the specific function needed to save the password.
# This avoids running the main loop of the manager.
from password_manager import save_generated_password


def gen_pswd(length: int, numbers: bool, specials: bool) -> str:
    """
    Generates a cryptographically strong password using the 'secrets' module.
    This approach ensures that each required character type is included,
    then fills the rest and shuffles for randomness.
    """
    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation

    # Start with a guaranteed character from each required set.
    password_parts = []
    all_chars = letters
    password_parts.append(
        secrets.choice(letters)
    )  # Passwords will always have letters.

    if numbers:
        password_parts.append(secrets.choice(digits))
        all_chars += digits
    if specials:
        password_parts.append(secrets.choice(special_chars))
        all_chars += special_chars

    # Fill the rest of the password length with characters from the full set.
    remaining_len = length - len(password_parts)
    for _ in range(remaining_len):
        password_parts.append(secrets.choice(all_chars))

    # Shuffle the list to ensure character positions are random.
    secrets.SystemRandom().shuffle(password_parts)

    return "".join(password_parts)


def prompt_to_save_pswd(password: str) -> None:
    """Asks the user if they want to save the generated password and handles the process."""
    while True:
        choice = (
            input("Would you like to save this password? (yes/no): ").lower().strip()
        )
        if choice in ("yes", "y"):
            ac = input("Enter an account name (or press Enter for 'Default'): ").strip()
            if not ac:
                ac = "Default"
            try:
                # Prompt for master password to encrypt and save the new password.
                master_password = getpass.getpass(
                    "Enter your master password to save: "
                )
                if not master_password:
                    print("Master password cannot be empty. Password not saved.")
                    return

                save_generated_password(ac, password, master_password)
                print(f"Password saved for account '{ac}'.")
            except Exception as e:
                print(f"An error occurred while saving: {e}", file=sys.stderr)
            break
        elif choice in ("no", "n"):
            print("Password not saved.")
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


def main():
    """Main function to parse arguments and generate a password."""
    # Use argparse for robust and user-friendly command-line argument parsing.
    parser = argparse.ArgumentParser(
        description="A secure password generator.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "length", type=int, help="The desired length of the password (e.g., 16)."
    )
    parser.add_argument(
        "--no-numbers",
        action="store_false",
        dest="numbers",
        help="Exclude numbers from the password.",
    )
    parser.add_argument(
        "--no-specials",
        action="store_false",
        dest="specials",
        help="Exclude special characters (e.g., !@#$) from the password.",
    )

    args = parser.parse_args()

    if args.length < 4:
        print("Error: Password length must be at least 4.", file=sys.stderr)
        sys.exit(1)

    try:
        # Generate the password with the specified criteria.
        password = gen_pswd(
            length=args.length, numbers=args.numbers, specials=args.specials
        )
        print("\nGenerated Password:")
        print(password)
        print()  # Add a newline for better formatting.

        # Ask the user if they want to save the password.
        prompt_to_save_pswd(password)

    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

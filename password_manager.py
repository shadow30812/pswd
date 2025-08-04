#!/usr/bin/env python3
from io import BufferedReader

from cryptography.fernet import Fernet

# # Uncomment the following lines when running the program for the first time
# def write_key():
#     key = Fernet.generate_key()
#     with open("key.key", "wb") as key_file:
#         key_file.write(key)
# write_key()


# Comment the following lines for the first use, and uncomment after
def load_key() -> bytes:
    file: BufferedReader = open("key.key", "rb")
    key: bytes = file.read()
    file.close()
    return key


def view() -> None:
    with open("passwords.txt", "r") as f:
        for line in f.readlines():
            data: str = line.rstrip()
            datasets: list[str] = data.split("|")
            user, pswd = datasets
            print("User:", user, "| Password:", fer.decrypt((pswd.encode()).decode()))


def add() -> None:
    name: str = input("A/c name:")
    pswd: str = input("Password:")

    with open("passwords.txt", "a") as f:
        f.write(name + " | " + fer.encrypt(pswd.encode()).decode() + "\n")


def main() -> None:
    while True:
        try:
            mode: str = input("View / Add passwords?\t")
            if mode.lower() == "quit":
                break
            elif mode.lower() == "view":
                view()
            elif mode.lower() == "add":
                add()
            else:
                print("Wrong option, please retry...")
                continue
        except KeyboardInterrupt:
            print("Interrupted by Keyboard input, exiting...")
            break
        except EOFError:
            print("Interrupted by End of File stream, exiting...")
            break
        except Exception:
            print("An unknown exception occurred. Please try again later.")
            break


if __name__ == "__main__":
    key: bytes = load_key()
    fer: Fernet = Fernet(key)
    main()


def gen_save(ac: str, password: str) -> None:
    key: bytes = load_key()
    fer: Fernet = Fernet(key)

    name: str = ac or "User"
    pswd: str = password

    with open("passwords.txt", "a") as f:
        f.write(name + " | " + fer.encrypt(pswd.encode()).decode() + "\n")

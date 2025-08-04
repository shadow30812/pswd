#!/usr/bin/env python3

import random
import string
import sys
from typing import LiteralString

from password_manager import gen_save

MAX_LEN: int = sys.maxsize


def gen_pswd(
    min_len: int, numbers_needed: bool = True, specials_needed: bool = True
) -> str:
    letters: LiteralString = string.ascii_letters
    digits: LiteralString = string.digits
    specials: LiteralString = string.punctuation

    valid_characters: str = letters
    if numbers_needed:
        valid_characters += digits
    if specials_needed:
        valid_characters += specials

    pswd: str = ""
    meets_criteria: bool = False
    has_number: bool = False
    has_special: bool = False

    while not meets_criteria or len(pswd) < min_len:
        new_char: str = random.choice(valid_characters)
        pswd += new_char

        if new_char in digits:
            has_number = True
        if new_char in specials:
            has_special = True

        if len(pswd) >= min_len and len(pswd) < MAX_LEN:
            meets_criteria = True
            if numbers_needed:
                meets_criteria = has_number
            if specials_needed:
                meets_criteria = meets_criteria and has_special

    return pswd


def save_pswd(password: str) -> None:
    print("Would you like to save the password?")
    choice: str = input("Yes/No")
    if choice.lower() == "yes":
        ac: str = input("Would you like an a/c name? Press Enter for User (default).")
        try:
            gen_save(ac, password)
        except ChildProcessError:
            print(
                "Critical error encountered, stopping the program to prevent memory leaks."
            )
            sys.exit(43)
        except (KeyboardInterrupt, EOFError) as K:
            print(K)
            sys.exit(-1)
        except Exception as e:
            print("An error occurred, please try again later.")
            print(e)
            sys.exit(1)
    else:
        pass


if __name__ == "__main__":
    args: list[str] = sys.argv[1:]
    num: int = len(args)
    if num == 1:
        arg0: int = int(args[0])
        password: str = gen_pswd(min_len=arg0)
    elif num == 2:
        arg0: int = int(args[0])
        arg1: bool = args[1] == "True"
        password = gen_pswd(min_len=arg0, numbers_needed=arg1)
    elif num == 3:
        arg0: int = int(args[0])
        arg1: bool = args[1] == "True"
        arg2: bool = args[2] == "True"
        password = gen_pswd(min_len=arg0, numbers_needed=arg1, specials_needed=arg2)
    else:
        print("Wrong number of inputs")
        sys.exit(2)
    print(password)

    save_pswd(password)
    sys.exit(0)

from hash_password import hash_password
from colorama import Fore,Back,Style

def login(username,password):
    password = hash_password(password)
    with open("users.txt", "r") as file:
        for line in file:
            stored_username, stored_password = line.strip().split(":")
            if username == stored_username and password == stored_password:
                print(Fore.GREEN + "Successful login.")
                print(Style.RESET_ALL)
                return True

    print(Fore.RED + "Name or username incorrect.")
    print(Style.RESET_ALL)
    return False

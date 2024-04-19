def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    with open("users.txt", "r") as file:
        for line in file:
            stored_username, stored_password = line.strip().split(":")
            if username == stored_username and password == stored_password:
                print("Successful login.")
                return True

    print("Name or username incorrect.")
    return False

def register():
    username = input("Enter username: ")
    password = input("Enter password: ")

    with open("users.txt", "a") as file:
        file.write(f"{username}:{password}\n")

    print("Successful registration.")



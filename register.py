from hash_password import hash_password
def register():
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    hashed_pwd = hash_password(password)
    with open("users.txt", "a") as file:
        file.write(f"{username}:{hashed_pwd}\n")

    print("Successful registration.")



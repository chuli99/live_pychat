
def save_message(msg,rm):
    room = (f"{rm}.txt")
    with open(room,"a") as file:
        file.write(f"{msg}\n")
    
def read_messages(rm):
    room = (f"{rm}.txt")
    with open(room,"r") as file:
        lines = file.readlines()
    return lines
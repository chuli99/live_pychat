import datetime

def save_message(msg,rm):
    room = (f"{rm}.txt")
    today = datetime.date.today()
    with open(room,"a") as file:
        file.write(f"({today}){msg}\n")

def read_messages(rm):
    room = (f"{rm}.txt")
    try: 
        with open(room,"r") as file:
            lines = file.readlines()
            return lines
    except:
        return "missing file"
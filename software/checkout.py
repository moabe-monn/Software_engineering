# checkout.py
import json

DATA_FILE = "data.json"

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(d):
    with open(DATA_FILE, "w") as f:
        json.dump(d, f, indent=2)

def check_out(room_number):
    d = load_data()
    # room_number を持つ reservation を検索
    for res_id, info in d["reservations"].items():
        if info.get("room_number") == room_number:
            # 削除または状態更新
            del d["reservations"][res_id]
            save_data(d)
            print("Check-out has been completed.")
            return True
    print("Room number not found.")
    return False

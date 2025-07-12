# checkin.py
import json
import random

DATA_FILE = "data.json"

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(d):
    with open(DATA_FILE, "w") as f:
        json.dump(d, f, indent=2)

def check_in(res_id):
    d = load_data()
    if res_id not in d["reservations"]:
        print("Reservation not found.")
        return None
    info = d["reservations"][res_id]
    if info["checked_in"]:
        print("Already checked in.")
        return info["room_number"]
    # ルーム番号を自動生成（例: 100〜199 のランダム）
    room_number = str(random.randint(100, 999))
    info["checked_in"] = True
    info["room_number"] = room_number
    save_data(d)
    print("Check-in has been completed.")
    print(f"Room number is {room_number}.")
    return room_number

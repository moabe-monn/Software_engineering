# checkin.py
import json
import random

DATA_FILE = "data.json"

# 部屋タイプごとにルーム番号の範囲を定義
ROOM_RANGES = {
    "Single": (101, 102),
    "Double": (201, 299),
    "Twin":   (301, 399),
    "Deluxe": (401, 499),
    "Suite":  (501, 599),
}

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(d):
    with open(DATA_FILE, "w") as f:
        json.dump(d, f, indent=2)

def check_in(res_id, name, phone_number):
    d = load_data()
    # 予約が存在するか
    if res_id not in d.get("reservations", {}):
        print("Reservation not found.")
        return None
    info = d["reservations"][res_id]

    # 名前の照合
    if info.get("name") != name:
        print("Reservation name does not match.")
        return None

    # 電話番号の照合（予約時に未登録の場合はスキップ）
    if info.get("phone_number") and info.get("phone_number") != phone_number:
        print("Reservation phone number does not match.")
        return None

    # 既にチェックイン済みならルーム番号を返す
    if info.get("checked_in"):
        print("Already checked in.")
        return info.get("room_number")

    # ルーム番号を部屋タイプごとの範囲内で自動生成
    room_type = info.get("room")
    rmin, rmax = ROOM_RANGES.get(room_type, (100, 999))
    room_number = str(random.randint(rmin, rmax))

    # データ更新
    info["checked_in"] = True
    info["room_number"]  = room_number
    info["phone_number"] = phone_number
    save_data(d)

    # 完了メッセージ
    print("Check-in has been completed.")
    print(f"Room number is {room_number}.")
    return room_number
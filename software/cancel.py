# cancel.py
import json

DATA_FILE = "data.json"

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def cancel_reservation(res_id):
    """
    res_id: str -- 予約ID
    戻り値: True=キャンセル成功, False=見つからず
    """
    data = load_data()
    if res_id not in data["reservations"]:
        return False

    # キャンセル（データ削除）
    del data["reservations"][res_id]
    save_data(data)
    return True

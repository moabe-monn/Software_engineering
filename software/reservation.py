#!/usr/bin/env python3
import json
import uuid
from datetime import datetime, date

# データファイル
DATA_FILE = "data.json"

# 部屋タイプごとの部屋番号レンジ設定
ROOM_RANGES = {
    "Single": (101, 199),
    "Double": (201, 299),
    "Twin":   (301, 399),
    "Deluxe": (401, 499),
    "Suite":  (501, 599),
}



def load_data():
    """
    データファイルからJSONを読み込んで返す
    """
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    """
    JSONデータをデータファイルに保存する
    """
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def assign_room_number(room_type: str, data: dict, new_checkin: date, new_checkout: date) -> int:
    """
    指定された部屋タイプの空き部屋番号を範囲内から割り当てる。
    既存予約と日付が重複しない部屋を選定。
    空きがなければ None を返す

    new_checkin: チェックイン日
    new_checkout: チェックアウト日（滞在最終日の翌日）
    """
    start, end = ROOM_RANGES.get(room_type, (0, -1))
    used = set()
    # 既存予約をチェック
    for info in data.get("reservations", {}).values():
        room_no = info.get("room_number")
        if not room_no:
            continue
        existing_ci = datetime.strptime(info["checkin"], "%Y/%m/%d").date()
        existing_co = datetime.strptime(info["checkout"], "%Y/%m/%d").date()
        # 重複判定: [new_ci, new_co) と [existing_ci, existing_co) が重なる場合
        if not (new_checkout <= existing_ci or new_checkin >= existing_co):
            used.add(int(room_no))
    # 空き部屋を探索
    for num in range(start, end + 1):
        if num not in used:
            return num
    return None


def make_reservation(room: str, guests: int, name: str, checkin: date, checkout: date) -> str:
    """
    新規予約を作成し、予約IDを返す。

    指定日の重複をチェックして部屋番号を割り当て、
    満室の場合は例外を発生させる
    """
    data = load_data()

    # 部屋番号を割り当て（重複判定を含む）
    room_number = assign_room_number(room, data, checkin, checkout)
    if room_number is None:
        raise RuntimeError(f"No rooms available for type {room} on {checkin.strftime('%Y/%m/%d')} to {checkout.strftime('%Y/%m/%d')}.")

    res_id = uuid.uuid4().hex[:12]

    reservation = {
        "name":       name,
        "room":       room,
        "guests":     guests,
        "checkin":    checkin.strftime("%Y/%m/%d"),
        "checkout":   checkout.strftime("%Y/%m/%d"),
        "checked_in": False,
        "room_number": str(room_number)
    }

    data.setdefault("reservations", {})[res_id] = reservation
    save_data(data)
    return res_id


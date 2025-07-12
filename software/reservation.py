#!/usr/bin/env python3
import json
import uuid
from datetime import datetime

DATA_FILE = "data.json"

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def make_reservation(room, guests, checkin, checkout):
    """
    room:     str         -- 部屋タイプ
    guests:   int         -- 人数
    checkin:  date object -- チェックイン日
    checkout: date object -- チェックアウト日
    """
    data = load_data()
    # 12桁の予約IDを生成
    res_id = uuid.uuid4().hex[:12]
    data["reservations"][res_id] = {
        "room":       room,
        "guests":     guests,
        "checkin":    checkin.strftime("%Y/%m/%d"),
        "checkout":   checkout.strftime("%Y/%m/%d"),
        "checked_in": False,
        "room_number": None
    }
    save_data(data)
    return res_id

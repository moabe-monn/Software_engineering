#!/usr/bin/env python3
import json
import uuid
from datetime import datetime

DATA_FILE = "data.json"


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


def make_reservation(room: str, guests: int, name: str, checkin: datetime, checkout: datetime) -> str:
    """
    新規予約を作成し、予約IDを返す

    Parameters:
    - room:     str       -- 部屋タイプ
    - guests:   int       -- 人数
    - name:     str       -- 予約者名
    - checkin:  datetime  -- チェックイン日
    - checkout: datetime  -- チェックアウト日

    Returns:
    - str: 生成した予約ID
    """
    # 既存データ読み込み
    data = load_data()

    # 12桁の予約IDを生成
    res_id = uuid.uuid4().hex[:12]

    # 予約データを構築
    reservation = {
        "name":       name,
        "room":       room,
        "guests":     guests,
        "checkin":    checkin.strftime("%Y/%m/%d"),
        "checkout":   checkout.strftime("%Y/%m/%d"),
        "checked_in": False,
        "room_number": None
    }

    # データに追加
    data.setdefault("reservations", {})[res_id] = reservation

    # ファイルに保存
    save_data(data)

    return res_id

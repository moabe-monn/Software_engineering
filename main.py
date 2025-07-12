#!/usr/bin/env python3
import sys
import json
from datetime import datetime
from reservation import make_reservation
from checkin import check_in
from checkout import check_out
from datetime import datetime, date
from cancel import cancel_reservation

DATA_FILE = "data.json"

ROOM_TYPES = ["Single", "Double", "Twin", "Deluxe", "Suite"]

def input_room_type():
    print("Input room type (Single, Double, Twin, Deluxe, Suite)")
    rt = input("> ").strip().title()
    if rt not in ROOM_TYPES:
        print("Invalid room type.")
        return None
    return rt

def input_num_guests(room_type):
    print("Input number of guests")
    try:
        n = int(input("> ").strip())
    except ValueError:
        print("Invalid number.")
        return None
    if room_type == "Single" and n != 1:
        print("Error: Single room can accommodate only 1 guest.")
        return None
    else:
        if n < 1 or n > 4:
            print("Error: {} room can have up to 4 guests.".format(room_type))
            return None
    return n

def input_date(prompt):
    print(f"Input {prompt} date in the form of yyyy/MM/dd")
    s = input("> ").strip()
    try:
        return datetime.strptime(s, "%Y/%m/%d").date()
    except ValueError:
        print(f"Invalid {prompt} date.")
        return None

def handle_reservation():
    room = input_room_type()
    if not room:
        return

    guests = input_num_guests(room)
    if guests is None:
        return

    # --- チェックイン日入力（再入力ループ）---
    today = date.today()
    while True:
        checkin = input_date("check-in")
        if checkin is None:
            # parse エラーなら再入力
            continue
        if checkin < today:
            print("Invalid check-in date. Must be today or later.")
            continue
        break

    # --- チェックアウト日入力（再入力ループ）---
    while True:
        checkout = input_date("check-out")
        if checkout is None:
            # parse エラーなら再入力
            continue
        if checkout <= checkin:
            print("Invalid check-out date. Must be after check-in.")
            continue
        break

    # --- 予約実行＆完了メッセージ ---
    res_id = make_reservation(room, guests, checkin, checkout)
    print("\nReservation has been completed.")
    print(f"Arrival (staying) date is {checkin.strftime('%Y/%m/%d')}.")
    print(f"The checkout date will be {checkout.strftime('%Y/%m/%d')}.")
    print(f"Reservation number is {res_id}.")

def handle_checkin():
    res_id = input("Input reservation number\n> ").strip()
    if res_id:
        check_in(res_id)
    else:
        print("Invalid reservation number.")

def handle_checkout():
    room_number = input("Input room number\n> ").strip()
    if room_number:
        check_out(room_number)
    else:
        print("Invalid room number.")

def handle_cancel():
    # 1) 予約番号入力
    res_id = input("Input reservation number\n> ").strip()
    if not res_id:
        print("Invalid reservation number.")
        return

    # 2) まず data.json から存在チェック
    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    if res_id not in data.get("reservations", {}):
        print("Reservation not found.")
        return

    # 3) 存在したら確認を取る
    yn = input("Would you like to cancel? (y/n)\n> ").strip().lower()
    if yn != "y":
        print("Cancellation aborted.")
        return

    # 4) キャンセル実行
    success = cancel_reservation(res_id)
    if success:
        print("\nCancel Reservation has been completed.")
    else:
        # 実際にはここにはこないはずですが…念のため
        print("Reservation not found.")


def main():
    while True:
        print("\nMenu")
        print("1: Reservation")
        print("2: Check-in")
        print("3: Check-out")
        print("4: Cancel Reservation")    # ← 追加
        print("5: End")
        sel = input("> ").strip()

        if sel == "1":
            handle_reservation()
        elif sel == "2":
            handle_checkin()
        elif sel == "3":
            handle_checkout()
        elif sel == "4":                 
            handle_cancel()              
        elif sel == "5":
            print("Ended")
            sys.exit(0)
        else:
            print("Invalid selection.")


if __name__ == "__main__":
    main()

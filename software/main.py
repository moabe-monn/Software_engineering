#!/usr/bin/env python3
import sys
import json
from datetime import datetime, date
from reservation import make_reservation
from checkin import check_in
from checkout import check_out
from cancel import cancel_reservation

DATA_FILE = "data.json"

ROOM_TYPES = ["Single", "Double", "Twin", "Deluxe", "Suite"]

# １泊あたりの料金マップ
PRICES = {
    "Single":  8000,
    "Double": 20000,
    "Twin":   25000,
    "Deluxe":100000,
    "Suite": 200000,
}

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
    if room_type == "Single":
        if n != 1:
            print("Error: Single room can accommodate only 1 guest.")
            return None
    else:
        if n < 1 or n > 4:
            print(f"Error: {room_type} room can have up to 4 guests.")
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

    name = input("Input guest name\n> ").strip()
    if not name:
        print("Invalid name.")
        return
    
    phone = input("Input phone number\n> ").strip()
    if not phone:
        print("Invalid phone number.")
        return

    # チェックイン日入力
    today = date.today()
    while True:
        checkin = input_date("check-in")
        if checkin is None:
            continue
        if checkin < today:
            print("Invalid check-in date. Must be today or later.")
            continue
        break

    # チェックアウト日入力
    while True:
        checkout = input_date("check-out")
        if checkout is None:
            continue
        if checkout <= checkin:
            print("Invalid check-out date. Must be after check-in.")
            continue
        break

    # 宿泊日数と料金計算
    nights = (checkout - checkin).days
    cost = PRICES.get(room, 0) * nights

    # 予約登録：部屋満室時にエラーをキャッチ
    try:
        res_id = make_reservation(room, guests, name, checkin, checkout)
    except RuntimeError as e:
        print(e)
        return

    # 完了メッセージ
    print("\nReservation has been completed.")
    print(f"Arrival (staying) date is {checkin.strftime('%Y/%m/%d')}." )
    print(f"The checkout date will be {checkout.strftime('%Y/%m/%d')}." )
    print(f"The cost will be ￥{cost:,}")
    print(f"Reservation number is {res_id}.")


def handle_checkin():
    res_id = input("Input reservation number\n> ").strip()
    name = input("Input guest name\n> ").strip()
    phone  = input("Input phone number\n> ").strip()
    if res_id and name:
        check_in(res_id, name, phone)
    else:
        print("Invalid reservation number, name or phone.")


def handle_checkout():
    room_number = input("Input room number\n> ").strip()
    if not room_number:
        print("Invalid room number.")
        return

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    reservation = None
    for res_id, info in data.get("reservations", {}).items():
        if info.get("room_number") == room_number:
            reservation = {"id": res_id, **info}
            break

    if not reservation:
        print("Room number not found.")
        return

    checkout_str = reservation["checkout"]
    checkin_date  = datetime.strptime(reservation["checkin"], "%Y/%m/%d").date()
    checkout_date = datetime.strptime(checkout_str, "%Y/%m/%d").date()
    nights = (checkout_date - checkin_date).days
    cost   = PRICES.get(reservation["room"], 0) * nights

    success = check_out(room_number)
    if not success:
        return

    print(f"Checked out date is {checkout_str}.")
    print(f"You stayed {nights} night(s)." )
    print(f"Total cost was ￥{cost:,}." )


def handle_cancel():
    res_id = input("Input reservation number\n> ").strip()
    if not res_id:
        print("Invalid reservation number.")
        return

    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    if res_id not in data.get("reservations", {}):
        print("Reservation not found.")
        return

    yn = input("Would you like to cancel? (y/n)\n> ").strip().lower()
    if yn != "y":
        print("Cancellation aborted.")
        return

    success = cancel_reservation(res_id)
    if success:
        print("\nCancel Reservation has been completed.")
    else:
        print("Reservation not found.")


def main():
    while True:
        print("\nMenu")
        print("1: Reservation")
        print("2: Check-in")
        print("3: Check-out")
        print("4: Cancel Reservation")
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
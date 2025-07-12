# app_tui.py
from prompt_toolkit.shortcuts import button_dialog, input_dialog, message_dialog
from datetime import datetime
import requests

API = "http://127.0.0.1:8000"

def do_reservation():
    room = input_dialog(
        title="Reservation",
        text="Room type (Single, Double, Twin, Deluxe, Suite):"
    ).run()
    if not room:
        return

    guests = input_dialog(
        title="Reservation",
        text="Number of guests:"
    ).run()
    try:
        guests = int(guests)
    except:
        message_dialog(title="Error", text="Invalid number").run()
        return

    checkin = input_dialog(
        title="Reservation",
        text="Check-in date (YYYY-MM-DD):"
    ).run()
    checkout = input_dialog(
        title="Reservation",
        text="Check-out date (YYYY-MM-DD):"
    ).run()

    # APIコール
    resp = requests.post(f"{API}/reservations", json={
        "room": room,
        "guests": guests,
        "checkin": checkin,
        "checkout": checkout
    })
    if resp.status_code == 200:
        rid = resp.json()["reservation_id"]
        message_dialog(title="Success", text=f"Reservation ID:\n{rid}").run()
    else:
        message_dialog(title="Error", text=resp.json().get("detail", resp.text)).run()

def do_checkin():
    rid = input_dialog(title="Check-in", text="Reservation ID:").run()
    if not rid: return
    resp = requests.post(f"{API}/checkin/{rid}")
    if resp.status_code == 200:
        data = resp.json()
        message_dialog(title="Checked In", text=f"Room Number: {data['room_number']}").run()
    else:
        message_dialog(title="Error", text=resp.json().get("detail", resp.text)).run()

def do_checkout():
    room = input_dialog(title="Check-out", text="Room Number:").run()
    if not room: return
    resp = requests.post(f"{API}/checkout/{room}")
    if resp.status_code == 200:
        message_dialog(title="Checked Out", text="Check-out completed.").run()
    else:
        message_dialog(title="Error", text=resp.json().get("detail", resp.text)).run()

def do_cancel():
    rid = input_dialog(title="Cancel", text="Reservation ID:").run()
    if not rid: return
    # まず存在確認
    confirm = button_dialog(
        title="Cancel",
        text="Would you like to cancel?",
        buttons=[("Yes","y"),("No","n")]
    ).run()
    if confirm != "y":
        return
    resp = requests.delete(f"{API}/reservations/{rid}?confirm=true")
    if resp.status_code == 200:
        message_dialog(title="Cancelled", text="Reservation has been cancelled.").run()
    else:
        message_dialog(title="Error", text=resp.json().get("detail", resp.text)).run()

def main():
    while True:
        action = button_dialog(
            title="Menu",
            text="Select an action:",
            buttons=[
                ("Reservation", "res"),
                ("Check-in",    "in"),
                ("Check-out",   "out"),
                ("Cancel",      "can"),
                ("Exit",        "exit"),
            ]
        ).run()

        if action == "res":
            do_reservation()
        elif action == "in":
            do_checkin()
        elif action == "out":
            do_checkout()
        elif action == "can":
            do_cancel()
        else:
            break

if __name__ == "__main__":
    main()

# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import date
import json, uuid, random, string

DATA_FILE = "data.json"

# Models
class ReservationRequest(BaseModel):
    room: str = Field(..., description="Room type: Single, Double, Twin, Deluxe, Suite")
    guests: int = Field(..., description="Number of guests")
    checkin: date
    checkout: date

class CancelRequest(BaseModel):
    confirm: bool = Field(..., description="True to confirm cancellation")

# Utilities
def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# FastAPI app
app = FastAPI(title="Hotel Reservation API")

@app.on_event("startup")
def ensure_data_file():
    try:
        with open(DATA_FILE, "r"):
            pass
    except FileNotFoundError:
        save_data({"reservations": {}})

@app.post("/reservations")
def create_reservation(req: ReservationRequest):
    # Validate room type
    ROOM_TYPES = ["Single", "Double", "Twin", "Deluxe", "Suite"]
    if req.room not in ROOM_TYPES:
        raise HTTPException(status_code=400, detail="Invalid room type")
    # Validate guests
    if req.room == "Single" and req.guests != 1:
        raise HTTPException(status_code=400, detail="Single room can only have 1 guest")
    if req.room != "Single" and (req.guests < 1 or req.guests > 4):
        raise HTTPException(status_code=400, detail="Room can have up to 4 guests")
    # Validate dates
    today = date.today()
    if req.checkin < today:
        raise HTTPException(status_code=400, detail="Check-in must be today or later")
    if req.checkout <= req.checkin:
        raise HTTPException(status_code=400, detail="Check-out must be after check-in")

    # Generate ID
    alphabet = string.ascii_uppercase + string.digits
    res_id = ''.join(random.choices(alphabet, k=8))
    data = load_data()
    data["reservations"][res_id] = {
        "room": req.room,
        "guests": req.guests,
        "checkin": req.checkin.strftime("%Y/%m/%d"),
        "checkout": req.checkout.strftime("%Y/%m/%d"),
        "checked_in": False,
        "room_number": None
    }
    save_data(data)
    return {"reservation_id": res_id}

@app.post("/checkin/{res_id}")
def check_in(res_id: str):
    data = load_data()
    info = data["reservations"].get(res_id)
    if not info:
        raise HTTPException(status_code=404, detail="Reservation not found")
    if info["checked_in"]:
        return {"room_number": info["room_number"], "status": "already checked in"}
    room_number = str(random.randint(100, 199))
    info["checked_in"] = True
    info["room_number"] = room_number
    save_data(data)
    return {"room_number": room_number, "status": "checked in"}

@app.post("/checkout/{room_number}")
def check_out(room_number: str):
    data = load_data()
    for res_id, info in list(data["reservations"].items()):
        if info.get("room_number") == room_number:
            del data["reservations"][res_id]
            save_data(data)
            return {"status": "checked out"}
    raise HTTPException(status_code=404, detail="Room number not found")

@app.delete("/reservations/{res_id}")
def cancel_reservation(res_id: str, confirm: bool = False):
    if not confirm:
        raise HTTPException(status_code=400, detail="Cancellation not confirmed")
    data = load_data()
    if res_id in data["reservations"]:
        del data["reservations"][res_id]
        save_data(data)
        return {"status": "cancelled"}
    else:
        raise HTTPException(status_code=404, detail="Reservation not found")

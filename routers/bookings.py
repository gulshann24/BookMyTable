from fastapi import APIRouter, HTTPException, Header
from typing import Optional, List
from database import get_connection
from models import BookingCreate, BookingResponse, BookingStatusUpdate

router = APIRouter()


def row_to_booking(row) -> dict:
    return {
        "id":              row["id"],
        "full_name":       row["full_name"],
        "email":           row["email"],
        "phone":           row["phone"],
        "guests":          row["guests"],
        "booking_date":    row["date"],
        "booking_time":    row["time"],
        "status":          row["status"],
        "restaurant_id":   row["restaurant_id"],
        "restaurant_name": row["restaurant_name"],
        "created_at":      row["created_at"],
    }


@router.post("/", response_model=BookingResponse, status_code=201)
def create_booking(
    booking: BookingCreate,
    authorization: Optional[str] = Header(None)
):
    user_id = None

    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ", 1)[1]
        with get_connection() as conn:
            user = conn.execute(
                "SELECT id FROM users WHERE id = ?", (token,)
            ).fetchone()
            if user:
                user_id = user["id"]

    with get_connection() as conn:
        cur = conn.execute(
            """
            INSERT INTO bookings
                (user_id, restaurant_id, restaurant_name, full_name, email, phone, guests, date, time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                booking.restaurant_id,
                booking.restaurant_name,
                booking.full_name,
                booking.email,
                booking.phone,
                booking.guests,
                str(booking.booking_date),
                str(booking.booking_time),
            )
        )
        booking_id = cur.lastrowid
        conn.commit()

        row = conn.execute(
            "SELECT * FROM bookings WHERE id = ?", (booking_id,)
        ).fetchone()

    return row_to_booking(row)


@router.get("/", response_model=List[BookingResponse])
def list_bookings():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM bookings ORDER BY created_at DESC"
        ).fetchall()
    return [row_to_booking(r) for r in rows]


@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: int):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM bookings WHERE id = ?", (booking_id,)
        ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Booking not found")
    return row_to_booking(row)


@router.patch("/{booking_id}/status", response_model=BookingResponse)
def update_booking_status(booking_id: int, update: BookingStatusUpdate):
    with get_connection() as conn:
        conn.execute(
            "UPDATE bookings SET status = ? WHERE id = ?",
            (update.status, booking_id)
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM bookings WHERE id = ?", (booking_id,)
        ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Booking not found")
    return row_to_booking(row)


@router.delete("/{booking_id}", status_code=204)
def delete_booking(booking_id: int):
    with get_connection() as conn:
        conn.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
        conn.commit()

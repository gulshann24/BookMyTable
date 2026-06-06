from fastapi import APIRouter, HTTPException
from typing import List
from database import get_connection
from models import ContactCreate, ContactResponse

router = APIRouter()


def row_to_contact(row) -> dict:
    return {
        "id":         row["id"],
        "full_name":  row["full_name"],
        "email":      row["email"],
        "phone":      row["phone"],
        "message":    row["message"],
        "created_at": row["created_at"],
    }


@router.post("/", response_model=ContactResponse, status_code=201)
def create_contact(contact: ContactCreate):
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO contacts (full_name, email, phone, message) VALUES (?, ?, ?, ?)",
            (contact.full_name, contact.email, contact.phone, contact.message)
        )
        contact_id = cur.lastrowid
        conn.commit()
        row = conn.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,)).fetchone()
    return row_to_contact(row)


@router.get("/", response_model=List[ContactResponse])
def list_contacts():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM contacts ORDER BY created_at DESC").fetchall()
    return [row_to_contact(r) for r in rows]


@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Contact not found")
    return row_to_contact(row)


@router.delete("/{contact_id}", status_code=204)
def delete_contact(contact_id: int):
    with get_connection() as conn:
        conn.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        conn.commit()

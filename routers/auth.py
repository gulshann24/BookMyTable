from fastapi import APIRouter, HTTPException
from database import get_connection
from models import UserCreate, UserLogin, UserResponse
import hashlib

router = APIRouter()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


@router.post("/register", response_model=UserResponse, status_code=201)
def register(user: UserCreate):
    with get_connection() as conn:
        existing = conn.execute(
            "SELECT id FROM users WHERE email = ? OR username = ?",
            (user.email, user.username)
        ).fetchone()
        if existing:
            raise HTTPException(status_code=400, detail="Email or username already registered.")

        cur = conn.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (user.username, user.email, hash_password(user.password))
        )
        user_id = cur.lastrowid
        conn.commit()
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

    return {"id": row["id"], "username": row["username"], "email": row["email"]}


@router.post("/login")
def login(credentials: UserLogin):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE email = ?", (credentials.email,)
        ).fetchone()

    if not row or row["password"] != hash_password(credentials.password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    # Simple token: user id as string (replace with JWT in production)
    return {
        "access_token": str(row["id"]),
        "token_type":   "bearer",
        "username":     row["username"],
    }

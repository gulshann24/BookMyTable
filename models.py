from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import date as Date, time as Time


# ─────────────────────────────────────────────
# User Models (Authentication)
# ─────────────────────────────────────────────

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str


# ─────────────────────────────────────────────
# Restaurant Models
# ─────────────────────────────────────────────

class RestaurantResponse(BaseModel):
    id: int
    name: str
    image_url: str
    address: str
    city: str
    cuisine: str
    rating: float
    google_maps_link: Optional[str]
    is_open: bool
    opening_time: str
    closing_time: str
    available_tables: int
    price_range: str
    created_at: str


# ─────────────────────────────────────────────
# Booking Models
# ─────────────────────────────────────────────

class BookingCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=7, max_length=15)
    guests: int = Field(..., ge=1, le=20)
    booking_date: Date
    booking_time: Time
    restaurant_id: Optional[int] = None
    restaurant_name: Optional[str] = None


class BookingResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str
    guests: int
    booking_date: str
    booking_time: str
    status: str
    restaurant_id: Optional[int]
    restaurant_name: Optional[str]
    created_at: str


class BookingStatusUpdate(BaseModel):
    status: Literal["pending", "confirmed", "cancelled"]


# ─────────────────────────────────────────────
# Contact Models
# ─────────────────────────────────────────────

class ContactCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(default=None, max_length=15)
    message: str = Field(..., min_length=5, max_length=1000)


class ContactResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone: Optional[str]
    message: str
    created_at: str

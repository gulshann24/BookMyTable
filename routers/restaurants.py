from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from database import get_connection
from models import RestaurantResponse

router = APIRouter()


def row_to_restaurant(row) -> dict:
    return {
        "id":               row["id"],
        "name":             row["name"],
        "image_url":        row["image_url"],
        "address":          row["address"],
        "city":             row["city"],
        "cuisine":          row["cuisine"],
        "rating":           row["rating"],
        "google_maps_link": row["google_maps_link"],
        "is_open":          bool(row["is_open"]),
        "opening_time":     row["opening_time"],
        "closing_time":     row["closing_time"],
        "available_tables": row["available_tables"],
        "price_range":      row["price_range"],
        "created_at":       row["created_at"],
    }


@router.get("/", response_model=List[RestaurantResponse])
def list_restaurants(
    city:    Optional[str] = Query(None),
    cuisine: Optional[str] = Query(None),
    search:  Optional[str] = Query(None),
    sort_by: Optional[str] = Query(None, regex="^(rating|name)$"),
    is_open: Optional[bool] = Query(None),
):
    """
    List all restaurants.
    Supports filtering by city, cuisine, search term, open status.
    Supports sorting by rating or name.
    """
    query  = "SELECT * FROM restaurants WHERE 1=1"
    params = []

    if city:
        query  += " AND LOWER(city) = LOWER(?)"
        params.append(city)

    if cuisine:
        query  += " AND LOWER(cuisine) = LOWER(?)"
        params.append(cuisine)

    if search:
        query  += " AND (LOWER(name) LIKE LOWER(?) OR LOWER(address) LIKE LOWER(?) OR LOWER(cuisine) LIKE LOWER(?))"
        like = f"%{search}%"
        params.extend([like, like, like])

    if is_open is not None:
        query  += " AND is_open = ?"
        params.append(1 if is_open else 0)

    if sort_by == "rating":
        query += " ORDER BY rating DESC"
    elif sort_by == "name":
        query += " ORDER BY name ASC"
    else:
        query += " ORDER BY rating DESC"

    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()

    return [row_to_restaurant(r) for r in rows]


@router.get("/cities")
def list_cities():
    """Return distinct cities available."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT DISTINCT city FROM restaurants ORDER BY city ASC"
        ).fetchall()
    return {"cities": [r["city"] for r in rows]}


@router.get("/cuisines")
def list_cuisines():
    """Return distinct cuisines available."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT DISTINCT cuisine FROM restaurants ORDER BY cuisine ASC"
        ).fetchall()
    return {"cuisines": [r["cuisine"] for r in rows]}


@router.get("/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(restaurant_id: int):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM restaurants WHERE id = ?", (restaurant_id,)
        ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    return row_to_restaurant(row)

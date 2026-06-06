# BookMyTable
BookMyTable is a full-stack restaurant discovery, table reservation, and food delivery platform. Users can browse restaurants, reserve tables, order food, filter Veg/Non-Veg menus, manage carts, and switch between Dark/Light modes. Built using HTML, CSS, JavaScript, FastAPI, and SQLite.

Python + FastAPI backend with SQLite for the L'Gran restaurant discovery & booking website.

---

## Project Structure

```
lgran/
├── main.py              # FastAPI app entry point
├── database.py          # SQLite connection, schema & seed data
├── models.py            # Pydantic request/response schemas
├── requirements.txt     # Python dependencies
├── run.bat              # Windows quick-start script
├── index.html           # Main frontend
├── login.html           # Auth page
├── style.css            # Styles
├── script.js            # Frontend logic
└── routers/
    ├── auth.py          # /api/auth       — login & register
    ├── bookings.py      # /api/bookings   — CRUD
    ├── contact.py       # /api/contact    — CRUD
    └── restaurants.py   # /api/restaurants — listing & filtering
```

---

## Setup & Run

### 1. Create a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the backend
```bash
uvicorn main:app --reload
```
Backend → **http://localhost:8000**

### 4. Serve the frontend (separate terminal)
```bash
python -m http.server 5500
```
Frontend → **http://localhost:5500/index.html**

> Or just double-click `run.bat` on Windows to launch both automatically.

---

## API Endpoints

### Restaurants  `/api/restaurants`

| Method | URL                                    | Description                     |
|--------|----------------------------------------|---------------------------------|
| GET    | `/api/restaurants`                     | List all restaurants            |
| GET    | `/api/restaurants?city=Lucknow`        | Filter by city                  |
| GET    | `/api/restaurants?cuisine=Italian`     | Filter by cuisine               |
| GET    | `/api/restaurants?search=biryani`      | Search by name/cuisine/address  |
| GET    | `/api/restaurants?sort_by=rating`      | Sort by rating (default)        |
| GET    | `/api/restaurants?sort_by=name`        | Sort alphabetically             |
| GET    | `/api/restaurants?is_open=true`        | Only open restaurants           |
| GET    | `/api/restaurants/cities`              | List available cities           |
| GET    | `/api/restaurants/cuisines`            | List available cuisines         |
| GET    | `/api/restaurants/{id}`                | Get single restaurant           |

### Bookings  `/api/bookings`

| Method | URL                            | Description              |
|--------|--------------------------------|--------------------------|
| POST   | `/api/bookings/`               | Submit a new booking     |
| GET    | `/api/bookings/`               | List all bookings        |
| GET    | `/api/bookings/{id}`           | Get booking by ID        |
| PATCH  | `/api/bookings/{id}/status`    | Update status            |
| DELETE | `/api/bookings/{id}`           | Delete booking           |

**POST body (with restaurant):**
```json
{
  "full_name": "Rahul Sharma",
  "email": "rahul@example.com",
  "phone": "9876543210",
  "guests": 2,
  "booking_date": "2025-12-25",
  "booking_time": "19:30",
  "restaurant_id": 1,
  "restaurant_name": "Spice Route"
}
```

### Contact  `/api/contact`

| Method | URL                   | Description               |
|--------|-----------------------|---------------------------|
| POST   | `/api/contact/`       | Submit a contact message  |
| GET    | `/api/contact/`       | List all messages         |
| DELETE | `/api/contact/{id}`   | Delete message            |

### Auth  `/api/auth`

| Method | URL                    | Description     |
|--------|------------------------|-----------------|
| POST   | `/api/auth/register`   | Register user   |
| POST   | `/api/auth/login`      | Login user      |

---

## Interactive Docs

- **Swagger UI** → http://localhost:8000/docs
- **ReDoc**       → http://localhost:8000/redoc

---

## Database

`lgran.db` is auto-created with **13 sample restaurants** across Lucknow, Delhi, and Mumbai on first run.

---

## What's New in v2.0

- ✅ `restaurants` table with full details
- ✅ Restaurant discovery section with cards
- ✅ Search, city filter, cuisine filter, sort, open-only toggle
- ✅ Glassmorphism restaurant cards with hover animations
- ✅ Favourite/bookmark (stored in localStorage)
- ✅ Click "Book Now" → auto-fills booking form with restaurant
- ✅ Booking includes `restaurant_id` and `restaurant_name`
- ✅ Toast notification system (replaces `alert()`)
- ✅ Loading spinner and empty state
- ✅ Fully responsive down to mobile

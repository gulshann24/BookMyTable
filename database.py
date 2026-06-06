import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "lgran.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with get_connection() as conn:

        conn.executescript("""
        -- =========================
        -- USERS TABLE
        -- =========================
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT UNIQUE NOT NULL,
            email       TEXT UNIQUE NOT NULL,
            password    TEXT NOT NULL,
            created_at  TEXT NOT NULL DEFAULT (datetime('now'))
        );

        -- =========================
        -- RESTAURANTS TABLE
        -- =========================
        CREATE TABLE IF NOT EXISTS restaurants (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            name             TEXT NOT NULL,
            image_url        TEXT NOT NULL,
            address          TEXT NOT NULL,
            city             TEXT NOT NULL,
            cuisine          TEXT NOT NULL,
            rating           REAL NOT NULL CHECK(rating BETWEEN 1.0 AND 5.0),
            google_maps_link TEXT,
            is_open          INTEGER NOT NULL DEFAULT 1,
            opening_time     TEXT NOT NULL DEFAULT '10:00',
            closing_time     TEXT NOT NULL DEFAULT '23:00',
            available_tables INTEGER NOT NULL DEFAULT 10,
            price_range      TEXT NOT NULL DEFAULT '₹₹'
                             CHECK(price_range IN ('₹', '₹₹', '₹₹₹', '₹₹₹₹')),
            created_at       TEXT NOT NULL DEFAULT (datetime('now'))
        );

        -- =========================
        -- BOOKINGS TABLE
        -- =========================
        CREATE TABLE IF NOT EXISTS bookings (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id         INTEGER,
            restaurant_id   INTEGER,
            restaurant_name TEXT,

            full_name       TEXT NOT NULL,
            email           TEXT NOT NULL,
            phone           TEXT NOT NULL,

            guests          INTEGER NOT NULL
                            CHECK(guests BETWEEN 1 AND 20),

            date            TEXT NOT NULL,
            time            TEXT NOT NULL,

            status          TEXT NOT NULL
                            DEFAULT 'pending'
                            CHECK(status IN (
                                'pending',
                                'confirmed',
                                'cancelled'
                            )),

            created_at      TEXT NOT NULL
                            DEFAULT (datetime('now')),

            FOREIGN KEY(user_id)        REFERENCES users(id)       ON DELETE CASCADE,
            FOREIGN KEY(restaurant_id)  REFERENCES restaurants(id) ON DELETE SET NULL
        );

        -- =========================
        -- CONTACTS TABLE
        -- =========================
        CREATE TABLE IF NOT EXISTS contacts (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name   TEXT NOT NULL,
            email       TEXT NOT NULL,
            phone       TEXT,
            message     TEXT NOT NULL,
            created_at  TEXT NOT NULL DEFAULT (datetime('now'))
        );
        """)

        # Seed sample restaurants (only if table is empty)
        existing = conn.execute("SELECT COUNT(*) FROM restaurants").fetchone()[0]
        if existing == 0:
            conn.executescript("""
            INSERT INTO restaurants
                (name, image_url, address, city, cuisine, rating, google_maps_link, is_open, opening_time, closing_time, available_tables, price_range)
            VALUES
                (
                    'Spice Route',
                    'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800',
                    '12, Hazratganj, Near Capitol Cinema',
                    'Lucknow',
                    'North Indian',
                    4.7,
                    'https://maps.google.com/?q=Hazratganj+Lucknow',
                    1, '11:00', '23:30', 8, '₹₹₹'
                ),
                (
                    'The Mughal Feast',
                    'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800',
                    '45, Aminabad Chowk, Old City',
                    'Lucknow',
                    'Mughlai',
                    4.5,
                    'https://maps.google.com/?q=Aminabad+Lucknow',
                    1, '12:00', '23:00', 12, '₹₹'
                ),
                (
                    'Sakura Garden',
                    'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800',
                    '8, Gomti Nagar, Vibhuti Khand',
                    'Lucknow',
                    'Japanese',
                    4.3,
                    'https://maps.google.com/?q=Gomti+Nagar+Lucknow',
                    1, '12:00', '22:30', 6, '₹₹₹₹'
                ),
                (
                    'Bella Italia',
                    'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800',
                    '3, Mahanagar Extension, Ring Road',
                    'Lucknow',
                    'Italian',
                    4.6,
                    'https://maps.google.com/?q=Mahanagar+Lucknow',
                    1, '11:30', '23:00', 10, '₹₹₹'
                ),
                (
                    'Dragon Palace',
                    'https://images.unsplash.com/photo-1563245372-f21724e3856d?w=800',
                    '22, Indira Nagar, Sector B',
                    'Lucknow',
                    'Chinese',
                    4.2,
                    'https://maps.google.com/?q=Indira+Nagar+Lucknow',
                    0, '12:00', '22:00', 0, '₹₹'
                ),
                (
                    'The Continental House',
                    'https://images.unsplash.com/photo-1544148103-0773bf10d330?w=800',
                    '7, Shahnajaf Road, Hazratganj',
                    'Lucknow',
                    'Continental',
                    4.8,
                    'https://maps.google.com/?q=Shahnajaf+Road+Lucknow',
                    1, '10:00', '23:59', 15, '₹₹₹₹'
                ),
                (
                    'Biryani Bros',
                    'https://images.unsplash.com/photo-1563379926898-05f4575a45d8?w=800',
                    '88, Chowk, Old Lucknow',
                    'Lucknow',
                    'Awadhi',
                    4.9,
                    'https://maps.google.com/?q=Chowk+Lucknow',
                    1, '10:30', '22:30', 5, '₹'
                ),
                (
                    'Mezze House',
                    'https://images.unsplash.com/photo-1600891964599-f61ba0e24092?w=800',
                    '15, Aliganj, Near Post Office',
                    'Lucknow',
                    'Mediterranean',
                    4.4,
                    'https://maps.google.com/?q=Aliganj+Lucknow',
                    1, '11:00', '22:00', 9, '₹₹₹'
                ),

                (
                    'Punjab Da Dhaba',
                    'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=800',
                    '34, Rajouri Garden, Main Market',
                    'Delhi',
                    'North Indian',
                    4.5,
                    'https://maps.google.com/?q=Rajouri+Garden+Delhi',
                    1, '09:00', '23:00', 20, '₹'
                ),
                (
                    'China Box',
                    'https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800',
                    '5, Connaught Place, Block E',
                    'Delhi',
                    'Chinese',
                    4.1,
                    'https://maps.google.com/?q=Connaught+Place+Delhi',
                    1, '12:00', '23:30', 14, '₹₹'
                ),
                (
                    'Trattoria Roma',
                    'https://images.unsplash.com/photo-1533777324565-a040eb52facd?w=800',
                    '9, Khan Market, Central Lane',
                    'Delhi',
                    'Italian',
                    4.7,
                    'https://maps.google.com/?q=Khan+Market+Delhi',
                    0, '12:00', '23:00', 0, '₹₹₹'
                ),

                (
                    'Marine Drive Grill',
                    'https://images.unsplash.com/photo-1484659619207-9165d119dafe?w=800',
                    '101, Nariman Point, Marine Drive',
                    'Mumbai',
                    'Continental',
                    4.6,
                    'https://maps.google.com/?q=Nariman+Point+Mumbai',
                    1, '11:00', '00:00', 18, '₹₹₹₹'
                ),
                (
                    'Tiffin House',
                    'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800',
                    '27, Dadar West, Shivaji Park',
                    'Mumbai',
                    'South Indian',
                    4.3,
                    'https://maps.google.com/?q=Dadar+West+Mumbai',
                    1, '07:30', '22:00', 7, '₹'
                );
            """)

        conn.commit()

    print(f"[DB] SQLite database ready → {DB_PATH}")


if __name__ == "__main__":
    init_db()

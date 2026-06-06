from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import init_db
from routers import bookings, contact, auth, restaurants


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="L'Gran Restaurant API",
    description="Backend API for L'Gran restaurant booking and contact system",
    version="2.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(bookings.router,     prefix="/api/bookings",     tags=["Bookings"])
app.include_router(contact.router,      prefix="/api/contact",      tags=["Contact"])
app.include_router(auth.router,         prefix="/api/auth",         tags=["Authentication"])
app.include_router(restaurants.router,  prefix="/api/restaurants",  tags=["Restaurants"])


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "L'Gran Restaurant API is running", "version": "2.0.0"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}

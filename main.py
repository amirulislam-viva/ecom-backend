from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api import auth, products, categories, brands, hero, featured, uploads, orders, site_settings

from database import engine, Base
import models

app = FastAPI(title="E-commerce Admin API")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])
app.include_router(brands.router, prefix="/api/brands", tags=["Brands"])
app.include_router(hero.router, prefix="/api/hero", tags=["Hero Section"])
app.include_router(featured.router, prefix="/api/featured", tags=["Featured Products"])
app.include_router(uploads.router, prefix="/api/uploads", tags=["Uploads"])
app.include_router(orders.router, prefix="/api/orders", tags=["Orders"])
app.include_router(site_settings.router, prefix="/api/site-settings", tags=["Site Settings"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the E-commerce Admin API"}

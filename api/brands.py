from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from deps import get_db, get_current_admin
from services.brand_service import BrandService
import schemas

router = APIRouter()
brand_service = BrandService()

@router.get("/", response_model=List[schemas.Brand])
def get_brands(db: Session = Depends(get_db)):
    return brand_service.get_all_brands(db)

@router.get("/{name}", response_model=schemas.Brand)
def get_brand_by_name(name: str, db: Session = Depends(get_db)):
    db_brand = brand_service.get_brand_by_name(db, name)
    if not db_brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return db_brand

@router.post("/", response_model=schemas.Brand)
def create_brand(brand: schemas.BrandCreate, db: Session = Depends(get_db), admin = Depends(get_current_admin)):
    return brand_service.create_brand(db, brand)

@router.put("/{brand_id}", response_model=schemas.Brand)
def update_brand(brand_id: int, brand: schemas.BrandCreate, db: Session = Depends(get_db), admin = Depends(get_current_admin)):
    db_brand = brand_service.update_brand(db, brand_id, brand)
    if not db_brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return db_brand

@router.delete("/{brand_id}")
def delete_brand(brand_id: int, db: Session = Depends(get_db), admin = Depends(get_current_admin)):
    success = brand_service.delete_brand(db, brand_id)
    if not success:
        raise HTTPException(status_code=404, detail="Brand not found")
    return {"message": "Brand deleted"}

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from deps import get_db, get_current_admin
from services.featured_service import FeaturedService
import schemas

router = APIRouter()
featured_service = FeaturedService()

@router.get("/", response_model=List[schemas.FeaturedProduct])
def get_featured_products(db: Session = Depends(get_db)):
    return featured_service.get_all(db)

@router.post("/", response_model=schemas.FeaturedProduct)
def create_featured_product(featured: schemas.FeaturedProductCreate, db: Session = Depends(get_db), admin = Depends(get_current_admin)):
    return featured_service.create(db, featured)

@router.put("/{featured_id}", response_model=schemas.FeaturedProduct)
def update_featured_product(featured_id: int, featured: schemas.FeaturedProductCreate, db: Session = Depends(get_db), admin = Depends(get_current_admin)):
    db_featured = featured_service.update(db, featured_id, featured)
    if not db_featured:
        raise HTTPException(status_code=404, detail="Featured product not found")
    return db_featured

@router.delete("/{featured_id}")
def delete_featured_product(featured_id: int, db: Session = Depends(get_db), admin = Depends(get_current_admin)):
    success = featured_service.delete(db, featured_id)
    if not success:
        raise HTTPException(status_code=404, detail="Featured product not found")
    return {"message": "Featured product deleted"}

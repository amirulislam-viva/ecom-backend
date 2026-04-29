from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from deps import get_db, get_current_admin
from services.category_service import CategoryService
import schemas

router = APIRouter()
category_service = CategoryService()

@router.get("/", response_model=List[schemas.Category])
def get_categories(db: Session = Depends(get_db)):
    return category_service.get_all(db)

@router.get("/{slug}", response_model=schemas.Category)
def get_category_by_slug(slug: str, db: Session = Depends(get_db)):
    db_category = category_service.get_by_slug(db, slug)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.post("/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db), admin = Depends(get_current_admin)):
    return category_service.create(db, category)

@router.put("/{category_id}", response_model=schemas.Category)
def update_category(category_id: int, category: schemas.CategoryCreate, db: Session = Depends(get_db), admin = Depends(get_current_admin)):
    db_category = category_service.update(db, category_id, category)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db), admin = Depends(get_current_admin)):
    success = category_service.delete(db, category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted"}

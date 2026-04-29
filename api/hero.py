from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from deps import get_db, get_current_admin
from services.hero_service import HeroService
import schemas

router = APIRouter()
hero_service = HeroService()

@router.get("/", response_model=List[schemas.HeroSection])
def get_hero_sections(db: Session = Depends(get_db)):
    return hero_service.get_all(db)

@router.post("/", response_model=schemas.HeroSection)
def create_hero_section(hero: schemas.HeroSectionCreate, db: Session = Depends(get_db), admin = Depends(get_current_admin)):
    return hero_service.create(db, hero)

@router.put("/{hero_id}", response_model=schemas.HeroSection)
def update_hero_section(hero_id: int, hero: schemas.HeroSectionCreate, db: Session = Depends(get_db), admin = Depends(get_current_admin)):
    db_hero = hero_service.update(db, hero_id, hero)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero section not found")
    return db_hero

@router.delete("/{hero_id}")
def delete_hero_section(hero_id: int, db: Session = Depends(get_db), admin = Depends(get_current_admin)):
    success = hero_service.delete(db, hero_id)
    if not success:
        raise HTTPException(status_code=404, detail="Hero section not found")
    return {"message": "Hero section deleted"}

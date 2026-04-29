from sqlalchemy.orm import Session
from repositories.hero_repo import HeroRepository
import schemas

class HeroService:
    def __init__(self):
        self.repo = HeroRepository()

    def get_all(self, db: Session):
        return self.repo.get_all(db)

    def create(self, db: Session, hero: schemas.HeroSectionCreate):
        return self.repo.create(db, hero.dict())

    def update(self, db: Session, id: int, hero: schemas.HeroSectionCreate):
        return self.repo.update(db, id, hero.dict())

    def delete(self, db: Session, id: int):
        return self.repo.delete(db, id)

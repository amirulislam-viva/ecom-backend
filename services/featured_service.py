from sqlalchemy.orm import Session
from repositories.featured_repo import FeaturedRepository
import schemas

class FeaturedService:
    def __init__(self):
        self.repo = FeaturedRepository()

    def get_all(self, db: Session):
        return self.repo.get_all(db)

    def create(self, db: Session, featured: schemas.FeaturedProductCreate):
        return self.repo.create(db, featured.dict())

    def update(self, db: Session, id: int, featured: schemas.FeaturedProductCreate):
        return self.repo.update(db, id, featured.dict())

    def delete(self, db: Session, id: int):
        return self.repo.delete(db, id)

from sqlalchemy.orm import Session
from repositories.category_repo import CategoryRepository
import schemas

class CategoryService:
    def __init__(self):
        self.repo = CategoryRepository()

    def get_all(self, db: Session):
        return self.repo.get_all(db)

    def get_by_slug(self, db: Session, slug: str):
        return self.repo.get_by_slug(db, slug)

    def create(self, db: Session, category: schemas.CategoryCreate):
        return self.repo.create(db, category.dict())

    def update(self, db: Session, id: int, category: schemas.CategoryCreate):
        return self.repo.update(db, id, category.dict())

    def delete(self, db: Session, id: int):
        return self.repo.delete(db, id)

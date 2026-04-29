from sqlalchemy.orm import Session
from .base_repo import BaseRepository
import models

class CategoryRepository(BaseRepository[models.Category]):
    def __init__(self):
        super().__init__(models.Category)

    def get_by_slug(self, db: Session, slug: str):
        return db.query(models.Category).filter(models.Category.slug == slug).first()

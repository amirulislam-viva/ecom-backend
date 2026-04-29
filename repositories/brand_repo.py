from sqlalchemy.orm import Session
from .base_repo import BaseRepository
import models

class BrandRepository(BaseRepository[models.Brand]):
    def __init__(self):
        super().__init__(models.Brand)

    def get_by_name(self, db: Session, name: str):
        return db.query(models.Brand).filter(models.Brand.name.ilike(name)).first()

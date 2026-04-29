from sqlalchemy.orm import Session
from repositories.brand_repo import BrandRepository
import schemas

class BrandService:
    def __init__(self):
        self.repo = BrandRepository()

    def get_all_brands(self, db: Session):
        return self.repo.get_all(db)

    def get_brand_by_name(self, db: Session, name: str):
        return self.repo.get_by_name(db, name)

    def create_brand(self, db: Session, brand: schemas.BrandCreate):
        return self.repo.create(db, brand.dict())

    def update_brand(self, db: Session, brand_id: int, brand: schemas.BrandCreate):
        return self.repo.update(db, brand_id, brand.dict())

    def delete_brand(self, db: Session, brand_id: int):
        return self.repo.delete(db, brand_id)

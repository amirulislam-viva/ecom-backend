from typing import Optional
from sqlalchemy.orm import Session
from repositories.product_repo import ProductRepository
import schemas

class ProductService:
    def __init__(self):
        self.repo = ProductRepository()

    def get_all(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100, 
        category_id: Optional[int] = None, 
        brand_id: Optional[int] = None, 
        search: Optional[str] = None
    ):
        return self.repo.get_products(db, skip=skip, limit=limit, category_id=category_id, brand_id=brand_id, search=search)

    def get_by_id(self, db: Session, id: int):
        return self.repo.get_by_id(db, id)

    def get_by_slug(self, db: Session, slug: str):
        return self.repo.get_by_slug(db, slug)

    def create(self, db: Session, product: schemas.ProductCreate):
        return self.repo.create(db, product.dict())

    def update(self, db: Session, id: int, product: schemas.ProductCreate):
        return self.repo.update(db, id, product.dict())

    def delete(self, db: Session, id: int):
        return self.repo.delete(db, id)

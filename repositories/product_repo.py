from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from .base_repo import BaseRepository
import models

class ProductRepository(BaseRepository[models.Product]):
    def __init__(self):
        super().__init__(models.Product)

    def get_products(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100, 
        category_id: Optional[int] = None, 
        brand_id: Optional[int] = None, 
        search: Optional[str] = None
    ) -> List[models.Product]:
        query = db.query(models.Product).options(joinedload(models.Product.images))
        
        if category_id:
            query = query.filter(models.Product.category_id == category_id)
        if brand_id:
            query = query.filter(models.Product.brand_id == brand_id)
        if search:
            query = query.filter(models.Product.name.contains(search) | models.Product.description.contains(search))
            
        return query.order_by(models.Product.created_at.desc()).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in_data: dict) -> models.Product:
        image_urls = obj_in_data.pop("image_urls", [])
            
        db_obj = models.Product(**obj_in_data)
        db.add(db_obj)
        db.flush() # flush to get product id
        
        # Add images
        for idx, url in enumerate(image_urls):
            db_img = models.ProductImage(product_id=db_obj.id, image_url=url, sort_order=idx)
            db.add(db_img)
            
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, id: int, obj_in_data: dict) -> Optional[models.Product]:
        image_urls = obj_in_data.pop("image_urls", None)
        db_obj = self.get_by_id(db, id)
        if not db_obj:
            return None
            
        for key, value in obj_in_data.items():
            setattr(db_obj, key, value)
            
        if image_urls is not None:
            # For update, we might want to replace images or just keep it as is.
            # Usually, if image_urls is provided, it means we want to sync the list.
            # But the requirement was mainly about creating with pictures.
            # Let's implement sync for update as well.
            db.query(models.ProductImage).filter(models.ProductImage.product_id == id).delete()
            for idx, url in enumerate(image_urls):
                db_img = models.ProductImage(product_id=id, image_url=url, sort_order=idx)
                db.add(db_img)
                
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_id(self, db: Session, id: int) -> Optional[models.Product]:
        return db.query(models.Product).options(joinedload(models.Product.images)).filter(models.Product.id == id).first()

    def get_by_slug(self, db: Session, slug: str):
        return db.query(models.Product).options(joinedload(models.Product.images)).filter(models.Product.slug == slug).first()

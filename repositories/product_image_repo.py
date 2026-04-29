from typing import List, Optional
from sqlalchemy.orm import Session
import models


class ProductImageRepository:
    def get_by_product(self, db: Session, product_id: int) -> List[models.ProductImage]:
        return (
            db.query(models.ProductImage)
            .filter(models.ProductImage.product_id == product_id)
            .order_by(models.ProductImage.sort_order)
            .all()
        )

    def add_image(self, db: Session, product_id: int, image_url: str, sort_order: int = 0) -> models.ProductImage:
        # Default sort_order = max existing + 1 so new images go to the end
        existing = self.get_by_product(db, product_id)
        if sort_order == 0 and existing:
            sort_order = max(img.sort_order for img in existing) + 1
        img = models.ProductImage(product_id=product_id, image_url=image_url, sort_order=sort_order)
        db.add(img)
        db.commit()
        db.refresh(img)
        return img

    def delete_image(self, db: Session, image_id: int, product_id: int) -> bool:
        img = (
            db.query(models.ProductImage)
            .filter(models.ProductImage.id == image_id, models.ProductImage.product_id == product_id)
            .first()
        )
        if not img:
            return False
        db.delete(img)
        db.commit()
        return True

    def reorder_images(self, db: Session, product_id: int, image_ids: List[int]) -> List[models.ProductImage]:
        """
        Accept an ordered list of image IDs and reassign sort_order = index.
        Only images belonging to `product_id` are updated.
        """
        images_map = {
            img.id: img
            for img in db.query(models.ProductImage)
            .filter(models.ProductImage.product_id == product_id)
            .all()
        }
        for idx, image_id in enumerate(image_ids):
            if image_id in images_map:
                images_map[image_id].sort_order = idx
        db.commit()
        return self.get_by_product(db, product_id)

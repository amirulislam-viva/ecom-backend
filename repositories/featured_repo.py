from sqlalchemy.orm import Session, joinedload
from .base_repo import BaseRepository
import models

class FeaturedRepository(BaseRepository[models.FeaturedProduct]):
    def __init__(self):
        super().__init__(models.FeaturedProduct)

    def get_all(self, db: Session):
        return db.query(models.FeaturedProduct).options(
            joinedload(models.FeaturedProduct.product).joinedload(models.Product.images)
        ).order_by(models.FeaturedProduct.sort_order).all()

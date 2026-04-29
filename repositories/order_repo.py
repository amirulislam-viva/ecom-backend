from sqlalchemy.orm import Session
from .base_repo import BaseRepository
import models
from typing import List, Optional

class OrderRepository(BaseRepository[models.Order]):
    def __init__(self):
        super().__init__(models.Order)

    def get_by_track_id(self, db: Session, track_id: str, mobile_number: str):
        return db.query(models.Order).filter(
            models.Order.track_id == track_id,
            models.Order.mobile_number == mobile_number
        ).first()

    def get_all_orders(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100, 
        status: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        search: Optional[str] = None
    ):
        query = db.query(models.Order)
        
        # Filtering
        if status:
            query = query.filter(models.Order.status == status)
        
        if start_date:
            try:
                from datetime import datetime
                sd = datetime.fromisoformat(start_date)
                query = query.filter(models.Order.created_at >= sd)
            except: pass
            
        if end_date:
            try:
                from datetime import datetime
                ed = datetime.fromisoformat(end_date)
                query = query.filter(models.Order.created_at <= ed)
            except: pass
            
        if search:
            search_filter = f"%{search}%"
            # Search in Order fields and OrderItem names
            query = query.join(models.Order.items).filter(
                (models.Order.track_id.ilike(search_filter)) |
                (models.Order.customer_name.ilike(search_filter)) |
                (models.Order.mobile_number.ilike(search_filter)) |
                (models.OrderItem.product_name.ilike(search_filter))
            ).distinct()

        # Custom Sorting: Pending first, then by date desc
        from sqlalchemy import case
        sort_logic = case(
            (models.Order.status == "pending", 1),
            else_=2
        )
        
        return query.order_by(sort_logic, models.Order.created_at.desc()).offset(skip).limit(limit).all()

    def create_order(self, db: Session, order_data: dict, items_data: List[dict]):
        db_order = models.Order(**order_data)
        db.add(db_order)
        db.flush()  # To get the order ID

        for item_data in items_data:
            db_item = models.OrderItem(**item_data, order_id=db_order.id)
            db.add(db_item)
        
        db.commit()
        db.refresh(db_order)
        return db_order

    def update_status(self, db: Session, order_id: int, status: str):
        db_order = self.get(db, order_id)
        if db_order:
            db_order.status = status
            db.commit()
            db.refresh(db_order)
        return db_order

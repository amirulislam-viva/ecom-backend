from sqlalchemy.orm import Session
from repositories.order_repo import OrderRepository
import schemas
from typing import List

class OrderService:
    def __init__(self):
        self.repo = OrderRepository()

    def create_order(self, db: Session, order_in: schemas.OrderCreate):
        order_data = order_in.dict(exclude={"items"})
        items_data = [item.dict() for item in order_in.items]
        return self.repo.create_order(db, order_data, items_data)

    def get_order_by_tracking(self, db: Session, track_id: str, mobile_number: str):
        return self.repo.get_by_track_id(db, track_id, mobile_number)

    def get_all_orders(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100, 
        status: schemas.Optional[str] = None,
        start_date: schemas.Optional[str] = None,
        end_date: schemas.Optional[str] = None,
        search: schemas.Optional[str] = None
    ):
        return self.repo.get_all_orders(
            db, 
            skip=skip, 
            limit=limit, 
            status=status, 
            start_date=start_date, 
            end_date=end_date, 
            search=search
        )

    def update_order_status(self, db: Session, order_id: int, status: str):
        return self.repo.update_status(db, order_id, status)
    
    def get_order(self, db: Session, order_id: int):
        return self.repo.get(db, order_id)

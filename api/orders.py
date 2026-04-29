from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from deps import get_db, get_current_admin
from services.order_service import OrderService
import schemas

router = APIRouter()
order_service = OrderService()

@router.post("/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return order_service.create_order(db, order)

@router.get("/track", response_model=schemas.Order)
def track_order(track_id: str, mobile_number: str, db: Session = Depends(get_db)):
    db_order = order_service.get_order_by_tracking(db, track_id, mobile_number)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.get("/", response_model=List[schemas.Order])
def get_orders(
    skip: int = 0, 
    limit: int = 100, 
    status: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db), 
    admin = Depends(get_current_admin)
):
    return order_service.get_all_orders(
        db, 
        skip=skip, 
        limit=limit, 
        status=status, 
        start_date=start_date, 
        end_date=end_date, 
        search=search
    )

@router.get("/{order_id}", response_model=schemas.Order)
def get_order(order_id: int, db: Session = Depends(get_db), admin = Depends(get_current_admin)):
    db_order = order_service.get_order(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.put("/{order_id}/status", response_model=schemas.Order)
def update_order_status(order_id: int, status_update: schemas.OrderStatusUpdate, db: Session = Depends(get_db), admin = Depends(get_current_admin)):
    db_order = order_service.update_order_status(db, order_id, status_update.status)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

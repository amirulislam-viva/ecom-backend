from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from deps import get_db, get_current_admin
from services.product_service import ProductService
from repositories.product_image_repo import ProductImageRepository
import schemas

router = APIRouter()
product_service = ProductService()
image_repo = ProductImageRepository()


# ─── Product CRUD ────────────────────────────────────────────────────────────

@router.get("/", response_model=List[schemas.Product])
def get_products(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    brand_id: Optional[int] = None,
    search: Optional[str] = None,
):
    return product_service.get_all(db, skip=skip, limit=limit, category_id=category_id, brand_id=brand_id, search=search)

@router.get("/{slug}", response_model=schemas.Product)
def get_product_by_slug(slug: str, db: Session = Depends(get_db)):
    db_product = product_service.get_by_slug(db, slug)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.post("/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    try:
        return product_service.create(db, product)
    except IntegrityError as e:
        if "UNIQUE constraint failed: products.slug" in str(e):
            raise HTTPException(status_code=400, detail={"field": "slug", "message": "Product slug already exists"})
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    try:
        db_product = product_service.update(db, product_id, product)
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")
        return db_product
    except IntegrityError as e:
        if "UNIQUE constraint failed: products.slug" in str(e):
            raise HTTPException(status_code=400, detail={"field": "slug", "message": "Product slug already exists"})
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    success = product_service.delete(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted"}


# ─── Product Images ───────────────────────────────────────────────────────────

@router.get("/{product_id}/images", response_model=List[schemas.ProductImage])
def get_product_images(product_id: int, db: Session = Depends(get_db)):
    return image_repo.get_by_product(db, product_id)


@router.post("/{product_id}/images", response_model=schemas.ProductImage)
def add_product_image(
    product_id: int,
    body: schemas.ProductImageCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    # Verify the product exists
    if not product_service.get_by_id(db, product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return image_repo.add_image(db, product_id, body.image_url, body.sort_order)


@router.delete("/{product_id}/images/{image_id}")
def delete_product_image(
    product_id: int,
    image_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    success = image_repo.delete_image(db, image_id, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Image not found")
    return {"message": "Image deleted"}


@router.put("/{product_id}/images/reorder", response_model=List[schemas.ProductImage])
def reorder_product_images(
    product_id: int,
    body: schemas.ProductImageReorder,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    if not product_service.get_by_id(db, product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return image_repo.reorder_images(db, product_id, body.image_ids)

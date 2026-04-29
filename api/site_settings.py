from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from deps import get_current_admin, get_db
from services.site_settings_service import SiteSettingsService
import schemas

router = APIRouter()
site_settings_service = SiteSettingsService()


@router.get("/public", response_model=schemas.SiteSettings)
def get_public_site_settings(db: Session = Depends(get_db)):
    return site_settings_service.get_settings(db)


@router.get("/admin", response_model=schemas.SiteSettings)
def get_admin_site_settings(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return site_settings_service.get_settings(db)


@router.patch("/admin", response_model=schemas.SiteSettings)
def update_admin_site_settings(
    payload: schemas.SiteSettingsPatch,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return site_settings_service.update_settings(db, payload)

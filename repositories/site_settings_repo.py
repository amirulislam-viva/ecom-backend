from sqlalchemy.orm import Session

from .base_repo import BaseRepository
import models


class SiteSettingsRepository(BaseRepository[models.SiteSettings]):
    def __init__(self):
        super().__init__(models.SiteSettings)

    def get_singleton(self, db: Session) -> models.SiteSettings | None:
        return db.query(self.model).order_by(self.model.id.asc()).first()

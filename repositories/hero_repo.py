from .base_repo import BaseRepository
import models

class HeroRepository(BaseRepository[models.HeroSection]):
    def __init__(self):
        super().__init__(models.HeroSection)

import json
from sqlalchemy.orm import Session

from repositories.site_settings_repo import SiteSettingsRepository
import models
import schemas


DEFAULT_QUICK_LINKS = [
    {"label": "About Us", "href": "#"},
    {"label": "Contact Us", "href": "#"},
    {"label": "Privacy Policy", "href": "#"},
    {"label": "Terms & Conditions", "href": "#"},
    {"label": "FAQ", "href": "#"},
    {"label": "Shipping Info", "href": "#"},
]

DEFAULT_SUPPORT_FEATURES = [
    {"icon": "truck", "title": "Free Shipping", "description": "On orders over ৳5000"},
    {"icon": "shield", "title": "Genuine Products", "description": "100% authentic brands"},
    {"icon": "clock", "title": "Fast Delivery", "description": "Within 2-5 business days"},
    {"icon": "headphones", "title": "24/7 Support", "description": "Dedicated customer service"},
]

DEFAULT_PAYMENT_METHODS = ["Visa", "Mastercard", "bKash", "Nagad"]


class SiteSettingsService:
    def __init__(self):
        self.repo = SiteSettingsRepository()

    def _serialize_payload(self, payload: dict) -> dict:
        serialized = payload.copy()
        if "quick_links" in payload:
            serialized["quick_links"] = json.dumps(payload.get("quick_links", DEFAULT_QUICK_LINKS))
        if "support_features" in payload:
            serialized["support_features"] = json.dumps(payload.get("support_features", DEFAULT_SUPPORT_FEATURES))
        if "payment_methods" in payload:
            serialized["payment_methods"] = json.dumps(payload.get("payment_methods", DEFAULT_PAYMENT_METHODS))
        return serialized

    def _ensure_settings(self, db: Session) -> models.SiteSettings:
        settings = self.repo.get_singleton(db)
        if settings:
            return settings

        defaults = schemas.SiteSettingsUpdate().model_dump()
        settings = self.repo.create(db, self._serialize_payload(defaults))
        return settings

    def _to_response(self, settings: models.SiteSettings) -> schemas.SiteSettings:
        return schemas.SiteSettings(
            id=settings.id,
            site_name=settings.site_name,
            site_tagline=settings.site_tagline,
            admin_panel_title=settings.admin_panel_title,
            home_nav_label=settings.home_nav_label,
            brands_nav_label=settings.brands_nav_label,
            track_order_label=settings.track_order_label,
            contact_phone=settings.contact_phone,
            contact_email=settings.contact_email,
            promotional_banner_text=settings.promotional_banner_text,
            search_placeholder=settings.search_placeholder,
            mobile_search_placeholder=settings.mobile_search_placeholder,
            hero_badge_text=settings.hero_badge_text,
            categories_section_title=settings.categories_section_title,
            categories_section_subtitle=settings.categories_section_subtitle,
            brands_section_title=settings.brands_section_title,
            brands_section_subtitle=settings.brands_section_subtitle,
            featured_section_title=settings.featured_section_title,
            featured_section_subtitle=settings.featured_section_subtitle,
            featured_cta_label=settings.featured_cta_label,
            newsletter_title=settings.newsletter_title,
            newsletter_subtitle=settings.newsletter_subtitle,
            newsletter_button_text=settings.newsletter_button_text,
            footer_description=settings.footer_description,
            footer_address=settings.footer_address,
            footer_copyright=settings.footer_copyright,
            facebook_url=settings.facebook_url,
            instagram_url=settings.instagram_url,
            youtube_url=settings.youtube_url,
            quick_links=json.loads(settings.quick_links or "[]"),
            support_features=json.loads(settings.support_features or "[]"),
            payment_methods=json.loads(settings.payment_methods or "[]"),
        )

    def get_settings(self, db: Session) -> schemas.SiteSettings:
        settings = self._ensure_settings(db)
        return self._to_response(settings)

    def update_settings(self, db: Session, payload: schemas.SiteSettingsPatch) -> schemas.SiteSettings:
        settings = self._ensure_settings(db)
        update_data = payload.model_dump(exclude_unset=True)
        if not update_data:
            return self._to_response(settings)

        updated = self.repo.update(db, settings.id, self._serialize_payload(update_data))
        return self._to_response(updated)

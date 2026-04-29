from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str
    slug: str
    level: int = 0
    parent_id: Optional[int] = None
    image: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True

class BrandBase(BaseModel):
    name: str
    logo_url: str

class BrandCreate(BrandBase):
    pass

class Brand(BrandBase):
    id: int

    class Config:
        from_attributes = True

class ProductImageBase(BaseModel):
    image_url: str
    sort_order: int = 0

class ProductImageCreate(ProductImageBase):
    pass

class ProductImage(ProductImageBase):
    id: int
    product_id: int

    class Config:
        from_attributes = True

class ProductImageReorder(BaseModel):
    image_ids: List[int]  # ordered list of image IDs representing the desired sort order

from pydantic import BaseModel, field_validator, model_validator

class ProductBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    price: float
    original_price: Optional[float] = None
    in_stock: bool = True
    category_id: int
    brand_id: int

    @model_validator(mode='after')
    def check_prices(self):
        if self.original_price is not None and self.price > self.original_price:
            raise ValueError("Selling price cannot be greater than original price")
        return self

class ProductCreate(ProductBase):
    image_urls: List[str] = []

class Product(ProductBase):
    id: int
    category: Optional[Category] = None
    brand: Optional[Brand] = None
    images: List[ProductImage] = []

    class Config:
        from_attributes = True

class HeroSectionBase(BaseModel):
    title: str
    subtitle: str
    image_url: str
    button_text: str
    button_link: str
    is_active: bool = True

class HeroSectionCreate(HeroSectionBase):
    pass

class HeroSection(HeroSectionBase):
    id: int

    class Config:
        from_attributes = True

class FeaturedProductBase(BaseModel):
    product_id: int
    sort_order: int = 0

class FeaturedProductCreate(FeaturedProductBase):
    pass

class FeaturedProduct(FeaturedProductBase):
    id: int
    product: Optional[Product] = None

    class Config:
        from_attributes = True

class SiteLink(BaseModel):
    label: str
    href: str

class SiteFeature(BaseModel):
    icon: str
    title: str
    description: str

class SiteSettingsBase(BaseModel):
    site_name: str = "Super Tools"
    site_tagline: str = "Bangladesh"
    admin_panel_title: str = "Admin Panel"
    home_nav_label: str = "Home"
    brands_nav_label: str = "Brands"
    track_order_label: str = "Track Order"
    contact_phone: str = "+880 1234-567890"
    contact_email: str = "info@supertoolsbd.com"
    promotional_banner_text: str = "Free Shipping on Orders Over ৳5000"
    search_placeholder: str = "Search for tools, brands, categories..."
    mobile_search_placeholder: str = "Search for tools..."
    hero_badge_text: str = "Featured Brand"
    categories_section_title: str = "All Products"
    categories_section_subtitle: str = "Browse our comprehensive collection of professional-grade power tools and equipment"
    brands_section_title: str = "Brands"
    brands_section_subtitle: str = "Showcasing reputed brands of the Bangladesh market"
    featured_section_title: str = "Featured Products"
    featured_section_subtitle: str = "Top picks from our collection"
    featured_cta_label: str = "View All Products"
    newsletter_title: str = "Subscribe to Our Newsletter"
    newsletter_subtitle: str = "Get updates on new products and exclusive offers"
    newsletter_button_text: str = "Subscribe"
    footer_description: str = "Your trusted source for professional-grade power tools and equipment in Bangladesh. We bring you the best brands at competitive prices."
    footer_address: str = "123 Tools Market, Elephant Road, Dhaka-1205, Bangladesh"
    footer_copyright: str = "© 2026 Super Tools Bangladesh. All rights reserved."
    facebook_url: str = "#"
    instagram_url: str = "#"
    youtube_url: str = "#"
    quick_links: List[SiteLink] = [
        SiteLink(label="About Us", href="#"),
        SiteLink(label="Contact Us", href="#"),
        SiteLink(label="Privacy Policy", href="#"),
        SiteLink(label="Terms & Conditions", href="#"),
        SiteLink(label="FAQ", href="#"),
        SiteLink(label="Shipping Info", href="#"),
    ]
    support_features: List[SiteFeature] = [
        SiteFeature(icon="truck", title="Free Shipping", description="On orders over ৳5000"),
        SiteFeature(icon="shield", title="Genuine Products", description="100% authentic brands"),
        SiteFeature(icon="clock", title="Fast Delivery", description="Within 2-5 business days"),
        SiteFeature(icon="headphones", title="24/7 Support", description="Dedicated customer service"),
    ]
    payment_methods: List[str] = ["Visa", "Mastercard", "bKash", "Nagad"]

class SiteSettingsUpdate(SiteSettingsBase):
    pass

class SiteSettingsPatch(BaseModel):
    site_name: Optional[str] = None
    site_tagline: Optional[str] = None
    admin_panel_title: Optional[str] = None
    home_nav_label: Optional[str] = None
    brands_nav_label: Optional[str] = None
    track_order_label: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    promotional_banner_text: Optional[str] = None
    search_placeholder: Optional[str] = None
    mobile_search_placeholder: Optional[str] = None
    hero_badge_text: Optional[str] = None
    categories_section_title: Optional[str] = None
    categories_section_subtitle: Optional[str] = None
    brands_section_title: Optional[str] = None
    brands_section_subtitle: Optional[str] = None
    featured_section_title: Optional[str] = None
    featured_section_subtitle: Optional[str] = None
    featured_cta_label: Optional[str] = None
    newsletter_title: Optional[str] = None
    newsletter_subtitle: Optional[str] = None
    newsletter_button_text: Optional[str] = None
    footer_description: Optional[str] = None
    footer_address: Optional[str] = None
    footer_copyright: Optional[str] = None
    facebook_url: Optional[str] = None
    instagram_url: Optional[str] = None
    youtube_url: Optional[str] = None
    quick_links: Optional[List[SiteLink]] = None
    support_features: Optional[List[SiteFeature]] = None
    payment_methods: Optional[List[str]] = None

class SiteSettings(SiteSettingsBase):
    id: int

    class Config:
        from_attributes = True

class OrderItemBase(BaseModel):
    product_id: int
    product_name: str
    product_image: Optional[str] = None
    quantity: int
    price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    order_id: int

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    track_id: str
    customer_name: str
    mobile_number: str
    address: str
    city: str
    notes: Optional[str] = None
    subtotal: float
    shipping_cost: float
    total: float
    payment_method: str = "cash_on_delivery"
    status: str = "pending"

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderStatusUpdate(BaseModel):
    status: str

class Order(OrderBase):
    id: int
    created_at: datetime
    items: List[OrderItem] = []

    class Config:
        from_attributes = True

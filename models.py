from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Text, DateTime
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    slug = Column(String, unique=True, index=True)
    level = Column(Integer, default=0)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    image = Column(String, nullable=True)

    products = relationship("Product", back_populates="category")
    parent = relationship("Category", remote_side=[id])
    children = relationship("Category", back_populates="parent")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    slug = Column(String, unique=True, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float)
    original_price = Column(Float, nullable=True)
    in_stock = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    brand_id = Column(Integer, ForeignKey("brands.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    category = relationship("Category", back_populates="products")
    brand = relationship("Brand", back_populates="products")
    images = relationship("ProductImage", back_populates="product", order_by="ProductImage.sort_order", cascade="all, delete-orphan")


class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    image_url = Column(String, nullable=False)
    sort_order = Column(Integer, default=0)

    product = relationship("Product", back_populates="images")

class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    logo_url = Column(String)

    products = relationship("Product", back_populates="brand")  

class HeroSection(Base):
    __tablename__ = "hero_sections"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    subtitle = Column(String)
    image_url = Column(String)
    button_text = Column(String)
    button_link = Column(String)
    is_active = Column(Boolean, default=True)

class FeaturedProduct(Base):
    __tablename__ = "featured_products"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    sort_order = Column(Integer, default=0)

    product = relationship("Product")

class SiteSettings(Base):
    __tablename__ = "site_settings"

    id = Column(Integer, primary_key=True, index=True)
    site_name = Column(String, default="Super Tools")
    site_tagline = Column(String, default="Bangladesh")
    admin_panel_title = Column(String, default="Admin Panel")
    home_nav_label = Column(String, default="Home")
    brands_nav_label = Column(String, default="Brands")
    track_order_label = Column(String, default="Track Order")
    contact_phone = Column(String, default="+880 1234-567890")
    contact_email = Column(String, default="info@supertoolsbd.com")
    promotional_banner_text = Column(String, default="Free Shipping on Orders Over ৳5000")
    search_placeholder = Column(String, default="Search for tools, brands, categories...")
    mobile_search_placeholder = Column(String, default="Search for tools...")
    hero_badge_text = Column(String, default="Featured Brand")
    categories_section_title = Column(String, default="All Products")
    categories_section_subtitle = Column(Text, default="Browse our comprehensive collection of professional-grade power tools and equipment")
    brands_section_title = Column(String, default="Brands")
    brands_section_subtitle = Column(Text, default="Showcasing reputed brands of the Bangladesh market")
    featured_section_title = Column(String, default="Featured Products")
    featured_section_subtitle = Column(Text, default="Top picks from our collection")
    featured_cta_label = Column(String, default="View All Products")
    newsletter_title = Column(String, default="Subscribe to Our Newsletter")
    newsletter_subtitle = Column(Text, default="Get updates on new products and exclusive offers")
    newsletter_button_text = Column(String, default="Subscribe")
    footer_description = Column(Text, default="Your trusted source for professional-grade power tools and equipment in Bangladesh. We bring you the best brands at competitive prices.")
    footer_address = Column(Text, default="123 Tools Market, Elephant Road, Dhaka-1205, Bangladesh")
    footer_copyright = Column(String, default="© 2026 Super Tools Bangladesh. All rights reserved.")
    facebook_url = Column(String, default="#")
    instagram_url = Column(String, default="#")
    youtube_url = Column(String, default="#")
    quick_links = Column(Text, default="[]")
    support_features = Column(Text, default="[]")
    payment_methods = Column(Text, default="[]")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    track_id = Column(String, unique=True, index=True)
    customer_name = Column(String)
    mobile_number = Column(String, index=True)
    address = Column(Text)
    city = Column(String)
    notes = Column(Text, nullable=True)
    subtotal = Column(Float)
    shipping_cost = Column(Float)
    total = Column(Float)
    payment_method = Column(String, default="cash_on_delivery")
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    product_name = Column(String)
    product_image = Column(String, nullable=True)
    quantity = Column(Integer)
    price = Column(Float)

    order = relationship("Order", back_populates="items")

import os
import shutil
import uuid
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from core.security import get_password_hash

def furnish_data():
    db = SessionLocal()
    try:
        # Create uploads directory and clean it
        if os.path.exists("uploads"):
            shutil.rmtree("uploads")
        os.makedirs("uploads", exist_ok=True)
        
        def copy_to_uploads(src_path):
            if not os.path.exists(src_path):
                # Return a placeholder if public images don't exist
                return f"https://images.unsplash.com/photo-1581092160562-40aa08e78837?auto=format&fit=crop&q=80&w=800"
            ext = os.path.splitext(src_path)[1]
            filename = f"{uuid.uuid4()}{ext}"
            shutil.copy(src_path, os.path.join("uploads", filename))
            return f"/uploads/{filename}"

        images_dir = "../frontend/public/images"
        
        # 1. Brands
        brands_data = [
            {"name": "CROWN", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Target_Corporation_logo_%28vector%29.svg/1024px-Target_Corporation_logo_%28vector%29.svg.png"},
            {"name": "TOTAL", "logo_url": "https://upload.wikimedia.org/wikipedia/en/thumb/e/e4/TotalEnergies_logo.svg/1200px-TotalEnergies_logo.svg.png"},
            {"name": "BOSCH", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/Bosch-logo.svg/1200px-Bosch-logo.svg.png"},
            {"name": "INGCO", "logo_url": "https://ingco.com/wp-content/themes/ingco/assets/img/logo.png"},
        ]
        
        brands = []
        for b_data in brands_data:
            brand = models.Brand(**b_data)
            db.add(brand)
            db.flush()
            brands.append(brand)

        # 2. Categories
        categories_data = [
            {"name": "Wood Works", "slug": "wood-works", "image": copy_to_uploads(f"{images_dir}/category-wood.jpg")},
            {"name": "Construction", "slug": "construction", "image": copy_to_uploads(f"{images_dir}/category-construction.jpg")},
            {"name": "Automotive", "slug": "automotive", "image": copy_to_uploads(f"{images_dir}/category-automotive.jpg")},
            {"name": "Hand Tools", "slug": "hand-tools", "image": copy_to_uploads(f"{images_dir}/category-handtools.jpg")},
        ]
        
        categories = []
        for c_data in categories_data:
            cat = models.Category(**c_data, level=0)
            db.add(cat)
            db.flush()
            categories.append(cat)

        # 3. Products
        products_data = [
            {"name": "Rotary Drill", "slug": "rotary-drill", "price": 4500, "original_price": 5200, "category_id": categories[1].id, "brand_id": brands[0].id, "img_src": f"{images_dir}/product-drill.jpg"},
            {"name": "Angle Grinder", "slug": "angle-grinder", "price": 3800, "original_price": 4500, "category_id": categories[1].id, "brand_id": brands[1].id, "img_src": f"{images_dir}/product-grinder.jpg"},
            {"name": "Jig Saw", "slug": "jig-saw", "price": 5200, "original_price": 6000, "category_id": categories[0].id, "brand_id": brands[2].id, "img_src": f"{images_dir}/product-jigsaw.jpg"},
            {"name": "Impact Wrench", "slug": "impact-wrench", "price": 8500, "original_price": 9800, "category_id": categories[2].id, "brand_id": brands[3].id, "img_src": f"{images_dir}/product-wrench.jpg"},
            {"name": "Circular Saw", "slug": "circular-saw", "price": 7200, "original_price": 8500, "category_id": categories[0].id, "brand_id": brands[0].id, "img_src": f"{images_dir}/product-drill.jpg"},
            {"name": "Heat Gun", "slug": "heat-gun", "price": 2500, "original_price": 3200, "category_id": categories[1].id, "brand_id": brands[1].id, "img_src": f"{images_dir}/product-grinder.jpg"},
            {"name": "Planer", "slug": "planer", "price": 6800, "original_price": 7500, "category_id": categories[0].id, "brand_id": brands[2].id, "img_src": f"{images_dir}/product-jigsaw.jpg"},
            {"name": "Impact Drill", "slug": "impact-drill", "price": 4200, "original_price": 4800, "category_id": categories[1].id, "brand_id": brands[3].id, "img_src": f"{images_dir}/product-drill.jpg"},
        ]
        
        products = []
        for p_data in products_data:
            img_src = p_data.pop("img_src")
            prod = models.Product(**p_data, in_stock=True)
            db.add(prod)
            db.flush()
            
            # Add images to gallery
            url = copy_to_uploads(img_src)
            db_img = models.ProductImage(product_id=prod.id, image_url=url, sort_order=0)
            db.add(db_img)
            
            # Add a second dummy image for gallery demo
            dummy_url = "https://images.unsplash.com/photo-1572981779307-38b8cabb2407?auto=format&fit=crop&q=80&w=800"
            db_img2 = models.ProductImage(product_id=prod.id, image_url=dummy_url, sort_order=1)
            db.add(db_img2)
            
            products.append(prod)

        # 4. Hero Section
        hero_data = [
            {"title": "CROWN Professional", "subtitle": "State of the Art Power Tools", "image_url": copy_to_uploads(f"{images_dir}/banner-crown.jpg"), "button_text": "Shop Now", "button_link": "/products", "is_active": True},
            {"title": "TOTAL One-Stop", "subtitle": "One-Stop Tools Station", "image_url": copy_to_uploads(f"{images_dir}/banner-total.jpg"), "button_text": "Explore", "button_link": "/products", "is_active": True},
        ]
        
        for h_data in hero_data:
            hero = models.HeroSection(**h_data)
            db.add(hero)

        # 5. Featured Products
        for i, prod in enumerate(products[:4]):
            featured = models.FeaturedProduct(product_id=prod.id, sort_order=i)
            db.add(featured)

        # 6. Admin User
        admin_user = models.User(
            username="admin",
            hashed_password=get_password_hash("admin123")
        )
        db.add(admin_user)

        db.commit()
        print("Database furnished successfully with demo data and images.")
    except Exception as e:
        db.rollback()
        print(f"Error furnishing data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    furnish_data()

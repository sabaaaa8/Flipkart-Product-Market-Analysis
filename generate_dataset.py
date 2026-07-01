"""
Dataset generator for Flipkart Product Market Analysis
Generates a realistic CSV with 1000+ rows
"""

import pandas as pd
import numpy as np
import random
import os

random.seed(42)
np.random.seed(42)

# --- Realistic data pools ---
categories = {
    "Electronics": {
        "sub": ["Smartphones", "Laptops", "Tablets", "Cameras", "Headphones", "Smartwatches"],
        "brands": ["Samsung", "Apple", "OnePlus", "Xiaomi", "Realme", "Oppo", "Vivo", "Sony", "LG", "Motorola"],
        "price_range": (5000, 150000),
    },
    "Fashion": {
        "sub": ["Men's Clothing", "Women's Clothing", "Footwear", "Accessories", "Bags"],
        "brands": ["Nike", "Adidas", "Puma", "Levi's", "H&M", "Zara", "FabIndia", "W", "Allen Solly", "Van Heusen"],
        "price_range": (299, 15000),
    },
    "Home & Kitchen": {
        "sub": ["Kitchen Appliances", "Furniture", "Decor", "Bedding", "Cleaning"],
        "brands": ["Prestige", "Bajaj", "Philips", "Havells", "Morphy Richards", "Milton", "Cello", "Bosch", "Inalsa", "Usha"],
        "price_range": (500, 80000),
    },
    "Beauty": {
        "sub": ["Skincare", "Haircare", "Makeup", "Fragrances", "Personal Care"],
        "brands": ["Lakme", "Maybelline", "L'Oreal", "Nivea", "Dove", "Biotique", "Himalaya", "Neutrogena", "Mamaearth", "WOW"],
        "price_range": (99, 5000),
    },
    "Books": {
        "sub": ["Fiction", "Non-Fiction", "Self Help", "Educational", "Comics"],
        "brands": ["Penguin", "Harper Collins", "Scholastic", "Oxford", "Arihant", "S. Chand", "Rupa", "Westland", "Bloomsbury", "Pan Macmillan"],
        "price_range": (99, 1500),
    },
    "Sports": {
        "sub": ["Cricket", "Football", "Fitness", "Yoga", "Cycling"],
        "brands": ["Decathlon", "Nivia", "SG", "SS", "Cosco", "Yonex", "Head", "Wilson", "Reebok", "Speedo"],
        "price_range": (299, 30000),
    },
    "Toys": {
        "sub": ["Board Games", "Action Figures", "Educational Toys", "Outdoor Toys", "Dolls"],
        "brands": ["Lego", "Hasbro", "Mattel", "Fisher-Price", "Funskool", "Chhota Bheem", "Hot Wheels", "Barbie", "Nerf", "Playmobil"],
        "price_range": (199, 8000),
    },
    "Groceries": {
        "sub": ["Snacks", "Beverages", "Dairy", "Staples", "Organic"],
        "brands": ["Amul", "Britannia", "Nestle", "ITC", "Dabur", "Haldiram's", "Patanjali", "MDH", "Tata", "Kissan"],
        "price_range": (29, 1500),
    },
}

sellers = [
    "RetailWorld", "TechZone", "QuickMart", "BestDeals", "FlashSale",
    "PrimeSeller", "ValueStore", "TopBrands", "MegaMart", "ShopKart",
    "DailyDeals", "SuperStore", "EliteSeller", "BrandHub", "SmartBuy",
]

product_name_templates = {
    "Smartphones": ["Pro Max", "Ultra", "5G", "Lite", "Plus", "Neo", "Edge", "X", "S", "Note"],
    "Laptops": ["Laptop", "Notebook", "Book", "Pro", "Air", "Slim", "Gaming", "Ultra"],
    "Tablets": ["Tab", "Pad", "Slate", "Air", "Pro"],
    "Cameras": ["DSLR", "Mirrorless", "Action Cam", "360 Cam", "Compact"],
    "Headphones": ["Earbuds", "Over-ear", "Neckband", "ANC Headphones", "TWS"],
    "Smartwatches": ["Smartwatch", "Fitness Band", "Watch Pro", "Sport Band"],
    "Men's Clothing": ["T-Shirt", "Jeans", "Shirt", "Kurta", "Jacket", "Shorts"],
    "Women's Clothing": ["Kurti", "Saree", "Dress", "Top", "Lehenga", "Blouse"],
    "Footwear": ["Sneakers", "Sandals", "Boots", "Loafers", "Slippers", "Heels"],
    "Accessories": ["Watch", "Belt", "Wallet", "Sunglasses", "Cap", "Scarf"],
    "Bags": ["Backpack", "Handbag", "Trolley", "Sling Bag", "Tote"],
    "Kitchen Appliances": ["Mixer Grinder", "Induction Cooktop", "Air Fryer", "Microwave", "Toaster", "Juicer"],
    "Furniture": ["Sofa", "Bed", "Table", "Chair", "Wardrobe", "Bookshelf"],
    "Decor": ["Wall Art", "Lamp", "Vase", "Cushion", "Candle", "Frame"],
    "Bedding": ["Bed Sheet", "Pillow", "Blanket", "Duvet", "Mattress"],
    "Cleaning": ["Mop", "Vacuum Cleaner", "Broom", "Dustbin", "Detergent"],
    "Skincare": ["Face Wash", "Moisturizer", "Sunscreen", "Serum", "Toner", "Face Mask"],
    "Haircare": ["Shampoo", "Conditioner", "Hair Oil", "Hair Mask", "Hair Serum"],
    "Makeup": ["Lipstick", "Foundation", "Mascara", "Eyeliner", "Blush", "Concealer"],
    "Fragrances": ["Perfume", "Deodorant", "Body Mist", "Attar", "EDT"],
    "Personal Care": ["Body Wash", "Soap", "Toothbrush", "Razor", "Trimmer"],
    "Fiction": ["Novel", "Thriller", "Mystery", "Romance", "Sci-Fi"],
    "Non-Fiction": ["Biography", "History", "Science", "Politics", "Economics"],
    "Self Help": ["Motivation", "Productivity", "Leadership", "Mindset", "Finance"],
    "Educational": ["Textbook", "Guide", "Workbook", "Practice Papers", "Reference"],
    "Comics": ["Manga", "Graphic Novel", "Comic Book", "Strip Collection"],
    "Cricket": ["Cricket Bat", "Cricket Ball", "Pads", "Gloves", "Helmet"],
    "Football": ["Football", "Shin Guards", "Jersey", "Boots", "Goalkeeper Gloves"],
    "Fitness": ["Dumbbells", "Resistance Band", "Treadmill", "Pull-up Bar", "Jump Rope"],
    "Yoga": ["Yoga Mat", "Yoga Block", "Yoga Strap", "Yoga Wheel", "Bolster"],
    "Cycling": ["Cycle", "Helmet", "Gloves", "Lock", "Water Bottle"],
    "Board Games": ["Chess", "Ludo", "Scrabble", "Monopoly", "Uno"],
    "Action Figures": ["Superhero Figure", "Robot", "Car", "Army Set", "Dinosaur"],
    "Educational Toys": ["Puzzle", "Building Blocks", "Science Kit", "Math Game", "Flash Cards"],
    "Outdoor Toys": ["Frisbee", "Kite", "Water Gun", "Bat Ball Set", "Badminton Set"],
    "Dolls": ["Barbie", "Baby Doll", "Soft Toy", "Puppet", "Fashion Doll"],
    "Snacks": ["Chips", "Biscuits", "Cookies", "Popcorn", "Namkeen"],
    "Beverages": ["Juice", "Energy Drink", "Tea", "Coffee", "Health Drink"],
    "Dairy": ["Milk", "Cheese", "Butter", "Curd", "Paneer"],
    "Staples": ["Rice", "Flour", "Sugar", "Salt", "Lentils"],
    "Organic": ["Organic Honey", "Organic Ghee", "Organic Oil", "Organic Spices", "Organic Tea"],
}


def generate_product_name(brand, sub_category):
    """Generate a realistic product name."""
    templates = product_name_templates.get(sub_category, ["Product"])
    variant = random.choice(templates)
    model_num = random.choice(["", f" {random.randint(10, 99)}", f" {random.choice(['Pro', 'Plus', 'Lite', 'Max', 'Ultra', 'SE'])}"])
    return f"{brand} {variant}{model_num}"


def generate_dataset(n=1100):
    """Generate a realistic Flipkart products dataset."""
    rows = []
    product_id = 1000

    cat_names = list(categories.keys())
    weights = [0.25, 0.18, 0.14, 0.10, 0.08, 0.08, 0.07, 0.10]  # realistic distribution

    for _ in range(n):
        cat = random.choices(cat_names, weights=weights, k=1)[0]
        cat_data = categories[cat]
        sub_cat = random.choice(cat_data["sub"])
        brand = random.choice(cat_data["brands"])
        price_min, price_max = cat_data["price_range"]

        original_price = round(random.uniform(price_min, price_max), -1)
        discount_pct = random.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70])
        price = round(original_price * (1 - discount_pct / 100), 2)

        rating = round(random.gauss(3.9, 0.7), 1)
        rating = max(1.0, min(5.0, rating))

        review_count = int(np.random.exponential(scale=500))
        review_count = max(5, min(50000, review_count))

        availability = random.choices(["In Stock", "Out of Stock", "Limited Stock"], weights=[0.70, 0.15, 0.15])[0]
        stock_status = "Available" if availability == "In Stock" else ("Sold Out" if availability == "Out of Stock" else "Low Stock")

        delivery_days = random.choices([1, 2, 3, 5, 7, 10], weights=[0.10, 0.25, 0.30, 0.20, 0.10, 0.05])[0]

        popularity = round(random.gauss(65, 20), 1)
        popularity = max(1.0, min(100.0, popularity))

        rows.append({
            "Product_ID": f"FLP{product_id}",
            "Product_Name": generate_product_name(brand, sub_cat),
            "Brand": brand,
            "Category": cat,
            "Sub_Category": sub_cat,
            "Price": price,
            "Original_Price": original_price,
            "Discount_Percentage": discount_pct,
            "Rating": rating,
            "Review_Count": review_count,
            "Availability": availability,
            "Seller": random.choice(sellers),
            "Delivery_Days": delivery_days,
            "Product_Popularity": popularity,
            "Stock_Status": stock_status,
        })
        product_id += 1

    df = pd.DataFrame(rows)
    return df


if __name__ == "__main__":
    df = generate_dataset(1100)
    out_path = os.path.join(os.path.dirname(__file__), "flipkart_products.csv")
    df.to_csv(out_path, index=False)
    print(f"Dataset saved: {out_path}  ({len(df)} rows)")

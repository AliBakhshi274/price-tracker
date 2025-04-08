from app import db, app
import os
import random
from datetime import timedelta, datetime
from io import BytesIO
from PIL import Image
import requests
from faker import Faker
from app.models import Product, PriceHistory

faker = Faker()

products_data = [
    {"name": "Samsung Galaxy Tab S8", "category": "Tablet"},
    {"name": "iPad Pro 12.9", "category": "Tablet"},
    {"name": "Lenovo ThinkPad X1", "category": "Laptop"},
    {"name": "MacBook Pro 14", "category": "Laptop"},
    {"name": "iPhone 15 Pro", "category": "Mobile"},
    {"name": "Xiaomi 13 Pro", "category": "Mobile"}
]

image_urls = [
    "https://m.media-amazon.com/images/I/715AVcfGf2L._AC_UY218_.jpg",
    "https://m.media-amazon.com/images/I/7147JzEtrqL._AC_UY218_.jpg",
    "https://m.media-amazon.com/images/I/61O5ClCxRXL._AC_UY218_.jpg",
    "https://m.media-amazon.com/images/I/61-oTP1X4rL._AC_UY218_.jpg",
    "https://m.media-amazon.com/images/I/61WUSYIQdKL._AC_UY218_.jpg",
    "https://m.media-amazon.com/images/I/51ujrY0Md7L._AC_UY218_.jpg"
]

def download_image(url, save_path):
    response = requests.get(url)
    response.raise_for_status()
    img = Image.open(BytesIO(response.content))
    img.save(save_path)
    return save_path

def generate_fake_prices(base_price):
    prices = []
    for i in range(4 * 30):
        date = datetime.now() - timedelta(days=(4*30) - i)
        fluctuation = random.uniform(-0.5, 0.5)
        price = round(base_price * (1 + fluctuation), 2)
        prices.append(
            {
                "price": f"${price}",
                "date": date,
            }
        )
    return prices

def seed_database():
    with app.app_context():

        PriceHistory.query.delete()
        Product.query.delete()
        db.session.commit()

        for i, product_info in enumerate(products_data):
            # img_path = f"app/static/images/product_{i}.jpg"
            # download_image(image_urls[i],img_path)

            base_price = random.uniform(300, 1500)

            product = Product(
                name = product_info["name"],
                category = product_info["category"],
                image_file = image_urls[i],
                last_updated = datetime.now(),
            )
            db.session.add(product)
            db.session.commit()

            prices = generate_fake_prices(base_price)
            for price_data in prices:
                price_history = PriceHistory(
                    product_id= product.id,
                    price = price_data["price"],
                    date = price_data["date"],
                )
                db.session.add(price_history)
            db.session.commit()

if __name__ == "__main__":
    os.makedirs("../app/static/images", exist_ok=True)
    seed_database()
    print("Fake data generation completed!...")

#scrape on amazon
    # scrape_amazon("tab samsung s10 plus", "Tablet")
    # scrape_amazon("Galaxy s25 ultra", "Mobile")
    # scrape_amazon("ps5", "Game")
    # scrape_amazon("Iphone 15 pro", "Mobile")
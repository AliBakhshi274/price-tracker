from app import db, app
from app.models import Product
from faker import Faker
import random

faker = Faker()
categories = ['Sport', 'Drink', 'Fruit', 'Country', 'Farm', 'Job']

with app.test_request_context():

    Product.query.delete()

    for i in range(1000):
        name = faker.name()
        description = faker.paragraph()
        price = round(random.uniform(10, 100), 2)
        category = random.choice(categories)
        image_file = faker.image_url(width=300, height=300)
        product = Product(name=name, description=description, price=price, category=category, image_file=image_file)
        db.session.add(product)
    db.session.commit()
    print("Database seeds done!")

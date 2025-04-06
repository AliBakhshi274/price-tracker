import re
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(
            password=password,
            method='pbkdf2:sha256',
            salt_length=8,
        )

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image_file = db.Column(db.String(200), nullable=False, default='default.jpg')
    last_updated = db.Column(db.DateTime, nullable=False)

    @property
    def clean_name(self):
        if not self.name:
            return ""
        parts = re.split(r'[,|\-_]', self.name, maxsplit=1)
        return parts[0] if parts else self.name

    @property
    def display_name(self):
        name = self.clean_name
        return f"{name[:30]}..." if len(name) > 30 else name

    def __repr__(self):
        return f"Product(name={self.name}, last_updated={self.last_updated}, category={self.category})"

class PriceHistory(db.Model):
    __tablename__ = 'price_history'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    price = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    product = db.relationship('Product', backref=db.backref('PriceHistory', lazy=True))

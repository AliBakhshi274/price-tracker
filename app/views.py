"""
- set methods relevant to views
"""

from datetime import datetime, timedelta, timezone
from app.models import Product, PriceHistory

# show chart for product_id's details
def product_chart(product_id):
    product = Product.query.get(product_id)
    last_7_days = datetime.now(timezone.utc) - timedelta(days=7)
    history = PriceHistory.query.filter(
        PriceHistory.product_id == product_id,
        PriceHistory.date >= last_7_days
    ).order_by(PriceHistory.date.asc()).all()
    print(f"history: {history}")

    chart_data = {
        'labels': [entry.date.strftime('%Y-%m-%d %H:%M') for entry in history],
        'prices': [entry.price.split("$")[1] for entry in history],
        'product_name': product.name,
    }

    return product, chart_data

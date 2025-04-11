from datetime import datetime, timedelta, timezone
from app.models import Product, PriceHistory
from ml.price_predictor import predict_price


def common_product_chart(product_id):
    product = Product.query.get(product_id)
    last_4_month = (datetime.now(timezone.utc) - timedelta(days=4 * 30)).replace(tzinfo=None)
    history = PriceHistory.query.filter(
        PriceHistory.product_id == product_id,
        PriceHistory.date >= last_4_month
    ).order_by(PriceHistory.date.asc()).all()
    yesterday = (datetime.now() - timedelta(days=1)).date()

    common_chart_date = {
        'labels': [entry.date.strftime('%Y-%m-%d') for entry in history if entry.date.day==1 or entry.date.date()==yesterday],
        'prices': [entry.price for entry in history if entry.date.day==1 or entry.date.date()==yesterday],
        'product_name': product.name,
    }

    return product, common_chart_date

def forecast_product_chart(product_id):
    # list of prices for 7 days later
    next_7_days_prices = predict_price(product_id)

    labels = []
    today = datetime.now(timezone.utc)
    # today's price ignored
    for i in range(1, 8):
        labels.append((today + timedelta(days=i)).replace(tzinfo=None).strftime('%Y-%m-%d'))

    forecast_data = {
        'labels': labels,
        'prices': next_7_days_prices,
    }

    return forecast_data

















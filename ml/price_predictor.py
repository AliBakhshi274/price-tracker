from datetime import datetime, timedelta, timezone
import numpy as np
from sklearn.linear_model import LinearRegression
from app.models import PriceHistory

# forecast price for 7 days later
def predict_price(product_id, days_ahead=7):
    today = datetime.now(timezone.utc)
    date_of_4_month_ago = (today - timedelta(days=4 * 30)).replace(tzinfo=None)

    prices = PriceHistory.query.filter(
        PriceHistory.product_id == product_id,
        PriceHistory.date >= date_of_4_month_ago
    ).order_by(PriceHistory.date).all()

    x = np.array(
        [(p.date - date_of_4_month_ago).days for p in prices]
    ).reshape(-1, 1)

    y = np.array(
        [p.price for p in prices]
    )

    model = LinearRegression()
    model.fit(x, y)

    future_days = np.array([
        [x[-1][0] + i] for i in range(1, days_ahead + 1)
    ])

    predicted_prices = model.predict(future_days)

    # predict prices for 7 days later
    # predict_prices = []
    # for i in range(0, 7):
    #     temp = round(model.predict(future_days)[i], 2)
    #     predict_prices.append(temp)
    # predicted_price = model.predict(future_day)[0]

    return [round(price, 2) for price in predicted_prices]
















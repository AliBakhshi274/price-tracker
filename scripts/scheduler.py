"""
run job() method every day at 8 o'clock.
"""

import schedule
import time
from app.scrapy_crawler.amazon_scraper import scrape_amazon

def job():
    products = [
        ("tab samsung s10 plus", "Tablet"),
        ("Galaxy s25 ultra", "Mobile"),
        ("ps5", "Game"),
        ("Iphone 15 pro", "Mobile")
    ]

    for product_name, category in products:
        scrape_amazon(product_name, category)

schedule.every().day.at("19:51").do(job)

while True:
    schedule.run_pending()
    time.sleep(10)
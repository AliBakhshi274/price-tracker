from app import app
from app.scrapy_crawler.amazon_scraper import scrape_amazon

with app.app_context():
    scrape_amazon("tab samsung s10 plus", "Tablet")
    scrape_amazon("Galaxy s25 ultra", "Mobile")
    scrape_amazon("ps5", "Game")
    scrape_amazon("Iphone 15 pro", "Mobile")
import random
import time
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from app.models import db, Product, PriceHistory
from datetime import datetime, timezone


def scrape_amazon(product_name, category):
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--start-maximized')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("accept-language=en-US,en;q=0.9")
    options.add_argument("accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
    options.add_argument("referer=https://www.google.com/")
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.geolocation": 1})
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')

    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    })
    wait = WebDriverWait(driver, 10)
    try:
        driver.get("https://www.amazon.com/")

        search_box = driver.find_element(By.ID, "twotabsearchtextbox")

        time.sleep(random.uniform(1, 3))
        search_box.send_keys(product_name)
        time.sleep(random.uniform(0.5, 1.5))
        search_box.send_keys(Keys.RETURN)

        product_element = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.s-main-slot div[data-component-type='s-search-result']"))
        )
        try:
            name = product_element.find_element(By.CSS_SELECTOR, "span h2.a-text-normal span").text
        except NoSuchElementException:
            name = "N/A"
        try:
            temp = product_element.find_element(By.CSS_SELECTOR,
                                                "div.a-section.a-spacing-none.a-spacing-top-mini span.a-color-base").text
            price = float(temp.split('$')[1])
        except NoSuchElementException:
            price = 0
        try:
            image = product_element.find_element(By.CSS_SELECTOR, "img.s-image").get_attribute("src")
        except NoSuchElementException:
            image = "N/A"

        print(f"name: {name}, price: {price}, image: {image}")

        # Insert data in Product db
        product = Product.query.filter_by(name=name).first()
        if not product:
            product = Product(name=name, category=category, image_file=image, last_updated=datetime.now(timezone.utc))
            db.session.add(product)
            db.session.commit()

        # Insert data in PriceHistory
        price_entry = PriceHistory(product_id=product.id, price=price, date=datetime.now(timezone.utc))
        db.session.add(price_entry)
        db.session.commit()

        print(f"insert: {name} / {price}")

    except TimeoutException:
        print("Timeout")
        driver.save_screenshot("timeout_error.png")
    except Exception as e:
        print("unknown error", str(e))
        driver.save_screenshot("unknown_error.png")
    finally:
        driver.quit()

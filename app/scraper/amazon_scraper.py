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
    options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36")
    options.add_argument("accept-language=de-DE,de;q=0.9")
    options.add_argument("geo-location=DE")
    options.add_argument("--timezone=Europe/Berlin")
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.geolocation": 1})
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    try:
        driver.get("https://www.amazon.com/")

        search_box = driver.find_element(By.ID, "twotabsearchtextbox")
        search_box.send_keys(product_name)
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
            price = product_element.find_element(By.CSS_SELECTOR,
                                         "div.a-section.a-spacing-none.a-spacing-top-mini span.a-color-base").text
        except NoSuchElementException:
            price = "N/A"
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

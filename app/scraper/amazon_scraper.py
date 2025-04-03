from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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
    search_box.send_keys("samsung tab s10")
    search_box.send_keys(Keys.ENTER)
    product = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot div[data-component-type='s-search-result']"))
    )
    try:
        name = product.find_element(By.CSS_SELECTOR, "span h2.a-text-normal span").text
    except NoSuchElementException:
        name = "N/A"
    try:
        price = product.find_element(By.CSS_SELECTOR, "div.a-section.a-spacing-none.a-spacing-top-mini span.a-color-base").text
    except NoSuchElementException:
        price = "N/A"
    try:
        image = product.find_element(By.CSS_SELECTOR, "img.s-image").get_attribute("src")
    except NoSuchElementException:
        image = "N/A"

    print(f"name: {name}")
    print(f"price: {price}")
    print(f"image: {image}")

except TimeoutException:
    print("Timeout")
    driver.save_screenshot("timeout_error.png")
except Exception as e:
    print("unknown error", str(e))
    driver.save_screenshot("unknown_error.png")
finally:
    driver.quit()

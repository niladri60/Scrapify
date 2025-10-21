import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_croma(driver, query, pages=None):
    """
    Scrapes product listings from Croma using Selenium (not BeautifulSoup)
    to capture dynamically rendered content.
    """
    print("🛍 Scraping Croma...")
    products = []

    url = f"https://www.croma.com/searchB?q={query}%3Arelevance&text={query}"
    driver.get(url)

    # Wait for products to appear
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.product-item"))
        )
    except:
        print("⚠️ No product container found. Possibly blocked or slow load.")
        return products

    # Scroll down multiple times to trigger JS lazy loading
    last_height = 0
    scroll_round = 0
    print("↕️ Scrolling through Croma page to load products...")
    while True:
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight / 2);")
        time.sleep(random.uniform(2, 4))
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height or scroll_round > 12:
            break
        last_height = new_height
        scroll_round += 1

    time.sleep(3)

    # Now fetch elements directly using Selenium
    product_elements = driver.find_elements(By.CSS_SELECTOR, "li.product-item")

    for item in product_elements:
        try:
            name_tag = item.find_element(By.CSS_SELECTOR, "h3")
            name = name_tag.text.strip() if name_tag else None

            link_tag = item.find_element(By.CSS_SELECTOR, "a")
            link = link_tag.get_attribute("href") if link_tag else None

            price_tag = item.find_element(By.CSS_SELECTOR, "span.new-price")
            price = price_tag.text.replace("₹", "").replace(",", "").strip() if price_tag else None

            brand = name.split()[0] if name else None

            if name and price:
                products.append({
                    "Source": "Croma",
                    "Brand": brand,
                    "Product Name": name,
                    "Price (INR)": price,
                    "Product Link": link
                })
        except Exception:
            continue

    print(f"✅ Finished scraping Croma ({len(products)} items total)")
    return products
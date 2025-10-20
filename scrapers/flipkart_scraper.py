import time
import random
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_flipkart(driver, query, pages):
    print("🛒 Scraping Flipkart...")
    products = []

    for page in range(1, pages + 1):
        url = f"https://www.flipkart.com/search?q={query}&page={page}"
        driver.get(url)

        # ✅ Wait until products load (up to 10 seconds)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "_1AtVbE"))
            )
        except:
            print(f"⚠️ Page {page} took too long to load. Skipping...")
            continue

        # Give a bit more time for dynamic content
        time.sleep(random.uniform(2, 5))

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # ✅ These are all possible containers for products
        product_blocks = soup.find_all("div", {"class": "_1AtVbE"})

        for item in product_blocks:
            # Check multiple possible name classes
            name_tag = (
                item.find("div", {"class": "_4rR01T"}) or  # laptops, phones, etc.
                item.find("a", {"class": "IRpwTa"}) or     # fashion, accessories
                item.find("a", {"class": "s1Q9rs"}) or     # grocery, home items
                item.find("div", {"class": "KzDlHZ"})      # newer UI
            )

            name = name_tag.text.strip() if name_tag else None
            link = None

            # ✅ Extract link safely
            link_tag = item.find("a", href=True)
            if link_tag:
                href = link_tag.get("href")
                if href.startswith("/"):
                    link = "https://www.flipkart.com" + href

            # ✅ Extract price
            price_tag = item.find("div", {"class": "_30jeq3"})
            price = price_tag.text.replace("₹", "").replace(",", "").strip() if price_tag else None

            brand = name.split()[0] if name else None

            if name and price:
                products.append({
                    "Source": "Flipkart",
                    "Brand": brand,
                    "Product Name": name,
                    "Price (INR)": price,
                    "Product Link": link
                })

        print(f"✅ Page {page} scraped ({len(products)} items total so far)")
        time.sleep(random.uniform(2, 5))

    print(f"✅ Finished scraping Flipkart ({len(products)} items total)")
    return products
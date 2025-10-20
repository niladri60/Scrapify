import time
import random
from bs4 import BeautifulSoup

def scrape_croma(driver, query, pages):
    print("🛍 Scraping Croma...")
    products = []

    for page in range(1, pages + 1):
        url = f"https://www.croma.com/search/?text={query}&page={page}"
        driver.get(url)
        time.sleep(random.uniform(3, 6))

        soup = BeautifulSoup(driver.page_source, "html.parser")
        items = soup.find_all("li", class_="product-item")

        for item in items:
            name_tag = item.find("h3")
            name = name_tag.text.strip() if name_tag else None

            link_tag = item.find("a", class_="product__list--name")
            link = "https://www.croma.com" + link_tag.get("href") if link_tag else None

            price_tag = item.find("span", class_="new-price")
            price = None
            if price_tag:
                price = price_tag.text.replace("₹", "").replace(",", "").strip()

            brand = name.split()[0] if name else None

            if name and price:
                products.append({
                    "Source": "Croma",
                    "Brand": brand,
                    "Product Name": name,
                    "Price (INR)": price,
                    "Product Link": link
                })

        time.sleep(random.uniform(2, 5))

    return products

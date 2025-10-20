import time
import random
from bs4 import BeautifulSoup

def scrape_reliance(driver, query, pages):
    print("🛒 Scraping Reliance Digital...")
    products = []

    for page in range(1, pages + 1):
        url = f"https://www.reliancedigital.in/search?q={query}:relevance&page={page}"
        driver.get(url)
        time.sleep(random.uniform(3, 6))

        soup = BeautifulSoup(driver.page_source, "html.parser")
        items = soup.find_all("div", class_="sp__name")

        for item in items:
            name_tag = item.find("a")
            name = name_tag.text.strip() if name_tag else None
            link = "https://www.reliancedigital.in" + name_tag.get("href") if name_tag else None

            # Price extraction
            price_tag = item.find_parent("div", class_="sp__price")
            price = None
            if price_tag:
                price_text = price_tag.text
                price_text = price_text.split("₹")[-1] if "₹" in price_text else None
                price = price_text.replace(",", "").strip() if price_text else None

            brand = name.split()[0] if name else None

            if name and price:
                products.append({
                    "Source": "Reliance Digital",
                    "Brand": brand,
                    "Product Name": name,
                    "Price (INR)": price,
                    "Product Link": link
                })

        time.sleep(random.uniform(2, 5))

    return products

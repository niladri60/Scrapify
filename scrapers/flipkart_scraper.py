import time
import random
from bs4 import BeautifulSoup

def scrape_flipkart(driver, query, pages):
    print("🛒 Scraping Flipkart...")
    products = []

    for page in range(1, pages + 1):
        url = f"https://www.flipkart.com/search?q={query}&page={page}"
        driver.get(url)
        time.sleep(random.uniform(3, 6))

        soup = BeautifulSoup(driver.page_source, "html.parser")

        for item in soup.find_all("div", {"class": "_1AtVbE"}):
            name_tag = item.find("a", {"class": "IRpwTa"})
            if not name_tag:
                name_tag = item.find("a", {"class": "s1Q9rs"})

            name = name_tag.text.strip() if name_tag else None
            link = "https://www.flipkart.com" + name_tag.get("href") if name_tag else None

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

        time.sleep(random.uniform(2, 5))

    return products

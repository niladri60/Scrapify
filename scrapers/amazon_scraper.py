import time
import random
from bs4 import BeautifulSoup

def scrape_amazon(driver, query, pages):
    print("🛒 Scraping Amazon...")
    products = []

    for page in range(1, pages + 1):
        url = f"https://www.amazon.in/s?k={query}&page={page}"
        driver.get(url)
        time.sleep(random.uniform(3, 6))

        soup = BeautifulSoup(driver.page_source, "html.parser")

        for item in soup.find_all("div", {"data-component-type": "s-search-result"}):
            name_tag = item.h2
            name = name_tag.text.strip() if name_tag else None

            link_tag = item.find("a", class_="a-link-normal s-no-outline")
            link = "https://www.amazon.in" + link_tag.get("href") if link_tag else None

            price_whole = item.find("span", class_="a-price-whole")
            price_fraction = item.find("span", class_="a-price-fraction")
            price = None
            if price_whole:
                price = price_whole.text.replace(",", "")
                if price_fraction:
                    price += "." + price_fraction.text

            brand = name.split()[0] if name else None

            if name and price:
                products.append({
                    "Source": "Amazon",
                    "Brand": brand,
                    "Product Name": name,
                    "Price (INR)": price,
                    "Product Link": link
                })

        time.sleep(random.uniform(2, 5))

    return products

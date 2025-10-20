from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import json
import os

# -------------------- LOAD CONFIG --------------------
CONFIG_FILE = "config.json"

if not os.path.exists(CONFIG_FILE):
    raise FileNotFoundError(f"{CONFIG_FILE} not found. Please create it with required settings.")

with open(CONFIG_FILE, "r") as f:
    config = json.load(f)

BRAVE_PATH = config.get("brave_path")
CHROMEDRIVER_PATH = config.get("chromedriver_path")
SEARCH_QUERY = config.get("search_query", "laptops")
NUM_PAGES = config.get("num_pages", 5)
OUTPUT_FILE = config.get("output_file", "amazon_products.csv")

if not BRAVE_PATH or not CHROMEDRIVER_PATH:
    raise ValueError("Please provide valid paths for Brave and ChromeDriver in config.json")

# -------------------- SETUP SELENIUM --------------------
options = Options()
options.binary_location = BRAVE_PATH
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/141.0.7390.108 Safari/537.36"
)

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# -------------------- SCRAPING LOGIC --------------------
products = []

for page in range(1, NUM_PAGES + 1):
    print(f"Scraping page {page} ...")
    url = f"https://www.amazon.in/s?k={SEARCH_QUERY}&page={page}"
    driver.get(url)
    
    time.sleep(random.uniform(3, 6))
    
    for _ in range(3):
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight / 3);")
        time.sleep(1)
    
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
                "Brand": brand,
                "Product Name": name,
                "Price (INR)": price,
                "Product Link": link
            })
    
    time.sleep(random.uniform(4, 8))

# -------------------- SAVE TO CSV --------------------
df = pd.DataFrame(products)
df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
print(f"\n✅ Scraping completed. {len(df)} products saved to {OUTPUT_FILE}")

# -------------------- CLEANUP --------------------
driver.quit()

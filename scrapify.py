import os
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Import scrapers
from scrapers.amazon_scraper import scrape_amazon

# -------------------- LOAD CONFIG --------------------
CONFIG_FILE = "config.json"

if not os.path.exists(CONFIG_FILE):
    raise FileNotFoundError(f"{CONFIG_FILE} not found. Please create it with required settings.")

with open(CONFIG_FILE, "r") as f:
    config = json.load(f)

CHROME_PATH = config.get("chrome_path")
CHROMEDRIVER_PATH = config.get("chromedriver_path")
SEARCH_QUERY = config.get("search_query", "laptops")
NUM_PAGES = config.get("num_pages", 3)
OUTPUT_FILE = config.get("output_file", "products.csv")
SITES = config.get("sites", ["amazon"])

if not CHROME_PATH or not CHROMEDRIVER_PATH:
    raise ValueError("Please provide valid paths for Chrome and ChromeDriver in config.json")

# -------------------- SETUP SELENIUM --------------------
options = Options()
options.binary_location = CHROME_PATH
options.add_argument("--headless=new")  # newer headless mode
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

print("🚀 Launching Chrome WebDriver...")
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# -------------------- RUN SCRAPERS --------------------
all_products = []

try:
    if "amazon" in SITES:
        all_products.extend(scrape_amazon(driver, SEARCH_QUERY, NUM_PAGES))

finally:
    driver.quit()
    print("🧹 Browser closed successfully.")

# -------------------- SAVE RESULTS --------------------
if all_products:
    df = pd.DataFrame(all_products)
    df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
    print(f"\n✅ Done! {len(df)} products saved to {OUTPUT_FILE}")
else:
    print("\n⚠️ No products scraped. Check site selectors or browser config.")

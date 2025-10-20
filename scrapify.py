import os
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Import scrapers
from scrapers.amazon_scraper import scrape_amazon
from scrapers.flipkart_scraper import scrape_flipkart
from scrapers.croma_scraper import scrape_croma
from scrapers.reliance_scraper import scrape_reliance

# -------------------- LOAD CONFIG --------------------
CONFIG_FILE = "config.json"

if not os.path.exists(CONFIG_FILE):
    raise FileNotFoundError(f"{CONFIG_FILE} not found. Please create it with required settings.")

with open(CONFIG_FILE, "r") as f:
    config = json.load(f)

BRAVE_PATH = config.get("brave_path")
CHROMEDRIVER_PATH = config.get("chromedriver_path")
SEARCH_QUERY = config.get("search_query", "laptops")
NUM_PAGES = config.get("num_pages", 3)
OUTPUT_FILE = config.get("output_file", "products.csv")
SITES = config.get("sites", ["amazon"])

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

# -------------------- RUN SCRAPERS --------------------
all_products = []

if "amazon" in SITES:
    all_products.extend(scrape_amazon(driver, SEARCH_QUERY, NUM_PAGES))

if "flipkart" in SITES:
    all_products.extend(scrape_flipkart(driver, SEARCH_QUERY, NUM_PAGES))

if "croma" in SITES:
    all_products.extend(scrape_croma(driver, SEARCH_QUERY, NUM_PAGES))

if "reliance" in SITES:
    all_products.extend(scrape_reliance(driver, SEARCH_QUERY, NUM_PAGES))

# -------------------- SAVE RESULTS --------------------
df = pd.DataFrame(all_products)
df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')

print(f"\n✅ Done! {len(df)} products saved to {OUTPUT_FILE}")

driver.quit()

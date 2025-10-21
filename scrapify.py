import os
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
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

FIREFOX_PATH = config.get("firefox_path")
GECKODRIVER_PATH = config.get("gecko_path")
SEARCH_QUERY = config.get("search_query", "laptops")
NUM_PAGES = config.get("num_pages", 3)
OUTPUT_FILE = config.get("output_file", "multi_site_products.csv")
SITES = config.get("sites", ["amazon"])

if not FIREFOX_PATH or not GECKODRIVER_PATH:
    raise ValueError("Please provide valid paths for Firefox and GeckoDriver in config.json")

# -------------------- SETUP SELENIUM FOR FIREFOX --------------------
options = Options()
options.binary_location = FIREFOX_PATH
options.add_argument("--headless")  # Firefox headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")
options.set_preference("dom.webnotifications.enabled", False)
options.set_preference("media.volume_scale", "0.0")

print("🚀 Launching WebScraper with Firefox...")
service = Service(GECKODRIVER_PATH)
driver = webdriver.Firefox(service=service, options=options)

# -------------------- RUN SCRAPERS --------------------
all_products = []

try:
    if "amazon" in SITES:
        print(f"🛍️  Scraping Amazon for '{SEARCH_QUERY}'...")
        all_products.extend(scrape_amazon(driver, SEARCH_QUERY, NUM_PAGES))

    if "flipkart" in SITES:
        print(f"🛍️  Scraping Flipkart for '{SEARCH_QUERY}'...")
        all_products.extend(scrape_flipkart(driver, SEARCH_QUERY, NUM_PAGES))

    if "croma" in SITES:
        print(f"🛍️  Scraping Croma for '{SEARCH_QUERY}'...")
        all_products.extend(scrape_croma(driver, SEARCH_QUERY, NUM_PAGES))

    if "reliance_digital" in SITES:
        print(f"🛍️  Scraping Reliance Digital for '{SEARCH_QUERY}'...")
        all_products.extend(scrape_reliance(driver, SEARCH_QUERY, NUM_PAGES))

except Exception as e:
    print(f"❌ Error during scraping: {e}")
finally:
    driver.quit()
    print("🧹 Browser closed successfully.")

# -------------------- SAVE RESULTS --------------------
if all_products:
    df = pd.DataFrame(all_products)
    df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
    print(f"\n✅ Done! {len(df)} products saved to {OUTPUT_FILE}")
    
    # Display summary
    print("\n📊 Summary by site:")
    if 'site' in df.columns:
        print(df['site'].value_counts())
else:
    print("\n⚠️ No products scraped. Check site selectors or browser config.")
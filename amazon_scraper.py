from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# -------------------- PATHS --------------------
# ✅ Path to Brave browser executable
BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

# ✅ Path to ChromeDriver executable (not Brave)
# Example: if you downloaded chromedriver-win64.zip from Google Chrome Labs
CHROMEDRIVER_PATH = r"C:\Users\Niladri\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# -------------------- CONFIGURATION --------------------
SEARCH_QUERY = "laptops"    # what to search
NUM_PAGES = 2               # number of pages
OUTPUT_FILE = "amazon_products.csv"

# -------------------- SETUP SELENIUM --------------------
options = Options()
options.binary_location = BRAVE_PATH
options.add_argument("--headless")  # 👈 run Brave in background (no UI)
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
    
    # wait for content to load
    time.sleep(random.uniform(3, 6))
    
    # scroll to load dynamic content
    for _ in range(3):
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight / 3);")
        time.sleep(1)
    
    # parse HTML with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # extract product data
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
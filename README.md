# ![Scrapify](https://img.shields.io/badge/Scrapify-Web%20Scraper-blue) Scrapify

[![Python](https://img.shields.io/badge/python-3.8+-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

**Scrapify** is a Python-based web scraping tool for extracting **product information** from Amazon.in. It collects **product name, brand, price, and product links** and saves the data in a CSV file for easy analysis. Built with **Selenium** and **BeautifulSoup**, Scrapify runs in **headless mode**, making scraping fast and efficient.

---

## 🚀 Features

* Scrape product data from multiple pages of Amazon search results
* Extract **product name**, **brand**, **price**, and **product link**
* Save results in a **CSV file** for analysis
* Runs in **headless mode** (no browser UI)
* Customizable search keywords and number of pages

---

## 🛠️ Requirements

* **Python 3.8+**
* **Brave Browser** (Chromium-based)
* **ChromeDriver** matching Brave’s Chromium version

### Python Libraries

```bash
pip install selenium beautifulsoup4 pandas
```

---

## ⚙️ Setup

1. **Install Brave Browser**
   [https://brave.com/download](https://brave.com/download)

2. **Download ChromeDriver** for your Brave Chromium version:
   [https://googlechromelabs.github.io/chrome-for-testing/](https://googlechromelabs.github.io/chrome-for-testing/)

3. **Update paths in `scrapify.py`**:

```python
BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
CHROMEDRIVER_PATH = r"C:\path\to\chromedriver.exe"
```

---

## ▶️ Usage

1. Open `scrapify.py` in VS Code.
2. Set the search keyword and number of pages:

```python
SEARCH_QUERY = "laptops"
NUM_PAGES = 5
OUTPUT_FILE = "amazon_products.csv"
```

3. Run the script:

```bash
python scrapify.py
```

4. After completion, check `amazon_products.csv` for the scraped data.

---

## 📊 Example Output

| Brand | Product Name            | Price (INR) | Product Link                      |
| ----- | ----------------------- | ----------- | --------------------------------- |
| Dell  | Dell Inspiron 15 Laptop | 45999.00    | [Link](https://www.amazon.in/...) |
| HP    | HP Pavilion Laptop      | 53999.00    | [Link](https://www.amazon.in/...) |

---

## ⚠️ Notes

* The script uses **random delays** to reduce the chance of Amazon blocking requests.
* For large-scale scraping, consider **rotating proxies** to avoid IP blocking.
* Ensure your **ChromeDriver version matches Brave’s Chromium version**.


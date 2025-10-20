# ![Scrapify](https://img.shields.io/badge/Scrapify-Web%20Scraper-blue) Scrapify

[![Python](https://img.shields.io/badge/python-3.8+-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

**Scrapify** is a Python-based web scraping tool that extracts product information from **Amazon.in**. It collects **product name, brand, price, and product link** from search results and saves it in a CSV file.

This version uses a **configuration file (`config.json`)**, so users can customize search keywords, number of pages, and file paths without modifying the script.

---

## 🚀 Features

* Scrape product data from multiple Amazon search result pages
* Extract **product name**, **brand**, **price**, and **product link**
* Save results in a **CSV file**
* Runs in **headless mode** (no browser UI)
* Fully configurable via `config.json`
* Easy to use and share

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

### 1. Download Brave Browser

[https://brave.com/download](https://brave.com/download)

### 2. Download ChromeDriver

[https://googlechromelabs.github.io/chrome-for-testing/](https://googlechromelabs.github.io/chrome-for-testing/)

> Make sure the ChromeDriver version matches your Brave Chromium version.

### 3. Create `config.json`

Create a file `config.json` in the project folder with the following content:

```json
{
    "brave_path": "PATH_TO_YOUR_BRAVE_BROWSER",
    "chromedriver_path": "PATH_TO_YOUR_CHROMEDRIVER",
    "search_query": "laptops",
    "num_pages": 5,
    "output_file": "amazon_products.csv"
}
```

* Replace `PATH_TO_YOUR_BRAVE_BROWSER` with the path to your Brave executable.
* Replace `PATH_TO_YOUR_CHROMEDRIVER` with the path to your ChromeDriver.
* Customize `search_query`, `num_pages`, and `output_file` as needed.

---

## ▶️ Usage

1. Open a terminal and navigate to the project folder.
2. Run the scraper:

```bash
python scrapify.py
```

3. Wait for the script to finish. The output CSV file (default: `amazon_products.csv`) will contain all scraped product data.

---

## 📊 Example Output

| Brand | Product Name            | Price (INR) | Product Link                      |
| ----- | ----------------------- | ----------- | --------------------------------- |
| Dell  | Dell Inspiron 15 Laptop | 45999.00    | [Link](https://www.amazon.in/...) |
| HP    | HP Pavilion Laptop      | 53999.00    | [Link](https://www.amazon.in/...) |

---

## ⚠️ Notes

* The scraper uses **random delays** to reduce the chance of Amazon blocking requests.
* For large-scale scraping, consider using **rotating proxies**.
* Ensure **ChromeDriver version matches Brave’s Chromium version**.

---

## 📄 License

This project is **open-source** under the **MIT License**.

---
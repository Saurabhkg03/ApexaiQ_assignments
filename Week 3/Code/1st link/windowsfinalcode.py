from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import os
import time

class WindowsReleaseScraper:
    """Scraper for extracting Windows 11 release information tables into a single CSV."""

    def __init__(self, driver_path, url, output_file="windows11_release_data.csv"):
        """Initialize WebDriver and set up headless execution."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--log-level=3")

        self.service = Service(driver_path)
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)
        self.url = url
        self.output_file = output_file
        self.dataframes = [] 

    def open_page(self):
        """Open the webpage and wait for it to load."""
        self.driver.get(self.url)
        self.wait = WebDriverWait(self.driver, 10)
        time.sleep(3)

    def expand_sections(self):
        """Expand all collapsible sections on the webpage."""
        sections = self.driver.find_elements(By.XPATH, "//details/summary")
        for section in sections:
            try:
                self.driver.execute_script("arguments[0].scrollIntoView();", section)
                time.sleep(1)
                self.driver.execute_script("arguments[0].click();", section)
                time.sleep(3)
            except Exception:
                pass  

    def extract_tables(self):
        """Extract all tables and store them in a merged DataFrame."""
        self.open_page()
        self.expand_sections()
        time.sleep(3)

        tables = self.driver.find_elements(By.TAG_NAME, "table")
        headings = [h4.text.strip() for h4 in self.driver.find_elements(By.TAG_NAME, "h4")]

        for idx, table in enumerate(tables):
            try:
                rows = table.find_elements(By.TAG_NAME, "tr")
                table_data = []

                for row in rows:
                    headers = row.find_elements(By.TAG_NAME, "th")
                    cols = row.find_elements(By.TAG_NAME, "td")

                    if headers:
                        table_data.append([col.text.strip() for col in headers])
                    elif cols:
                        table_data.append([col.text.strip() for col in cols])

                if len(table_data) <= 1:
                    print(f"Skipping Table {idx+1} (unsupported or empty)")
                    continue

                df = pd.DataFrame(table_data)
                table_name = headings[idx] if idx < len(headings) else f"Table_{idx+1}"
                df.insert(0, "Table Name", table_name)  

                self.dataframes.append(df)

            except Exception as e:
                print(f"Error processing Table {idx+1}: {e}")

    def save_to_csv(self):
        """Merge all tables and save to a single CSV file."""
        if self.dataframes:
            final_df = pd.concat(self.dataframes, ignore_index=True)
            final_df.to_csv(self.output_file, index=False)
            print(f"✅ All tables merged and saved to {self.output_file}")
        else:
            print("⚠ No tables extracted. CSV file not created.")

    def close_driver(self):
        """Close the WebDriver session."""
        self.driver.quit()
        print("Scraping completed successfully.")

if __name__ == "__main__":
    scraper = WindowsReleaseScraper(driver_path=r"D:\ApexaiQ\chromedriver.exe", 
                                    url="https://learn.microsoft.com/en-us/windows/release-health/windows11-release-information",
                                    output_file="windows11_release_data.csv")
    scraper.extract_tables()
    scraper.save_to_csv()
    scraper.close_driver()

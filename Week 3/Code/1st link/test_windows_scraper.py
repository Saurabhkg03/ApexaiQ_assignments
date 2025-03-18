import unittest
import os
import pandas as pd
from selenium.common.exceptions import WebDriverException, TimeoutException
from windowsfinalcode import WindowsReleaseScraper 

class TestWindowsReleaseScraper(unittest.TestCase):
    """Unit tests for WindowsReleaseScraper class."""

    @classmethod
    def setUpClass(cls):
        """Set up the test environment before any test runs."""
        cls.driver_path = r"D:\ApexaiQ\chromedriver.exe"
        cls.url = "https://learn.microsoft.com/en-us/windows/release-health/windows11-release-information"
        cls.output_file = "test_windows11_release_data.csv"
        cls.scraper = WindowsReleaseScraper(driver_path=cls.driver_path, url=cls.url, output_file=cls.output_file)

    def test_driver_initialization(self):
        """Test if WebDriver initializes correctly."""
        try:
            self.scraper.open_page()
            self.assertIsNotNone(self.scraper.driver, "WebDriver failed to initialize.")
        except WebDriverException as e:
            self.fail(f"WebDriverException occurred: {e}")

    def test_page_load(self):
        """Test if the page loads correctly."""
        self.scraper.open_page()
        self.assertEqual(self.scraper.driver.current_url, self.url, "Page did not load correctly.")

    def test_table_extraction(self):
        """Test if tables are extracted properly."""
        self.scraper.extract_tables()
        self.assertGreater(len(self.scraper.dataframes), 0, "No tables were extracted.")

    def test_csv_creation(self):
        """Test if the CSV file is created."""
        self.scraper.extract_tables()
        self.scraper.save_to_csv()
        if len(self.scraper.dataframes) > 0:
            self.assertTrue(os.path.exists(self.output_file), "CSV file was not created.")
        else:
            self.skipTest("Skipping CSV creation test due to no extracted tables.")

    def test_csv_content(self):
        """Test if the CSV file contains data."""
        self.scraper.extract_tables()
        self.scraper.save_to_csv()
        if os.path.exists(self.output_file):
            df = pd.read_csv(self.output_file)
            self.assertFalse(df.empty, "CSV file is empty.")
        else:
            self.skipTest("Skipping CSV content test because file was not created.")

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests run."""
        cls.scraper.close_driver()
        if os.path.exists(cls.output_file):
            os.remove(cls.output_file)

if __name__ == "__main__":
    unittest.main()

# test_automation_framework/web_utils/selenium_wrapper.py
import tempfile
import uuid

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
import os

class SeleniumWrapper:
    def __init__(self):
        self.driver = self._create_driver()

    def _create_driver(self):
        chrome_options = ChromeOptions()
        # Generate unique user data directory for each instance
        temp_dir = tempfile.gettempdir()
        unique_user_data_dir = os.path.join(temp_dir, f"chrome_user_data_{uuid.uuid4()}")

        if os.environ.get("BROWSER_HEADLESS") == "true":
            chrome_options.add_argument("--headless=new")
        chrome_options.add_argument(f"--user-data-dir={unique_user_data_dir}")
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--start-maximized")
        try:
            driver = webdriver.Chrome(
                service=webdriver.ChromeService(ChromeDriverManager().install()),
                options=chrome_options
            )
            return driver
        except Exception as e:
            print(f"Failed to create Chrome driver: {e}")
            # Cleanup user data directory if driver creation failed
            import shutil
            if os.path.exists(unique_user_data_dir):
                shutil.rmtree(unique_user_data_dir, ignore_errors=True)
            raise

    def get_driver(self):
        return self.driver

    def quit_driver(self):
        self.driver.quit()
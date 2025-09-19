# test_automation_framework/web_utils/selenium_wrapper.py
import os
import shutil
import tempfile
import uuid

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions

class SeleniumWrapper:
    def __init__(self):
        self.user_data_dir = self._create_user_data_dir()
        self.driver = self._create_driver()

    def _create_user_data_dir(self):
        """Creates a unique temporary directory for Chrome's user data."""
        temp_dir = tempfile.gettempdir()
        unique_dir = os.path.join(temp_dir, f"chrome_user_data_{uuid.uuid4()}")
        os.makedirs(unique_dir, exist_ok=True)
        return unique_dir

    def _create_driver(self):
        chrome_options = ChromeOptions()

        # Add arguments for correct container operation
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"--user-data-dir={self.user_data_dir}")

        # Use headless mode if environment variable is set
        if os.environ.get("BROWSER_HEADLESS") == "true":
            chrome_options.add_argument("--headless=new")

        # Set window size and start maximized only for headless mode
        if "--headless=new" in chrome_options.arguments:
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--start-maximized")

        try:
            driver = webdriver.Chrome(
                service=webdriver.ChromeService(ChromeDriverManager().install()),
                options=chrome_options
            )
            driver.implicitly_wait(10)
            return driver
        except Exception as e:
            print(f"Failed to create Chrome driver: {e}")
            # Ensure cleanup even if driver creation fails
            self._cleanup_user_data_dir()
            raise

    def get_driver(self):
        return self.driver

    def quit_driver(self):
        self.driver.quit()
        self._cleanup_user_data_dir()

    def _cleanup_user_data_dir(self):
        """Cleans up the temporary user data directory."""
        if os.path.exists(self.user_data_dir):
            shutil.rmtree(self.user_data_dir, ignore_errors=True)
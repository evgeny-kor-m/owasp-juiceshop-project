# test_automation_framework/web_utils/selenium_wrapper.py
# test_automation_framework/web_utils/selenium_wrapper.py
import os
import shutil
import tempfile
import uuid
import time

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
        unique_dir = os.path.join(temp_dir, f"chrome_user_data_{uuid.uuid4()}_{int(time.time())}")
        os.makedirs(unique_dir, exist_ok=True)
        return unique_dir

    def _create_driver(self):
        chrome_options = ChromeOptions()

        # CRITICAL: Remove user-data-dir completely - it's causing the issue
        # chrome_options.add_argument(f"--user-data-dir={self.user_data_dir}")

        # Essential arguments for containerized Chrome
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--remote-debugging-port=0")  # Let Chrome choose port
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--no-default-browser-check")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--disable-background-networking")
        chrome_options.add_argument("--disable-sync")
        chrome_options.add_argument("--metrics-recording-only")
        chrome_options.add_argument("--no-report-upload")

        # Force headless mode in containers
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920,1080")

        try:
            # Try with system Chrome first
            chrome_binary_path = self._find_chrome_binary()
            if chrome_binary_path:
                chrome_options.binary_location = chrome_binary_path

            driver = webdriver.Chrome(
                service=webdriver.ChromeService(ChromeDriverManager().install()),
                options=chrome_options
            )
            driver.implicitly_wait(10)
            driver.set_page_load_timeout(30)
            return driver
        except Exception as e:
            print(f"Failed to create Chrome driver: {e}")
            self._cleanup_user_data_dir()
            raise

    def _find_chrome_binary(self):
        """Try to find Chrome/Chromium binary in common locations."""
        possible_paths = [
            '/usr/bin/google-chrome',
            '/usr/bin/chromium-browser',
            '/usr/bin/chromium',
            '/opt/google/chrome/chrome',
            '/usr/bin/google-chrome-stable'
        ]

        for path in possible_paths:
            if os.path.exists(path):
                print(f"Found Chrome binary at: {path}")
                return path

        print("No Chrome binary found, using default")
        return None

    def get_driver(self):
        return self.driver

    def quit_driver(self):
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                print(f"Error during driver quit: {e}")
            finally:
                self.driver = None
        self._cleanup_user_data_dir()

    def _cleanup_user_data_dir(self):
        """Cleans up the temporary user data directory."""
        if hasattr(self, 'user_data_dir') and os.path.exists(self.user_data_dir):
            try:
                shutil.rmtree(self.user_data_dir, ignore_errors=True)
            except Exception as e:
                print(f"Error cleaning up user data dir: {e}")
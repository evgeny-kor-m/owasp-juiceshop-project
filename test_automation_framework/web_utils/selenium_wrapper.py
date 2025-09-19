# test_automation_framework/web_utils/selenium_wrapper.py
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
import os

class SeleniumWrapper:
    def __init__(self):
        self.driver = self._create_driver()

    def _create_driver(self):
        chrome_options = ChromeOptions()

        if os.environ.get("BROWSER_HEADLESS") == "true":
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--start-maximized")

        driver = webdriver.Chrome(
            service=webdriver.ChromeService(ChromeDriverManager().install()),
            options=chrome_options
        )
        return driver

    def get_driver(self):
        return self.driver

    def quit_driver(self):
        self.driver.quit()
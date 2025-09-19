# test_automation_framework/web_utils/selenium_wrapper.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

class SeleniumWrapper:
    def __init__(self):
        self.driver = self._create_driver()

    def _create_driver(self):
        chrome_options = Options()

        if os.environ.get("BROWSER_HEADLESS") == "true":
            chrome_options.binary_location = "/usr/bin/google-chrome"
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--user-data-dir=/tmp/user-data-dir")

        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(1920, 1080)
        driver.implicitly_wait(10)
        return driver

    def get_driver(self):
        return self.driver

    def quit_driver(self):
        self.driver.quit()
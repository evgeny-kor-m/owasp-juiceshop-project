# test_automation_framework/web_utils/playwright_wrapper.py
from playwright.sync_api import sync_playwright

class PlaywrightWrapper:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.page = self.browser.new_page()

    def get_page(self):
        return self.page

    def close(self):
        self.browser.close()
        self.playwright.stop()
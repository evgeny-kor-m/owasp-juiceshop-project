# test_automation_framework/pages/base_page.py
"""
FILE: pages/base_page.py
Base Page Object providing common utilities for all pages:
- overlay handling
- stable click actions
- input helpers
- element waiting
"""
import logging
import time
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

logger = logging.getLogger(__name__)


class BasePage:
    """Base class for all Page Objects with improved handling of blocking overlays."""

    # Locators for known blocking elements
    ACTIVE_OVERLAY_BACKDROP = (By.CSS_SELECTOR, ".cdk-overlay-backdrop.cdk-overlay-backdrop-showing")
    WELCOME_BANNER = (By.CSS_SELECTOR, "div.mat-dialog-container, mat-dialog-container")
    DISMISS_BUTTON = (By.XPATH, "//button[contains(., 'Dismiss')] | //button[@aria-label='Close Welcome Banner']")
    COOKIE_DISMISS = (By.CSS_SELECTOR, ".cc-btn.cc-dismiss")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def close_welcome_banner(self):
        """Closes the Welcome Banner if it is present."""
        try:
            logger.debug("Attempting to close Welcome Banner...")

            # Check if banner exists
            banner = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(self.WELCOME_BANNER)
            )

            if banner.is_displayed():
                # Click the Dismiss button
                dismiss_btn = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable(self.DISMISS_BUTTON)
                )
                dismiss_btn.click()
                logger.info("✅ Welcome Banner dismissed successfully")

                # Wait until overlay disappears
                WebDriverWait(self.driver, 5).until(
                    EC.invisibility_of_element_located(self.ACTIVE_OVERLAY_BACKDROP)
                )
                time.sleep(0.5)  # Extra pause for stability

        except TimeoutException:
            logger.debug("Welcome Banner not found or already closed")
        except Exception as e:
            logger.warning(f"Could not close Welcome Banner: {e}")

    def dismiss_cookie_banner(self):
        """Dismisses the cookie consent banner if present."""
        try:
            cookie_btn = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable(self.COOKIE_DISMISS)
            )
            cookie_btn.click()
            logger.debug("Cookie banner dismissed")
        except TimeoutException:
            logger.debug("Cookie banner not found")
        except Exception as e:
            logger.debug(f"Could not dismiss cookie banner: {e}")

    def close_all_overlays(self):
        """Attempts to close all known blocking overlays."""
        # 1. Close the Welcome Banner
        self.close_welcome_banner()

        # 2. Close the Cookie Banner
        self.dismiss_cookie_banner()

        # 3. If overlays still exist, send ESC key
        try:
            overlays = self.driver.find_elements(*self.ACTIVE_OVERLAY_BACKDROP)
            if overlays and any(o.is_displayed() for o in overlays):
                logger.debug("Overlays still visible, sending ESC key...")
                ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                time.sleep(0.5)
        except Exception as e:
            logger.debug(f"Error while checking overlays: {e}")

    def click(self, locator: tuple, timeout: int = 20):
        """
        Universal click method with overlay handling:
        1. Closes all overlays
        2. Scrolls to the element
        3. Performs standard click
        4. Falls back to JavaScript click if necessary
        """
        self.close_all_overlays()
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            # time.sleep(0.3)
            element.click()
            logger.info(f"✅ Clicked element: {locator}")
        except (TimeoutException, ElementClickInterceptedException) as e:
            logger.warning(f"⚠️ Standard click failed for {locator}. Trying JS click...")
            try:
                element = self.wait.until(EC.presence_of_element_located(locator))
                self.driver.execute_script("arguments[0].click();", element)
                logger.info("✅ JavaScript click succeeded")
            except Exception as js_e:
                logger.error(f"❌ Both clicks failed. Original: {e}, JS: {js_e}")
                raise

    def wait_for_visible(self, locator: tuple, timeout: int = 20):
        """Waiting for an element to be visible"""
        logger.debug(f"Waiting for element to be visible: {locator}")
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            logger.debug(f"Element is visible: {locator}")
            return element
        except TimeoutException:
            logger.error(f"❌ Element not visible within {timeout}s: {locator}")
            raise

    def input_text(self, locator: tuple, text: str, clear_first: bool = True, timeout: int = 20):
        """Types text into an input field with optional clearing."""
        element = self.wait_for_visible(locator, timeout)
        try:
            if clear_first:
                element.clear()
                logger.debug(f"Cleared input field: {locator}")
            element.send_keys(text)
            logger.info(f"✅ Entered text into element: {locator}")
        except Exception as e:
            logger.error(f"❌ Failed to input text to {locator}: {e}")
            raise

    def get_text(self, locator: tuple, timeout: int = 20) -> str:
        """Retrieves visible text from an element."""
        element = self.wait_for_visible(locator, timeout)
        text = element.text.strip()
        logger.debug(f"Text of element {locator}: '{text}'")
        return text

    def is_element_visible(self, locator: tuple, timeout: int = 5) -> bool:
        """Checking the visibility of an element"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def find_element(self, locator: tuple):
        """Search for an element with expectation"""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator: tuple):
        """Search for multiple elements with expectation"""
        return self.wait.until(EC.presence_of_all_elements_located(locator))
# test_automation_framework/pages/base_page.py

import logging

from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)

class BasePage:
    # Universal locator for active blocking overlay (based on logs and UI behavior)
    ACTIVE_OVERLAY_BACKDROP = (By.CSS_SELECTOR, ".cdk-overlay-backdrop.cdk-overlay-backdrop-showing")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        # Extended the default timeout to 20 seconds for more reliability
        self.wait = WebDriverWait(driver, 20)

    def _wait_for_known_blockers_to_disappear(self):
        """Waits for known blocking overlay elements to disappear."""
        logger.debug("Checking for active blocking overlays...")
        try:
            self.wait.until(EC.invisibility_of_element_located(self.ACTIVE_OVERLAY_BACKDROP))
            logger.debug("Active overlay has disappeared.")
        except Exception:
            logger.debug("Blocking overlay not detected or did not disappear within the timeout.")

    def click(self, locator: tuple, timeout: int = 20):
        """
        Universal click method:
        1. Waits for known blocking overlays to disappear.
        2. Waits until the target element becomes clickable (EC.element_to_be_clickable).
        3. Uses a JavaScript click as a fallback if the normal click fails.
        """
        self._wait_for_known_blockers_to_disappear()

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            logger.info(f"Successful click on element located by: {locator}")
        except Exception as e:
            logger.warning(f"Failed to click element {locator}. Attempting JavaScript click as fallback...")
            try:
                element = self.wait.until(EC.presence_of_element_located(locator))
                self.driver.execute_script("arguments[0].click();", element)
                logger.info("Successful click via JavaScript fallback.")
            except Exception as js_e:
                logger.error(f"JavaScript click also failed. Original exception: {e}")
                raise e

    def wait_for_visible(self, locator: tuple, timeout: int = 20):
        """
        Waits until the specified element becomes visible on the page.
        Returns the WebElement if visible, or raises TimeoutException if not found.
        """
        logger.debug(f"Waiting for element to become visible: {locator}")
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            logger.debug(f"Element is visible: {locator}")
            return element
        except Exception as e:
            logger.error(f"Element not visible within {timeout}s: {locator}")
            raise e

    def input_text(self, locator: tuple, text: str, clear_first: bool = True, timeout: int = 20):
        """
        Universal method for entering text into an input field:
        1. Waits for the element to be visible.
        2. Optionally clears the input before typing.
        3. Sends the specified text.
        """
        element = self.wait_for_visible(locator, timeout)
        try:
            if clear_first:
                element.clear()
                logger.debug(f"Cleared input field: {locator}")
            element.send_keys(text)
            logger.info(f"Entered text '{text}' into element: {locator}")
        except Exception as e:
            logger.error(f"Failed to send keys to {locator}: {e}")
            raise e

    def get_text(self, locator: tuple, timeout: int = 30) -> str:
        """
        Returns the visible text of an element.
        Waits until the element is visible to ensure up-to-date content.
        """
        element = self.wait_for_visible(locator, timeout)
        text = element.text.strip()
        logger.debug(f"Text of element {locator}: '{text}'")
        return text

    def close_welcome_banner(self):
        """Close the welcome banner if there is one"""
        try:
            close_button = (By.CSS_SELECTOR, "button[aria-label='Close Welcome Banner']")
            WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(close_button)
            ).click()
        except TimeoutException:
            pass

    def dismiss_cookie_banner(self):
        """Closing the cookie banner"""
        try:
            cookie_button = (By.CSS_SELECTOR, ".cc-btn.cc-dismiss")
            WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(cookie_button)
            ).click()
        except TimeoutException:
            pass

    def find_element(self, locator):
        """Поиск элемента с ожиданием"""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        """Поиск множества элементов"""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def is_element_visible(self, locator, timeout=5):
        """Проверка видимости элемента"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
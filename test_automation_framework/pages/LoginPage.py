# test_automation_framework/pages/LoginPage.py

import logging

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .BasePage import BasePage

logger = logging.getLogger(__name__)

class LoginPage(BasePage):
    """Page Object representing the Login page."""

    def __init__(self, driver, base_url):
        super().__init__(driver)
        self.url = f"{base_url}/#/login"

    # Locators for page elements
    USERNAME_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginButton")
    WELCOME_MESSAGE = (By.CSS_SELECTOR, ".mat-card-header .mat-headline")
    ACCOUNT_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Show/hide account menu']")

    # Page actions
    def open(self):
        """Opens the login page and verifies that it is loaded."""
        try:
            self.driver.get(self.url)
            logger.info(f"Opening login page: {self.url}")
            current_url = self.driver.current_url
            assert "login" in current_url, f"Expected login page, but opened: {current_url}"
            logger.info("Login page opened successfully.")
        except Exception as e:
            logger.error(f"Failed to open login page. Exception: {e}, Current URL: {self.driver.current_url}")
            raise

    def enter_credentials(self, username: str, password: str):
        """
        Enters the username and password into their respective fields.
        Uses BasePage.send_keys() for reliability.
        """
        logger.info(f"Entering credentials: {username}/****")
        try:
            self.send_keys(self.USERNAME_INPUT, username)
            self.send_keys(self.PASSWORD_INPUT, password)
            logger.debug("Credentials entered successfully.")
        except Exception as e:
            logger.error(f"Failed to enter credentials on URL {self.driver.current_url}: {e}")
            raise

    def click_login(self):
        """Clicks on the Login button using the BasePage click method."""
        logger.info("Clicking on the login button.")
        self.click(self.LOGIN_BUTTON)

    def get_welcome_message(self) -> str:
        """Returns the welcome message text displayed on the page."""
        try:
            text = self.get_text(self.WELCOME_MESSAGE)
            logger.info(f"Welcome message retrieved: '{text}'")
            return text
        except Exception as e:
            logger.error(f"Failed to retrieve welcome message: {e}")
            raise

    def verify_login_successful(self):
        """
        Verifies a successful login by:
        1. Waiting for the URL to change from the initial login page (redirect detection).
        2. Waiting for the account button to appear on the new page (UI confirmation).
        """
        logger.info("Verifying that the user has logged in and waiting for redirect.")
        initial_url = self.driver.current_url  # Store the current login page URL

        try:
            # --- Step 1: Wait until the URL changes from the login page (10 seconds) ---
            # Confirms that the redirect to a new page has started.
            WebDriverWait(self.driver, 10).until(
                EC.url_changes(initial_url)
            )
            logger.info(f"URL changed to: {self.driver.current_url}. Waiting for account button...")

            # --- Step 2: Wait until the account button becomes visible (10 seconds) ---
            # Confirms that the target page has fully loaded.
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.ACCOUNT_BUTTON)
            )

            current_url = self.driver.current_url
            # Ensure we are no longer on the login page
            assert "login" not in current_url.lower(), f"Still on the login page: {current_url}"
            logger.info("Login verified successfully.")

        except TimeoutException as e:
            # Use TimeoutException explicitly for better error reporting
            current_url = self.driver.current_url
            logger.error(f"Timeout waiting for successful login. Current URL: {current_url}. Exception: {e}")
            raise AssertionError(f"Timeout waiting for login success. Current URL: {current_url}. Error: {e}")
        except Exception as e:
            logger.error(f"Login verification failed. Current URL: {self.driver.current_url}. Error: {e}")
            raise

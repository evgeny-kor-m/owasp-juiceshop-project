# test_automation_framework/pages/LoginPage.py

import logging
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
        Verifies that the login process completed successfully:
        - Waits for the account button to appear.
        - Confirms that the current URL has changed from the login page.
        """
        logger.info("Verifying that the user is logged in.")
        try:
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(self.ACCOUNT_BUTTON)
            )
            current_url = self.driver.current_url
            assert "login" not in current_url, f"Still on login page after login attempt: {current_url}"
            logger.info("Login successful.")
        except Exception as e:
            logger.error(f"Login verification failed: {e}")
            raise

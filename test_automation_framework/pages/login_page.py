# test_automation_framework/pages/login_page.py

# ============================================
# FILE: pages/login_page.py
# ============================================
import logging
import time
import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from test_automation_framework.base.base_page import BasePage

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Page Object representing the Login Page of the application."""

    # Locators
    USERNAME_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginButton")
    ACCOUNT_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Show/hide account menu']")

    def __init__(self, driver, base_url):
        super().__init__(driver)
        self.url = f"{base_url}/#/login"

    @allure.step("Open login page")
    def open(self):
        """Opens the login page and verifies the correct URL was loaded."""
        try:
            self.driver.get(self.url)
            logger.info(f"📄 Opening login page: {self.url}")

            current_url = self.driver.current_url
            assert "login" in current_url.lower(), f"Expected login page, but got: {current_url}"
            logger.info("✅ Login page opened successfully.")

        except Exception as e:
            logger.error(f"❌ Failed to open login page: {e}")
            raise

    @allure.step("Enter credentials: username={username}")
    def enter_credentials(self, username: str, password: str):
        """Enters user credentials into username and password fields."""
        logger.info(f"🔑 Entering credentials for user: {username}/****")
        try:
            self.input_text(self.USERNAME_INPUT, username)
            self.input_text(self.PASSWORD_INPUT, password)
            logger.debug("✅ Credentials entered successfully.")
        except Exception as e:
            logger.error(f"❌ Failed to enter credentials: {e}")
            raise

    @allure.step("Click login button")
    def click_login(self):
        """Clicks the Login button."""
        logger.info("🖱️ Clicking the Login button...")
        self.click(self.LOGIN_BUTTON)

    @allure.step("Verify successful login")
    def verify_login_successful(self):
        """
        Verifies successful login:
        1. Waits for the URL to change (redirect)
        2. Waits for the account button to appear
        3. Closes Welcome Banner and other overlays
        """
        logger.info("🔍 Verifying login success...")
        initial_url = self.driver.current_url

        try:
            # Step 1: Wait for redirect
            WebDriverWait(self.driver, 0.5).until(EC.url_changes(initial_url))
            logger.info(f"✅ URL changed to: {self.driver.current_url}")

            # Step 2: Wait for account button
            WebDriverWait(self.driver, 0.5).until(
                EC.visibility_of_element_located(self.ACCOUNT_BUTTON)
            )

            current_url = self.driver.current_url
            assert "login" not in current_url.lower(), f"Still on login page: {current_url}"
            logger.info("✅ Login verified successfully.")

            # Step 3: Close any post-login popups
            time.sleep(1)
            self.close_welcome_banner()
            self.close_all_overlays()

        except TimeoutException as e:
            current_url = self.driver.current_url
            logger.error(f"❌ Timeout during login verification. URL: {current_url}")
            raise AssertionError(f"Login failed. Current URL: {current_url}. Error: {e}")
        except Exception as e:
            logger.error(f"❌ Login verification failed: {e}")
            raise

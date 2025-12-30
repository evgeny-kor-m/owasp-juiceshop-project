# ============================================
# FILE: pages/checkout_page.py
# ============================================
import logging
from selenium.webdriver.common.by import By
from test_automation_framework.base.base_page import BasePage

logger = logging.getLogger(__name__)


class CheckoutPage(BasePage):
    """Page Object representing the Checkout Page."""

    # Locators
    ADDRESS_SECTION = (By.CSS_SELECTOR, "mat-card[class*='address']")
    DELIVERY_SECTION = (By.CSS_SELECTOR, "mat-card[class*='delivery']")
    PAYMENT_SECTION = (By.CSS_SELECTOR, "mat-card[class*='payment']")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Continue']")
    PLACE_ORDER_BUTTON = (By.CSS_SELECTOR, "button#checkoutButton")

    def __init__(self, driver):
        super().__init__(driver)
        logger.info("💳 Initializing CheckoutPage...")

    def is_checkout_page_loaded(self) -> bool:
        """Checks if the checkout page is loaded by verifying the address section."""
        return self.is_element_visible(self.ADDRESS_SECTION, timeout=10)

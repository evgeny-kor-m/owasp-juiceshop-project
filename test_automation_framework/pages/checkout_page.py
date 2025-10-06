# ============================================
# FILE: pages/checkout_page.py
# ============================================
from selenium.webdriver.common.by import By
from .base_page import BasePage


class CheckoutPage(BasePage):
    """Страница оформления заказа"""

    # Локаторы
    ADDRESS_SECTION = (By.CSS_SELECTOR, "mat-card[class*='address']")
    DELIVERY_SECTION = (By.CSS_SELECTOR, "mat-card[class*='delivery']")
    PAYMENT_SECTION = (By.CSS_SELECTOR, "mat-card[class*='payment']")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Continue']")
    PLACE_ORDER_BUTTON = (By.CSS_SELECTOR, "button#checkoutButton")

    def __init__(self, driver):
        super().__init__(driver)

    def is_checkout_page_loaded(self):
        """Проверка загрузки страницы оформления"""
        return self.is_element_visible(self.ADDRESS_SECTION, timeout=10)
# ============================================
# FILE: pages/basket_page.py
# ============================================
import logging
from selenium.webdriver.common.by import By
from .base_page import BasePage

logger = logging.getLogger(__name__)


class BasketPage(BasePage):
    """Page Object representing the Shopping Basket page."""

    # Locators
    BASKET_HEADING = (By.XPATH, "//h1[contains(text(), 'Your Basket')]")
    BASKET_ITEMS = (By.CSS_SELECTOR, "mat-row.mat-mdc-row")
    ITEM_NAME_IN_BASKET = (By.CSS_SELECTOR, "mat-cell.mat-mdc-cell")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, "button#checkoutButton")
    ITEM_QUANTITY = (By.CSS_SELECTOR, "mat-cell[id*='quantity']")
    TOTAL_PRICE = (By.ID, "price")

    def __init__(self, driver):
        super().__init__(driver)
        logger.info("🛒 Initializing BasketPage...")

    def is_basket_page_loaded(self) -> bool:
        """Checks if the basket page is visible."""
        return self.is_element_visible(self.BASKET_HEADING, timeout=10)

    def get_items_in_basket(self) -> list:
        """Retrieves a list of product names currently in the basket."""
        items = []
        try:
            rows = self.find_elements(self.BASKET_ITEMS)
            for row in rows:
                item_cells = row.find_elements(By.CSS_SELECTOR, "mat-cell")
                if len(item_cells) > 1:
                    item_name = item_cells[1].text
                    items.append(item_name)
            logger.debug(f"Items in basket: {items}")
        except Exception as e:
            logger.warning(f"Could not retrieve basket items: {e}")
        return items

    def is_product_in_basket(self, product_name: str) -> bool:
        """Checks if a specific product is present in the basket."""
        items = self.get_items_in_basket()
        is_present = any(product_name in item for item in items)
        logger.info(f"Product '{product_name}' in basket: {is_present}")
        return is_present

    def get_basket_items_count(self) -> int:
        """Returns the total count of items in the basket."""
        items = self.find_elements(self.BASKET_ITEMS)
        count = len(items)
        logger.debug(f"Basket items count: {count}")
        return count

    def proceed_to_checkout(self):
        """Clicks the checkout button to proceed with order placement."""
        logger.info("💳 Proceeding to checkout...")
        self.click(self.CHECKOUT_BUTTON)

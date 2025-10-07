# ============================================
# FILE: pages/products_page.py
# ============================================
import logging
import time
from selenium.webdriver.common.by import By
from .base_page import BasePage

logger = logging.getLogger(__name__)


class ProductsPage(BasePage):
    """Page Object representing the 'All Products' page."""

    # Locators
    ALL_PRODUCTS_HEADING = (By.XPATH, "//div[contains(text(), 'All Products')]")
    ADD_TO_BASKET_BUTTONS = (By.CSS_SELECTOR, "button.btn-basket")
    BASKET_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Show the shopping cart']")
    BASKET_COUNTER = (By.CSS_SELECTOR, "span.fa-layers-counter")
    PRODUCT_NAME = (By.CSS_SELECTOR, "div.item-name")

    def __init__(self, driver):
        super().__init__(driver)
        logger.info("🛒 Initializing ProductsPage...")
        self.close_all_overlays()
        time.sleep(0.5)

    def is_products_page_loaded(self) -> bool:
        """Checks if the products page is fully loaded."""
        return self.is_element_visible(self.ALL_PRODUCTS_HEADING)

    def get_product_name_by_index(self, index: int = 0) -> str:
        """Returns the product name by its index in the product list."""
        products = self.find_elements(self.PRODUCT_NAME)
        if index < len(products):
            return products[index].text
        return None

    def add_product_to_basket_by_index(self, index: int = 0) -> str:
        """
        Adds a product to the basket by its index with proper overlay handling.
        """
        logger.info(f"➕ Adding product #{index} to basket...")

        self.close_all_overlays()
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.3)

        buttons = self.find_elements(self.ADD_TO_BASKET_BUTTONS)
        if index >= len(buttons):
            logger.error(f"❌ Product index {index} out of range (total: {len(buttons)})")
            return None

        product_name = self.get_product_name_by_index(index)
        button = buttons[index]

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", button
        )
        time.sleep(0.3)

        self.close_all_overlays()

        try:
            button.click()
            logger.info(f"✅ Product '{product_name}' added to basket.")
        except Exception as e:
            logger.warning(f"⚠️ Standard click failed, using JavaScript: {e}")
            self.driver.execute_script("arguments[0].click();", button)
            logger.info(f"✅ Product '{product_name}' added via JavaScript.")

        time.sleep(0.5)
        return product_name

    def add_product_by_name(self, product_name: str):
        """Adds a specific product to the basket by its name."""
        logger.info(f"➕ Adding product by name: '{product_name}'")
        self.close_all_overlays()

        product_xpath = (
            By.XPATH,
            f"//div[@class='item-name' and contains(text(), '{product_name}')]"
            "/ancestor::mat-card//button[contains(@class, 'btn-basket')]",
        )
        self.click(product_xpath)
        time.sleep(0.5)
        logger.info(f"✅ Product '{product_name}' added to basket.")

    def get_basket_items_count(self) -> int:
        """Returns the number of items currently in the basket."""
        try:
            counter_text = self.get_text(self.BASKET_COUNTER)
            count = int(counter_text)
            logger.debug(f"Basket counter: {count}")
            return count
        except Exception as e:
            logger.warning(f"Could not read basket counter: {e}")
            return 0

    def go_to_basket(self):
        """Navigates to the shopping basket page."""
        logger.info("🛒 Navigating to basket...")
        self.click(self.BASKET_BUTTON)
        time.sleep(1)

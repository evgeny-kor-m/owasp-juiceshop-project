# ============================================
# FILE: pages/basket_page.py
# ============================================
import logging
from selenium.webdriver.common.by import By
from .base_page import BasePage

logger = logging.getLogger(__name__)

class BasketPage(BasePage):
    """Страница корзины"""

    # Локаторы
    BASKET_HEADING = (By.XPATH, "//h1[contains(text(), 'Your Basket')]")
    BASKET_ITEMS = (By.CSS_SELECTOR, "mat-row.mat-mdc-row")
    ITEM_NAME_IN_BASKET = (By.CSS_SELECTOR, "mat-cell.mat-mdc-cell")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, "button#checkoutButton")
    ITEM_QUANTITY = (By.CSS_SELECTOR, "mat-cell[id*='quantity']")
    TOTAL_PRICE = (By.ID, "price")

    def __init__(self, driver):
        super().__init__(driver)

    def is_basket_page_loaded(self):
        """Проверка загрузки страницы корзины"""
        return self.is_element_visible(self.BASKET_HEADING, timeout=10)

    def get_items_in_basket(self):
        """Получение списка товаров в корзине"""
        items = []
        try:
            rows = self.find_elements(self.BASKET_ITEMS)
            for row in rows:
                item_cells = row.find_elements(By.CSS_SELECTOR, "mat-cell")
                if len(item_cells) > 0:
                    item_name = item_cells[1].text if len(item_cells) > 1 else item_cells[0].text
                    items.append(item_name)
        except:
            pass
        return items

    def is_product_in_basket(self, product_name):
        """Проверка наличия товара в корзине"""
        items = self.get_items_in_basket()
        return any(product_name in item for item in items)

    def get_basket_items_count(self):
        """Получение количества товаров в корзине"""
        items = self.find_elements(self.BASKET_ITEMS)
        return len(items)

    def proceed_to_checkout(self):
        """Переход к оформлению заказа"""
        self.click(self.CHECKOUT_BUTTON)




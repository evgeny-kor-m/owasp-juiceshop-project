# ============================================
# FILE: pages/products_page.py
# ============================================
from selenium.webdriver.common.by import By
from .base_page import BasePage


class ProductsPage(BasePage):
    """Страница со списком товаров"""

    # Локаторы
    ALL_PRODUCTS_HEADING = (By.XPATH, "//div[contains(text(), 'All Products')]")
    ADD_TO_BASKET_BUTTONS = (By.CSS_SELECTOR, "button.btn-basket")
    BASKET_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Show the shopping cart']")
    BASKET_COUNTER = (By.CSS_SELECTOR, "span.fa-layers-counter")
    PRODUCT_CARDS = (By.CSS_SELECTOR, "mat-card.mat-mdc-card")
    PRODUCT_NAME = (By.CSS_SELECTOR, "div.item-name")
    PRODUCT_PRICE = (By.CSS_SELECTOR, "div.item-price")

    def __init__(self, driver):
        super().__init__(driver)

    def is_products_page_loaded(self):
        """Проверка загрузки страницы товаров"""
        return self.is_element_visible(self.ALL_PRODUCTS_HEADING)

    def get_product_name_by_index(self, index=0):
        """Получение имени товара по индексу"""
        products = self.find_elements(self.PRODUCT_NAME)
        if index < len(products):
            return products[index].text
        return None

    def add_product_to_basket_by_index(self, index=0):
        """Добавление товара в корзину по индексу"""
        buttons = self.find_elements(self.ADD_TO_BASKET_BUTTONS)
        if index < len(buttons):
            product_name = self.get_product_name_by_index(index)
            buttons[index].click()
            return product_name
        return None

    def add_product_by_name(self, product_name):
        """Добавление конкретного товара по имени"""
        product_xpath = (
            By.XPATH,
            f"//div[@class='item-name' and contains(text(), '{product_name}')]"
            "/ancestor::mat-card//button[@class='btn-basket']"
        )
        self.click(product_xpath)

    def get_basket_items_count(self):
        """Получение количества товаров в корзине"""
        try:
            counter_text = self.get_text(self.BASKET_COUNTER)
            return int(counter_text)
        except:
            return 0

    def go_to_basket(self):
        """Переход в корзину"""
        self.click(self.BASKET_BUTTON)
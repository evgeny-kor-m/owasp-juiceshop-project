import logging
import pytest
from test_automation_framework.pages.products_page import ProductsPage
from test_automation_framework.pages.basket_page import BasketPage
from test_automation_framework.pages.login_page import LoginPage

logger = logging.getLogger(__name__)

class TestShoppingCart:
    """Тесты для работы с корзиной покупок"""

    def test_add_product_to_basket(self, setup_teardown_driver,web_base_url):
        """Тест: Добавление товара в корзину"""

        driver = setup_teardown_driver
        logger.info(f"Create an instance of Page Object")
        login_page = LoginPage(driver,web_base_url)

        # Выполняем действия, используя методы Page Object
        login_page.open()
        login_page.enter_credentials("admin@juice-sh.op", "admin123")
        login_page.click_login()
        login_page.verify_login_successful()

# Шаг 1: Создание объекта страницы товаров
        products_page = ProductsPage(driver)

        # Проверяем, что страница загружена
        assert products_page.is_products_page_loaded(), "Страница товаров не загрузилась"

        # Шаг 2: Добавление товара в корзину
        initial_count = products_page.get_basket_items_count()
        product_name = products_page.add_product_to_basket_by_index(0)

        # Проверяем увеличение счетчика корзины
        new_count = products_page.get_basket_items_count()
        assert new_count == initial_count + 1, "Счетчик корзины не увеличился"

        # Шаг 3: Переход в корзину
        products_page.go_to_basket()

        # Создание объекта страницы корзины
        basket_page = BasketPage(driver)
        assert basket_page.is_basket_page_loaded(), "Страница корзины не загрузилась"

        # Шаг 4: Проверка, что товар в корзине
        assert basket_page.is_product_in_basket(product_name), \
            f"Товар '{product_name}' не найден в корзине"

    def test_add_multiple_products_to_basket(self, setup_teardown_driver,web_base_url):
        """Тест: Добавление нескольких товаров в корзину"""
        driver = setup_teardown_driver
        logger.info(f"Create an instance of Page Object")
        login_page = LoginPage(driver,web_base_url)

        # Выполняем действия, используя методы Page Object
        login_page.open()
        login_page.enter_credentials("admin@juice-sh.op", "admin123")
        login_page.click_login()
        login_page.verify_login_successful()

        products_page = ProductsPage(driver)

        # Добавляем 3 разных товара
        added_products = []
        for i in range(3):
            product_name = products_page.add_product_to_basket_by_index(i)
            added_products.append(product_name)

        # Проверяем счетчик
        basket_count = products_page.get_basket_items_count()
        assert basket_count >= 3, f"Ожидалось минимум 3 товара, получено {basket_count}"

        # Переходим в корзину
        products_page.go_to_basket()

        basket_page = BasketPage(driver)

        # Проверяем наличие всех товаров
        for product in added_products:
            assert basket_page.is_product_in_basket(product), \
                f"Товар '{product}' не найден в корзине"

    def test_full_checkout_flow(self, setup_teardown_driver,web_base_url):
        """Тест: Полный процесс оформления заказа"""
        driver = setup_teardown_driver
        logger.info(f"Create an instance of Page Object")
        login_page = LoginPage(driver,web_base_url)

        # Выполняем действия, используя методы Page Object
        login_page.open()
        login_page.enter_credentials("admin@juice-sh.op", "admin123")
        login_page.click_login()
        login_page.verify_login_successful()

        # 1. Добавляем товар
        products_page = ProductsPage(driver)
        product_name = products_page.add_product_to_basket_by_index(0)

        # 2. Идем в корзину
        products_page.go_to_basket()

        basket_page = BasketPage(driver)
        assert basket_page.is_basket_page_loaded(), "Корзина не загрузилась"

        # 3. Проверяем товар
        assert basket_page.is_product_in_basket(product_name), "Товар не в корзине"

        # 4. Оформляем заказ
        basket_page.proceed_to_checkout()

        # Здесь нужно добавить дополнительные шаги для checkout
        # в зависимости от того, что требует Juice Shop


if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", __file__])

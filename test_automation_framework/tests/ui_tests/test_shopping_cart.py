# test_automation_framework/tests/ui_tests/test_shopping_cart.py

import logging
import pytest
from test_automation_framework.pages.products_page import ProductsPage
from test_automation_framework.pages.basket_page import BasketPage
from test_automation_framework.pages.login_page import LoginPage

logger = logging.getLogger(__name__)

class TestShoppingCart:
    """Tests for shopping cart functionality"""
    @pytest.mark.ui
    @pytest.mark.skip
    def test_add_product_to_basket(self, setup_teardown_driver,web_base_url):
        """Test: Adding a product to the basket"""

        driver = setup_teardown_driver
        logger.info(f"Create an instance of Page Object")
        login_page = LoginPage(driver,web_base_url)

        # Perform actions using Page Object methods
        login_page.open()
        login_page.enter_credentials("admin@juice-sh.op", "admin123")
        login_page.click_login()
        login_page.verify_login_successful()

        # # At the start of the test after login
        # driver.save_screenshot("/app/screenshots/after_login.png")
        # print(f"Overlays on page: {len(driver.find_elements(By.CSS_SELECTOR, '.cdk-overlay-backdrop'))}")

        # # Add after login:
        # print("=" * 80)
        # print("PAGE SOURCE (first 1000 characters):")
        # print(driver.page_source[:1000])
        # print("=" * 80)
        #
        # # Overlay check
        # overlays = driver.find_elements(By.CSS_SELECTOR, '.cdk-overlay-backdrop')
        # print(f"Found {len(overlays)} overlays")
        # for overlay in overlays:
        #     print(f"  - Displayed: {overlay.is_displayed()}")
        #     print(f"  - Classes: {overlay.get_attribute('class')}")

        # Step 1: Create the products page object
        products_page = ProductsPage(driver)

        # Verify that the page is loaded
        assert products_page.is_products_page_loaded(), "Products page did not load"

        # Step 2: Add product to basket
        initial_count = products_page.get_basket_items_count()
        product_name = products_page.add_product_to_basket_by_index(0)

        # Verify the basket counter increased
        new_count = products_page.get_basket_items_count()
        assert new_count == initial_count + 1, "Basket counter did not increase"

        # Step 3: Go to the basket
        products_page.go_to_basket()

        # Create the basket page object
        basket_page = BasketPage(driver)
        # Verify that the page is loaded
        assert basket_page.is_basket_page_loaded(), "Basket page did not load"

        # Step 4: Verify the product is in the basket
        assert basket_page.is_product_in_basket(product_name), \
            f"Product '{product_name}' not found in the basket"
    @pytest.mark.skip
    @pytest.mark.ui
    def test_add_multiple_products_to_basket(self, setup_teardown_driver,web_base_url):
        """Test: Adding multiple products to the basket"""
        driver = setup_teardown_driver
        logger.info(f"Create an instance of Page Object")
        login_page = LoginPage(driver,web_base_url)

        # Perform actions using Page Object methods
        login_page.open()
        login_page.enter_credentials("admin@juice-sh.op", "admin123")
        login_page.click_login()
        login_page.verify_login_successful()

        products_page = ProductsPage(driver)

        # Add 3 different products
        added_products = []
        for i in range(3):
            product_name = products_page.add_product_to_basket_by_index(i)
            added_products.append(product_name)

        # Check the counter
        basket_count = products_page.get_basket_items_count()
        assert basket_count >= 3, f"Expected minimum 3 products, got {basket_count}"

        # Go to the basket
        products_page.go_to_basket()

        basket_page = BasketPage(driver)

        # Verify the presence of all products
        for product in added_products:
            assert basket_page.is_product_in_basket(product), \
                f"Product '{product}' not found in the basket"
    @pytest.mark.ui
    @pytest.mark.skip
    def test_full_checkout_flow(self, setup_teardown_driver,web_base_url):
        """Test: Full checkout process"""
        driver = setup_teardown_driver
        logger.info(f"Create an instance of Page Object")
        login_page = LoginPage(driver,web_base_url)

        # Perform actions using Page Object methods
        login_page.open()
        login_page.enter_credentials("admin@juice-sh.op", "admin123")
        login_page.click_login()
        login_page.verify_login_successful()

        # 1. Add a product
        products_page = ProductsPage(driver)
        product_name = products_page.add_product_to_basket_by_index(0)

        # 2. Go to the basket
        products_page.go_to_basket()

        basket_page = BasketPage(driver)
        assert basket_page.is_basket_page_loaded(), "Basket page did not load"

        # 3. Verify the product
        assert basket_page.is_product_in_basket(product_name), "Product not in the basket"

        # 4. Proceed to checkout
        basket_page.proceed_to_checkout()

        # Additional steps for checkout are needed here
        # depending on what Juice Shop requires


if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", __file__])
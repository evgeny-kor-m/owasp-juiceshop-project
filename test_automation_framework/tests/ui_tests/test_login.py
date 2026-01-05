import logging
import pytest
from test_automation_framework.base.base_test import BaseUITest
from test_automation_framework.pages.login_page import LoginPage

# Logging Settings (you can use a logger from Conftest.py, but for clarity here is your own)
logger = logging.getLogger(__name__)

class TestJuiceShopLoginUI(BaseUITest):
    #@pytest.mark.skip
    @pytest.mark.ui
    @pytest.mark.login
    @pytest.mark.smoke
    def test_user_login(self):

        # Создаем экземпляр Page Object
        logger.info(f"Create an instance of Page Object")
        login_page = LoginPage(self.driver, self.web_url)

        # Выполняем действия, используя методы Page Object
        login_page.open()
        login_page.enter_credentials("admin@juice-sh.op", "ERRORadmin123")
        login_page.click_login()
        login_page.verify_login_successful()

        # Проверяем результат
    #    assert "Welcome" in login_page.get_welcome_message() # Предполагаемая проверка
    #    assert "admin@juice-sh.op" in login_page.get_welcome_message() # Предполагаемая проверка
        assert "OWASP Juice Shop" in self.driver.title
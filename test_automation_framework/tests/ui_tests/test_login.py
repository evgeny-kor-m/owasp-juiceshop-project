import logging
from test_automation_framework.pages.LoginPage import LoginPage

# Logging Settings (you can use a logger from Conftest.py, but for clarity here is your own)
logger = logging.getLogger(__name__)

#@pytest.mark.ui
def test_user_login(setup_teardown_driver,web_base_url):
    # 'setup_teardown_driver' - это фикстура, которая предоставляет драйвер.
    driver = setup_teardown_driver

    # Создаем экземпляр Page Object
    logger.info(f"Создаем экземпляр Page Object")
    login_page = LoginPage(driver,web_base_url)

    # Выполняем действия, используя методы Page Object
    login_page.open()
    login_page.enter_credentials("test@example.com", "password")
    login_page.click_login()

    # Проверяем результат
    # assert "Welcome" in login_page.get_welcome_message() # Предполагаемая проверка
    # assert "test@example.com" in login_page.get_welcome_message() # Предполагаемая проверка
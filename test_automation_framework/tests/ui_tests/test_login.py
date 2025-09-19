import pytest
from test_automation_framework.pages.LoginPage import LoginPage

@pytest.mark.ui
def test_user_login(setup_teardown_driver):
    # 'setup_teardown_driver' - это фикстура, которая предоставляет драйвер.
    driver = setup_teardown_driver

    # Создаем экземпляр Page Object
    login_page = LoginPage(driver)

    # Выполняем действия, используя методы Page Object
    login_page.open()
    login_page.enter_credentials("test@example.com", "password")
    login_page.click_login()

    # Проверяем результат
    # assert "Welcome" in login_page.get_welcome_message() # Предполагаемая проверка
    # assert "test@example.com" in login_page.get_welcome_message() # Предполагаемая проверка
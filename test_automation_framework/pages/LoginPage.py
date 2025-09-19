import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

class LoginPage:
    # Конструктор, который принимает драйвер
    def __init__(self, driver,base_url):
        self.driver = driver
        self.url = f"{base_url}/rest/user/login"

    # Локаторы элементов на странице
    _email_field = (By.ID, "email")
    _password_field = (By.ID, "password")
    _login_button = (By.ID, "loginButton")
    _welcome_message = (By.CSS_SELECTOR, ".mat-card-header .mat-headline")

    # Методы, которые выполняют действия
    def open(self):
        self.driver.get(self.url)

    def enter_credentials(self, email, password):
        try:
            wait = WebDriverWait(self.driver, 10)
            # self.driver.find_element(*self._email_field).send_keys(email)
            # self.driver.find_element(*self._password_field).send_keys(password)

            # Явное ожидание, пока поле email не станет видимым и доступным для клика.
            email_element = wait.until(EC.element_to_be_clickable(self._email_field))
            email_element.send_keys(email)

            # Явное ожидание, пока поле password не станет видимым.
            password_element = wait.until(EC.visibility_of_element_located(self._password_field))
            password_element.send_keys(password)
        except Exception as e:
            logger.error(f"Failed to enter credentials: {e}")
            raise

    def click_login(self):
        self.driver.find_element(*self._login_button).click()

    def get_welcome_message(self):
        return self.driver.find_element(*self._welcome_message).text

# test_automation_framework/pages/LoginPage.py
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

class LoginPage:
    # Конструктор, который принимает драйвер
    def __init__(self, driver,base_url):
        self.driver = driver
        self.url = f"{base_url}/#/login"

    # Локаторы элементов на странице
    USERNAME_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginButton")
    WELCOME_MESSAGE = (By.CSS_SELECTOR, ".mat-card-header .mat-headline")
    OVERLAY_BACKDROP = (By.CLASS_NAME, "cdk-overlay-backdrop")
    OVERLAY_BACKDROP_ACTIVE = (By.CSS_SELECTOR, ".cdk-overlay-backdrop.cdk-overlay-backdrop-showing")
    ACCOUNT_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Show/hide account menu']")


    # Методы, которые выполняют действия
    def open(self):
        try:
            self.driver.get(self.url)
            html_content = self.driver.page_source
            logger.info(f"open page with Url:{self.driver.current_url}")
            #logger.info(html_content)
            current_url = self.driver.current_url
            assert "login" in current_url, f"Ожидали страницу логина, но открыта: {current_url}"
            logger.info("Страница логина открыта успешно")
        except Exception as e:
            logger.error(f"Failed to open page with ex: {e} \n Url:{self.driver.current_url}")
            raise

    def enter_credentials(self, username, password):
        logger.info(f"Вводим логин и пароль: {username}/****")
        try:
            wait = WebDriverWait(self.driver, 10)
            # self.driver.find_element(*self._email_field).send_keys(email)
            # self.driver.find_element(*self._password_field).send_keys(password)

            # Явное ожидание, пока поле email не станет видимым и доступным для клика.
            email_element = wait.until(EC.element_to_be_clickable(self.USERNAME_INPUT))
            email_element.send_keys(username)

            # Явное ожидание, пока поле password не станет видимым.
            password_element = wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
            password_element.send_keys(password)
        except Exception as e:
            logger.error(f"Failed to enter credentials Url:{self.driver.current_url}\n: {e}")
            raise

    def click_login(self):
        try:
            logger.info("Ждем исчезновения активного оверлея, если он есть")
            # Увеличиваем таймаут до 10 секунд и используем более специфичный локатор
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(self.OVERLAY_BACKDROP_ACTIVE)
            )
            logger.info("Активный оверлей исчез.")
        except Exception as e:
            # Если оверлей не исчез за 10 секунд, мы просто логируем это, но не падаем
            # В противном случае, ElementClickInterceptedException поймается позже.
            logger.warning(f"Активный оверлей не исчез за 10 секунд. Продолжаем. Ex: {e}")

        try:
            logger.info("Кликаем по кнопке логина")
            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.LOGIN_BUTTON)   )
            login_button.click()
        except Exception as e:
            # Ваш код обработки ошибки JS-кликом — это хороший fallback,
            # но сначала нужно устранить проблему синхронизации.
            logger.error(f"Не удалось кликнуть по кнопке логина: {e}")
            try:
                logger.warning("Пробуем кликнуть через JavaScript")
                self.driver.execute_script("arguments[0].click();", login_button)
            except Exception as js_e:
                logger.error(f"Даже JS-клик не сработал: {js_e}")
                raise


    def get_welcome_message(self):
        return self.driver.find_element(*self.WELCOME_MESSAGE).text

    def verify_login_successful(self):
        """Проверяем, что логин прошел успешно"""
        logger.info("Проверяем, что пользователь залогинился")
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.ACCOUNT_BUTTON)
        )
        current_url = self.driver.current_url
        assert "login" not in current_url, f"После логина остались на странице логина: {current_url}"
        logger.info("Логин прошел успешно")
from selenium.webdriver.common.by import By

class LoginPage:
    # Конструктор, который принимает драйвер
    def __init__(self, driver):
        self.driver = driver
        self.url = "http://host.docker.internal:8080"

    # Локаторы элементов на странице
    _email_field = (By.ID, "email")
    _password_field = (By.ID, "password")
    _login_button = (By.ID, "loginButton")
    _welcome_message = (By.CSS_SELECTOR, ".mat-card-header .mat-headline")

    # Методы, которые выполняют действия
    def open(self):
        self.driver.get(self.url)

    def enter_credentials(self, email, password):
        self.driver.find_element(*self._email_field).send_keys(email)
        self.driver.find_element(*self._password_field).send_keys(password)

    def click_login(self):
        self.driver.find_element(*self._login_button).click()

    def get_welcome_message(self):
        return self.driver.find_element(*self._welcome_message).text

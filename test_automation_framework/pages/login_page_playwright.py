# test_automation_framework/pages/login_page_playwright.py

class LoginPage:
    # Конструктор, который принимает объект 'page' Playwright
    def __init__(self, page):
        self.page = page
        self.url = "http://localhost:3000/#/login"

    # Локаторы элементов
    _email_field = "#email"
    _password_field = "#password"
    _login_button = "#loginButton"

    # Методы, которые выполняют действия
    def open(self):
        self.page.goto(self.url)

    def enter_credentials(self, email, password):
        self.page.locator(self._email_field).fill(email)
        self.page.locator(self._password_field).fill(password)

    def click_login(self):
        self.page.locator(self._login_button).click()
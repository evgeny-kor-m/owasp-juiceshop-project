# test_automation_framework/api/api_service.py

import requests
import time
import pytest
import random

# Базовый URL для OWASP Juice Shop.
# BASE_URL = "http://localhost:3000"

def generate_random_email():
    """Генерирует случайный email для регистрации."""
    return f"testuser_{int(time.time() * 1000)}@example.com"

class AuthAPI:
    """Сервисный слой для взаимодействия с API аутентификации."""
    headers = {'Host': 'juice-shop.local',
               'Content-Type': 'application/json'}

    def __init__(self, session, base_url):
            self.session = session
            self.base_url = base_url
            self.session.headers.update({'Host': 'juice-shop.local'})

    def register_new_user(self, email, password, security_answer="This is my favorite fruit"):
        """Выполняет регистрацию нового пользователя."""
        registration_payload = {
            "email": email,
            "password": password,
            "passwordRepeat": password,
            "securityQuestion": {"id": 1},
            "securityAnswer": security_answer
        }
        response = self.session.post(f"{self.base_url}/api/Users/", json=registration_payload)
        return response

    def login_with_creds(self, email, password):
        """Выполняет вход в систему и возвращает ответ."""
        login_payload = {
            "email": email,
            "password": password
        }
        response = self.session.post(f"{self.base_url}/rest/user/login", json=login_payload)
        return response

class BasketAPI:
    """Сервисный слой для взаимодействия с API корзины."""
    def __init__(self, session, base_url, basket_id):
        self.session = session
        self.base_url = base_url
        self.basket_id = basket_id

    def add_item_to_basket(self, product_id, quantity=1):
        """Добавляет товар в корзину."""
        add_item_payload = {
            "ProductId": product_id,
            "quantity": quantity,
            "BasketId": self.basket_id
        }
        response = self.session.post(f"{self.base_url}/api/BasketItems/", json=add_item_payload)
        return response

    def get_basket_content(self):
        """Проверяет содержимое корзины."""
        response = self.session.get(f"{self.base_url}/rest/basket/{self.basket_id}")
        return response

    def checkout(self):
        """Оформляет заказ."""
        response = self.session.post(f"{self.base_url}/rest/basket/{self.basket_id}/checkout")
        return response


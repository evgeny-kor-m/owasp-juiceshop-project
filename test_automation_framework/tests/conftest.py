import pytest
import os
import requests

JUICESHOP_BASE_URL = "JUICESHOP_BASE_URL"

@pytest.fixture(scope="session")
def base_url():
    """
    Получает базовый URL приложения из переменной окружения.
    Если переменная не установлена, выдает ошибку, чтобы избежать
    запуска тестов без цели.
    """
    url = os.getenv(JUICESHOP_BASE_URL)
    if not url:
        raise ValueError(f"Не установлена переменная окружения {JUICESHOP_BASE_URL}. "
                         "Укажите URL-адрес приложения Juice Shop, например: "
                         "http://juiceshop-service.juiceshop-namespace.svc.cluster.local")
    return url

@pytest.fixture(scope="session")
def api_session():
    """
    Фикстура для создания сессии requests.Session.
    Помогает сохранять cookies и заголовки между запросами.
    """
    session = requests.Session()
    session.headers.update({'Host': 'juice-shop.local'})
    yield session
    session.close()
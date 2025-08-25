import pytest
import requests

@pytest.fixture(scope="session")
def base_url():
    """Фикстура, предоставляющая базовый URL."""
    return "http://localhost:3000"

@pytest.fixture(scope="session")
def api_session():
    """
    Фикстура для создания сессии requests.Session.
    Помогает сохранять cookies и заголовки между запросами.
    """
    session = requests.Session()
    yield session
    session.close()
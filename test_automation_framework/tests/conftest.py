import pytest
import os
import requests
import logging
from test_automation_framework.web_utils.selenium_wrapper import SeleniumWrapper

# Logging Settings (performed once for the entire test launch)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/test_log.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

#JUICESHOP_BASE_URL = "JUICESHOP_BASE_URL"
WEB_BASE_URL = "WEB_BASE_URL"
API_BASE_URL  = "API_BASE_URL"

@pytest.fixture(scope="session")
def api_base_url():
    """
    Получает базовый URL приложения из переменной окружения.
    Если переменная не установлена, выдает ошибку, чтобы избежать
    запуска тестов без цели.
    """
    url = os.getenv(API_BASE_URL)
    if not url:
        raise ValueError(f"Не установлена переменная окружения {API_BASE_URL}. "
                         "Укажите URL-адрес приложения Juice Shop, например: "
                         "http://host.docker.internal:8080")
    return url

@pytest.fixture(scope="session")
def web_base_url():
    """
    Получает базовый URL приложения из переменной окружения.
    Если переменная не установлена, выдает ошибку, чтобы избежать
    запуска тестов без цели.
    """
    url = os.getenv(WEB_BASE_URL)
    if not url:
        raise ValueError(f"Не установлена переменная окружения {WEB_BASE_URL}. "
                         "Укажите URL-адрес приложения Juice Shop, например: "
                         "http://host.docker.internal:8080")
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

@pytest.fixture(scope="function")
def setup_teardown_driver(request):
    """
    Фикстура для инициализации и закрытия драйвера, используя класс-обертку.
    """
    web_wrapper = SeleniumWrapper()
    driver = web_wrapper.get_driver()

    yield driver

    web_wrapper.quit_driver()
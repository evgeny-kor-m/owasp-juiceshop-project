import os
from pathlib import Path
from dotenv import load_dotenv
import logging

# Загружаем переменные из .env файла
# Если config.py лежит в подпапке, можно указать точный путь
load_dotenv()

class Config:
    """Класс для управления настройками проекта."""
    logger = logging.getLogger(__name__)
    # Базовые URL
    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8080")
    WEB_BASE_URL = os.getenv("WEB_BASE_URL", "http://localhost:3000")
    #JUICESHOP_BASE_URL = os.getenv("JUICESHOP_BASE_URL", API_BASE_URL)

    # Окружение
    ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Пути (используем Path для кроссплатформенности)
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    ALLURE_RESULTS = BASE_DIR / os.getenv("ALLURE_RESULTS_PATH", "allure-results")
    LOGS_DIR = BASE_DIR / os.getenv("LOGS_PATH", "logs")

    # Настройки таймаутов
    DEFAULT_TIMEOUT = 10  # секунд

    @classmethod
    def print_config(cls):
        """Метод для отладки: выводит текущие настройки."""
        cls.logger.info(f"--- Configuration [{cls.ENVIRONMENT}] ---")
        cls.logger.info(f"API URL: {cls.API_BASE_URL}")
        cls.logger.info(f"Web URL: {cls.WEB_BASE_URL}")
        cls.logger.info(f"Allure results: {cls.ALLURE_RESULTS}")
        cls.logger.info(f"Log Level: {cls.LOG_LEVEL}")
        cls.logger.info(f"Log path: {cls.LOGS_DIR}")
        cls.logger.info(f"Base path: {cls.BASE_DIR}")
        cls.logger.info("---------------------------------------")

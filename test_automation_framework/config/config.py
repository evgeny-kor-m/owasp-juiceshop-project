import os
from pathlib import Path
from dotenv import load_dotenv
import logging

# Load variables from .env file
load_dotenv()

class Config:
    """Class for management project settings."""
    logger = logging.getLogger(__name__)
    # Basic URL
    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8080")
    WEB_BASE_URL = os.getenv("WEB_BASE_URL", "http://localhost:3000")
    #JUICESHOP_BASE_URL = os.getenv("JUICESHOP_BASE_URL", API_BASE_URL)

    ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Пути (используем Path для кроссплатформенности)
    BASE_DIR_PATH = Path(__file__).resolve().parent.parent.parent
    ALLURE_RESULTS_PATH = BASE_DIR_PATH / os.getenv("ALLURE_RESULTS_DIR", "allure-results")
    ALLURE_REPORTS_PATH = BASE_DIR_PATH / os.getenv("ALLURE_REPORTS_DIR", "allure-reports")
    HTML_REPORT_PATH = BASE_DIR_PATH / os.getenv("HTML_REPORTS_DIR", "html-reports")
    LOGS_PATH = BASE_DIR_PATH / os.getenv("LOGS_DIR", "logs")
    SCREENSHOTS_PATH = BASE_DIR_PATH / os.getenv("SCREENSHOTS_DIR", "screenshots")
    # TEST_RESULTS_DIR = BASE_DIR / os.getenv("TEST_RESULTS_PATH", "test_results")

    # Timeout settings
    DEFAULT_TIMEOUT = 10  # seconds
    DEFAULT_WAIT = 15
    SHORT_WAIT = 3
    LONG_WAIT = 30


    @classmethod
    def ensure_directories(cls):
        """Create necessary directories"""
        directories = [
            cls.ALLURE_RESULTS_PATH,
            cls.ALLURE_REPORTS_PATH,
            cls.HTML_REPORT_PATH,
            cls.LOGS_PATH,
            cls.SCREENSHOTS_PATH
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            cls.logger.debug(f"Directory ensured: {directory}")

    @classmethod
    def print_config(cls):
        """Output all settings."""
        cls.logger.info(f"--- Configuration [{cls.ENVIRONMENT}] ---")
        cls.logger.info(f"API URL: {cls.API_BASE_URL}")
        cls.logger.info(f"Web URL: {cls.WEB_BASE_URL}")
        cls.logger.info(f"Allure results: {cls.ALLURE_RESULTS_PATH}")
        cls.logger.info(f"Allure reports: {cls.ALLURE_REPORTS_PATH}")
        cls.logger.info(f"Html reports: {cls.HTML_REPORT_PATH}")
        cls.logger.info(f"Log Level: {cls.LOG_LEVEL}")
        cls.logger.info(f"Log path: {cls.LOGS_PATH}")
        cls.logger.info(f"Base path: {cls.BASE_DIR_PATH}")
        cls.logger.info("---------------------------------------")

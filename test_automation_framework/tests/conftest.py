# test_automation_framework/tests/conftest.py
import os

import pytest
import requests
import logging
from test_automation_framework.web_utils.selenium_wrapper import SeleniumWrapper
from test_automation_framework.config.config import config as app_config

# Read LOG_LEVEL from .env (default to INFO if not defined)
#log_level_str = os.getenv("LOG_LEVEL", "INFO").strip().upper()
log_level_str = config.LOG_LEVEL.upper()

# Convert the string to an actual logging level constant (default to INFO if invalid)
log_level = getattr(logging, log_level_str, logging.INFO)

# Configure the global logging settings
logging.basicConfig(
    level=log_level,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[
        logging.StreamHandler(),                      # Output to console
        logging.FileHandler(app_config.LOGS_DIR / "test_run.log")      # Output to file
    ]
)

logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def api_base_url():
    """
    Retrieves the base URL of the application from an environment variable.
    If the variable is not set, it raises an error to prevent
    running tests without a target.
    """
    url = app_config.API_BASE_URL
    if not url:
        raise ValueError(f"Environment variable API_BASE_URL is not set. "
                         "Please specify the URL of the Juice Shop application, for example: "
                         "http://host.docker.internal:8080")
    return url

@pytest.fixture(scope="session")
def web_base_url():
    """
    Retrieves the base URL of the application from an environment variable.
    If the variable is not set, it raises an error to prevent
    running tests without a target.
    """
    url = app_config.WEB_BASE_URL
    if not url:
        raise ValueError(f"Environment variable WEB_BASE_URL is not set. "
                         "Please specify the URL of the Juice Shop application, for example: "
                         "http://host.docker.internal:8080")
    return url

@pytest.fixture(scope="session")
def api_session():
    """
    Fixture for creating a requests.
    Helps preserve cookies and headers between requests.
    """
    session = requests.Session()
    session.headers.update({'Host': 'juice-shop.local'})
    yield session
    session.close()

@pytest.fixture(scope="session", autouse=True)
def setup_teardown_driver(request):
    """
    Fixture for initializing and closing the driver using the wrapper class.
    """
    logger.info("\n=== PYTEST: Start browser session ===")
    web_wrapper = SeleniumWrapper()
    driver = web_wrapper.get_driver()

    yield driver

    web_wrapper.quit_driver()
    logger.info("\n=== PYTEST: End browser session ===")

def pytest_configure(config):
    """Hook is executed before all tests start"""
    # os.makedirs(config.SCREENSHOTS_DIR, exist_ok=True)
    # os.makedirs(config.HTML_REPORTS, exist_ok=True)
    logger.info("\n" + "="*50)
    logger.info("PYTEST: Test execution started")
    logger.info(f"(ENVIRONMENT: {app_config.ENVIRONMENT})")
    logger.info("="*50)


def pytest_unconfigure(config):
    """Hook is executed after all tests finish"""
    try:
        logger.info("\n" + "="*50)
        logger.info("PYTEST: Test execution finished")
        logger.info("="*50)
    except ValueError:
        logger.warning("log file already closed by pytest")
        # Игнорируем ошибку, если логгер уже закрыт pytest-ом
        pass

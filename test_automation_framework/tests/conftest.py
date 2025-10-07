# test_automation_framework/tests/conftest.py
import pytest
import os
import requests
import logging
from test_automation_framework.web_utils.selenium_wrapper import SeleniumWrapper

# Read LOG_LEVEL from .env (default to INFO if not defined)
log_level_str = os.getenv("LOG_LEVEL", "INFO").strip().upper()

# Convert the string to an actual logging level constant (default to INFO if invalid)
log_level = getattr(logging, log_level_str, logging.INFO)

# Configure the global logging settings
logging.basicConfig(
    level=log_level,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[
        logging.StreamHandler(),                      # Output to console
        logging.FileHandler("logs/test_run.log")      # Output to file
    ]
)

logger = logging.getLogger(__name__)

#JUICESHOP_BASE_URL = "JUICESHOP_BASE_URL"
WEB_BASE_URL = "WEB_BASE_URL"
API_BASE_URL  = "API_BASE_URL"

@pytest.fixture(scope="session")
def api_base_url():
    """
    Retrieves the base URL of the application from an environment variable.
    If the variable is not set, it raises an error to prevent
    running tests without a target.
    """
    url = os.getenv(API_BASE_URL)
    if not url:
        raise ValueError(f"Environment variable {API_BASE_URL} is not set. "
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
    url = os.getenv(WEB_BASE_URL)
    if not url:
        raise ValueError(f"Environment variable {WEB_BASE_URL} is not set. "
                         "Please specify the URL of the Juice Shop application, for example: "
                         "http://host.docker.internal:8080")
    return url

@pytest.fixture(scope="session")
def api_session():
    """
    Fixture for creating a requests.Session session.
    Helps preserve cookies and headers between requests.
    """
    session = requests.Session()
    session.headers.update({'Host': 'juice-shop.local'})
    yield session
    session.close()

@pytest.fixture(scope="function")
def setup_teardown_driver(request):
    """
    Fixture for initializing and closing the driver using the wrapper class.
    """
    web_wrapper = SeleniumWrapper()
    driver = web_wrapper.get_driver()

    yield driver

    web_wrapper.quit_driver()
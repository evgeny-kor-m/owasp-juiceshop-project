# test_automation_framework/tests/conftest.py
import pytest
import allure
import requests
import logging
from test_automation_framework.web_utils.selenium_wrapper import SeleniumWrapper
from test_automation_framework.config.logging_config import setup_logging
from test_automation_framework.config.config import Config as app_config

# Вызываем один раз при импорте conftest
setup_logging()
logger = logging.getLogger(__name__)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook to capture test results.
    Takes a screenshot on test failure if a driver is available.
    """
    # Run the test and get the result
    outcome = yield
    rep = outcome.get_result()
    # Handle only failed test executions
    if rep.when == "call" and rep.failed:
        # Get driver if the test provides one (UI tests only)
        mode = "a" if not hasattr(item, "fixturenames") else "w"
        driver = getattr(item, "driver", None)

        if driver:
            try:
                # Capture screenshot and attach it to Allure
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=f"screenshot_{item.name}",
                    attachment_type=allure.attachment_type.PNG
                )
                logging.error(
                    f"Screenshot for failed test '{item.name}' attached to Allure."
                )
            except Exception as e:
                logging.error(f"Failed to capture screenshot: {e}")

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
                         "Please specify the URL of the Juice Shop application")
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
                         "Please specify the URL of the Juice Shop application")
    return url

@pytest.fixture(scope="function")
def api_client():
    """
    Fixture for creating a requests. Helps preserve cookies and headers between requests.
    """
    logger.info("=== PYTEST: Start api session ===")
    session = requests.Session()
    session.headers.update({'Host': 'juice-shop.local'})
    yield session
    session.close()
    logger.info("=== PYTEST: End api session ===")

@pytest.fixture(scope="function")
def browser(request):
    """
    Fixture for initializing and closing the driver using the wrapper class.
    """
    logger.info("=== PYTEST: Start browser session ===")
    web_wrapper = SeleniumWrapper()
    driver = web_wrapper.get_driver()

    yield driver

    web_wrapper.quit_driver()
    logger.info("=== PYTEST: End browser session ===")

def pytest_configure(config):
    """Hook is executed before all tests start"""
    # os.makedirs(config.SCREENSHOTS_DIR, exist_ok=True)
    # os.makedirs(config.HTML_REPORTS, exist_ok=True)
    app_config.print_config()
    logger.info("\n" + "="*50)
    logger.info("PYTEST: All tests execution started")
    logger.info(f"(ENVIRONMENT: {app_config.ENVIRONMENT})")
    logger.info("="*50)


def pytest_unconfigure(config):
    """Hook is executed after all tests finish"""
    try:
        logger.info("\n" + "="*50)
        logger.info("PYTEST: All test execution finished")
        logger.info("="*50)
    except ValueError:
        logger.warning("log file already closed by pytest")
        # Игнорируем ошибку, если логгер уже закрыт pytest-ом
        pass

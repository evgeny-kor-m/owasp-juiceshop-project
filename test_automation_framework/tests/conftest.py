# test_automation_framework/tests/conftest.py
import base64
import os
import time
from datetime import datetime

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
        is_ui_test = any(mark.name == "ui" for mark in item.iter_markers())

        if is_ui_test:
            driver = item.funcargs.get("browser")

            if driver:
                try:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    screenshot_filename = f"screenshot_{item.name}_{timestamp}.png"
                    screenshot_path = app_config.SCREENSHOTS_PATH / screenshot_filename

                    # Save screenshot on disk
                    driver.save_screenshot(str(screenshot_path))
                    logger.info(f"Screenshot saved: {screenshot_path}")

                    screenshot_png = driver.get_screenshot_as_png()
                    # Capture screenshot and attach it to Allure
                    allure.attach(
                        screenshot_png,
                        name=f"{item.name}_{timestamp}",
                        attachment_type=allure.attachment_type.PNG
                    )
                    logger.info(f"Screenshot for failed test '{item.name}' attached to Allure.")

                    # 2. Save the screenshot in base64 inside the report object for pytest-html
                    rep._html_screenshot = base64.b64encode(screenshot_png).decode("utf-8")

                except Exception as e:
                    logger.error(f"Failed to capture screenshot: {e}")

@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_html(report, data):
    """ Official pytest-html hook for modifying results table cells.
        Inserts a screenshot from the previously saved _html_screenshot attribute.  """
    screenshot = getattr(report, "_html_screenshot", None)
    if screenshot:
        # Add the screenshot's HTML code to the report data list
        html = f"""
        <div style="margin: 10px 0;">
            <style>
                .screenshot-img {{
                    width: 600px; 
                    border: 2px solid #444; 
                    border-radius: 8px; 
                    cursor: zoom-in;
                    transition: transform 0.2s;
                    display: block;
                }}
                .screenshot-img:hover {{
                    transform: scale(1.02);
                    border-color: #007bff;
                }}
            </style>
            <img src="data:image/png;base64,{screenshot}" 
                 class="screenshot-img"
                 onclick="window.open(this.src)" 
                 title="Press to open full size"/>
        </div>
        """
        data.append(html)

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
    app_config.ensure_directories()
    app_config.print_config()

    logger.info("\n" + "="*50)
    logger.info("PYTEST: All tests execution started")
    logger.info(f"(ENVIRONMENT: {app_config.ENVIRONMENT})")
    logger.info("="*50)

    if os.path.exists('/.dockerenv'):
        print("🚀 Running inside DOCKER container")
    else:
        print("💻 Running LOCALLY (Host machine)")

    # Заголовок для HTML отчета
    if hasattr(config, "_metadata"):
        config._metadata['Project Name'] = 'Juice Shop UI Automation'


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

@pytest.fixture(scope="session", autouse=True)
def wait_for_app_ready():
    """
    CI-safe healthcheck.
    Blocks test execution until the application becomes reachable.
    """

    web_base_url = os.getenv("WEB_BASE_URL")
    assert web_base_url, "WEB_BASE_URL is not set"

    # IMPORTANT: do NOT use /#/login for healthcheck
    # Hash URLs are client-side only
    health_url = web_base_url.rstrip("/")

    timeout = 90
    interval = 3
    end_time = time.time() + timeout

    logger.info(f"🔎 Waiting for application to be ready: {health_url}")

    last_error = None

    while time.time() < end_time:
        try:
            response = requests.get(health_url, timeout=5)
            if response.status_code < 500:
                logger.info("✅ Application is reachable")
                return
        except Exception as e:
            last_error = e

        time.sleep(interval)

    pytest.exit(
        f"❌ Application is not reachable after {timeout}s\n"
        f"URL: {health_url}\n"
        f"Last error: {last_error}",
        returncode=1
    )

def pytest_runtest_setup(item):
    """Hook: before each test setup"""
    print(f" [HOOK] Test setup: {item.name}")

def pytest_runtest_teardown(item):
    """Hook: after each test teardown"""
    print(f" [HOOK] Test completion: {item.name}")

def pytest_collection_modifyitems(items):
    """Hook: after collecting all tests"""
    print(f"\n[HOOK] Tests collected: {len(items)}")
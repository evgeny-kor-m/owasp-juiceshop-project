import pytest
import logging
from test_automation_framework.config.config import Config

logger = logging.getLogger(__name__)

class BaseTest:
    """
    Base test class.
    Provides common fixtures and helpers.
    """
    @pytest.fixture(autouse=True)
    def setup_base(self, api_client, api_base_url):
        # Expose fixtures as instance attributes
        self.api = api_client
        self.api_url = api_base_url
        self.config = Config
        # self.db = db_connection
        logger.info(f"Setup API base settings")

    def get_token_header(self, token):
        """Build Authorization header"""
        return {"Authorization": f"Bearer {token}"}

class BaseUITest(BaseTest):
    """
    Base class for UI tests.
    Extends BaseTest with browser support.
    """
    @pytest.fixture(autouse=True)
    def setup_ui(self, browser, web_base_url, request):
        # Initialize browser only for tests inheriting from BaseUITest
        self.driver = browser
        self.web_url = web_base_url

        # Attach driver to the test request for crash handling in conftest.py
        if request.node:
            request.node.driver = self.driver

        logger.info(f"Setup UI base settings")
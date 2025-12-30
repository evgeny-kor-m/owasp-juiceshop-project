import pytest
from test_automation_framework.config.config import Config

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

    def get_token_header(self, token):
        """Build Authorization header"""
        return {"Authorization": f"Bearer {token}"}

class BaseUITest(BaseTest):
    """
    Base class for UI tests.
    Extends BaseTest with browser support.
    """

    @pytest.fixture(autouse=True)
    def setup_ui(self, browser):
        # Initialize browser only for tests inheriting from BaseUITest
        self.driver = browser
# test_api_juceshop.py
import logging
from test_automation_framework.api.api_service import AuthAPI, BasketAPI, generate_random_email

logger = logging.getLogger(__name__)

def test_full_e2e_flow_with_api(api_base_url, api_session):
    """
    Testing the full End-to-End flow using the API.
    """

    logger.info("--- Starting E2E Test for OWASP Juice Shop (with API) ---")

    # Step 1: Register a new user
    logger.info("1. Registering a new user...")
    auth_api = AuthAPI(api_session, api_base_url)
    new_email = generate_random_email()
    password = "MyStrongPassword123"
    register_response = auth_api.register_new_user(new_email, password)
    assert register_response.status_code == 201, f"Registration failed: {register_response.status_code}"
    logger.info(f"    User {new_email} successfully registered.")

    # Step 2: Log in to the system
    logger.info("2. Logging in to the system...")
    login_response = auth_api.login_with_creds(new_email, password)
    assert login_response.status_code == 200, f"Login failed: {login_response.status_code}"
    basket_id = login_response.json().get("authentication", {}).get("bid")
    assert basket_id is not None, "Basket ID was not received after login."
    logger.info(f"    Successful login. Basket ID received - {basket_id}")
    auth_token = login_response.json().get("authentication", {}).get("token")
    assert auth_token is not None, "Authentication token was not received after login."
    api_session.headers.update({"Authorization": f"Bearer {auth_token}"})
    logger.info("    Authentication token added to session headers.")

    # Create the basket object after login
    basket_api = BasketAPI(api_session, api_base_url, basket_id)

    # Step 3: Add a product to the basket
    logger.info("3. Adding a product to the basket...")
    product_id = 1
    add_item_response = basket_api.add_item_to_basket(product_id)
    assert add_item_response.status_code == 200, f"Failed to add product to basket: {add_item_response.status_code}"
    logger.info(f"    Product (ID: {product_id}) successfully added to the basket.")

    # Step 4: Verify the product is in the basket
    logger.info("4. Checking basket contents...")
    basket_response = basket_api.get_basket_content()
    assert basket_response.status_code == 200, f"Failed to retrieve basket contents: {basket_response.status_code}"
    basket_items = basket_response.json().get("data", {}).get("Products", [])
    assert len(basket_items) > 0, "Basket is empty."
    assert basket_items[0].get("id") == product_id, "Incorrect product in the basket."
    logger.info("    Product successfully found in the basket.")

    # Step 5: Complete the order
    logger.info("5. Completing the order...")
    checkout_response = basket_api.checkout()
    assert checkout_response.status_code == 200, f"Failed to complete the order: {checkout_response.status_code}"
    logger.info("    Order successfully completed!")
    logger.info("\n--- End-to-End test successfully finished ---")
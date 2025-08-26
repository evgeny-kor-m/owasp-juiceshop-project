# test_api_juceshop.py
from test_automation_framework.api.api_service import AuthAPI, BasketAPI, generate_random_email

def test_full_e2e_flow_with_api(base_url, api_session):
    """
    Тестирование полного End-to-End потока с использованием API.
    """
    print("\n--- Запуск E2E-теста для OWASP Juice Shop (с API) ---")

    # Шаг 1: Регистрация нового пользователя
    print("1. Регистрация нового пользователя...")
    auth_api = AuthAPI(api_session, base_url)
    new_email = generate_random_email()
    password = "MyStrongPassword123"
    register_response = auth_api.register_new_user(new_email, password)
    assert register_response.status_code == 201, f"Регистрация не удалась: {register_response.status_code}"
    print(f"    Пользователь {new_email} успешно зарегистрирован.")

    # Шаг 2: Вход в систему
    print("2. Вход в систему...")
    login_response = auth_api.login_with_creds(new_email, password)
    assert login_response.status_code == 200, f"Вход не удался: {login_response.status_code}"
    basket_id = login_response.json().get("authentication", {}).get("bid")
    assert basket_id is not None, "ID корзины не получен после входа."
    print("    Успешный вход в систему. ID корзины получен.")

    # Создание объекта корзины после входа
    basket_api = BasketAPI(api_session, base_url, basket_id)

    # Шаг 3: Добавление товара в корзину
    print("3. Добавление товара в корзину...")
    product_id = 1
    add_item_response = basket_api.add_item_to_basket(product_id)
    assert add_item_response.status_code == 201, f"Не удалось добавить товар в корзину: {add_item_response.status_code}"
    print(f"    Товар (ID: {product_id}) успешно добавлен в корзину.")

    # Шаг 4: Проверка, что товар в корзине
    print("4. Проверка содержимого корзины...")
    basket_response = basket_api.get_basket_content()
    assert basket_response.status_code == 200, f"Не удалось получить содержимое корзины: {basket_response.status_code}"
    basket_items = basket_response.json().get("data", {}).get("Products", [])
    assert len(basket_items) > 0, "Корзина пуста."
    assert basket_items[0].get("id") == product_id, "В корзине неверный товар."
    print("    Товар успешно найден в корзине.")

    # Шаг 5: Оформление заказа
    print("5. Оформление заказа...")
    checkout_response = basket_api.checkout()
    assert checkout_response.status_code == 200, f"Не удалось оформить заказ: {checkout_response.status_code}"
    print("    Заказ успешно оформлен!")
    print("\n--- End-to-End тест успешно завершен ---")

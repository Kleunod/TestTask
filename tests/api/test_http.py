import requests
import pytest

# Функція для створення користувача і отримання API ключа
@pytest.mark.user_create
def create_user():
    url = "https://favqs.com/api/users"
    payload = {
        "user": {
            "login": "test_user",
            "email": "test@example.com",
            "password": "test_password"
        }
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 201, f"Failed to create user: {response.text}"
    api_key = response.json()['user']['api_key']
    return api_key

# Функція для отримання інформації про користувача за допомогою API ключа
@pytest.mark.user_get_info
def get_user_info(api_key):
    url = "https://favqs.com/api/users/me"
    headers = {
        "Authorization": f"Token token={api_key}"
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, f"Failed to get user info: {response.text}"
    return response.json()

# Перший тест: Створення користувача та перевірка полів login та email
@pytest.mark.user_create_and_check
def test_create_user_and_check_fields():
    api_key = create_user()
    user_info = get_user_info(api_key)
    assert user_info['login'] == "test_user", "Incorrect login returned"
    assert user_info['email'] == "test@example.com", "Incorrect email returned"

# Додаткова функція для оновлення налаштувань користувача
@pytest.mark.update_user
def update_user_settings(api_key, new_login, new_email):
    url = "https://favqs.com/api/users/me"
    headers = {
        "Authorization": f"Token token={api_key}"
    }
    payload = {
        "user": {
            "login": new_login,
            "email": new_email
        }
    }
    response = requests.put(url, headers=headers, json=payload)
    assert response.status_code == 200, f"Failed to update user settings: {response.text}"
    return response.json()

# Другий тест: Оновлення користувача та перевірка оновлених полів login та email
@pytest.mark.update_test
def test_update_user_and_check_fields():
    api_key = create_user()
    new_login = "updated_user"
    new_email = "updated@example.com"
    update_user_settings(api_key, new_login, new_email)
    user_info = get_user_info(api_key)
    assert user_info['login'] == new_login, "Incorrect updated login returned"
    assert user_info['email'] == new_email, "Incorrect updated email returned"

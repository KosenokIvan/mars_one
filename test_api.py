from requests import get, post, delete

print(get("http://localhost:5000/api/v2/users").json())  # Корректный запрос
print(get("http://localhost:5000/api/v2/users/1").json())  # Корректный запрос
print(get("http://localhost:5000/api/v2/users/999").json())  # Несуществующий пользователь
print(post("http://localhost:5000/api/v2/users", json={
    "id": 45,
    "surname": "API_SURNAME",
    "name": "API_NAME",
    "age": 33,
    "email": "api_email@mars.org",
    "password": "API_PASSWORD",
    "address": "API_ADDRESS"
}).json())  # Корректный запрос
print(post("http://localhost:5000/api/v2/users", json={
    "id": 45,
    "surname": "API_SURNAME2",
    "name": "API_NAME2",
    "age": 34,
    "email": "api_email2@mars.org",
    "password": "API_PASSWORD2",
    "address": "API_ADDRESS2"
}).json())  # ID уже существует
print(post("http://localhost:5000/api/v2/users").json())  # Пустой запрос
print(get("http://localhost:5000/api/v2/users").json())  # Проверка добавления пользователя
print(delete("http://localhost:5000/api/v2/users/45").json())  # Корректный запрос
print(delete("http://localhost:5000/api/v2/users/450").json())  # Несущействующий пользователь

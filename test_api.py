from datetime import date, timedelta
from requests import get, post, delete, put

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
print(put("http://localhost:5000/api/v2/users/45", json={
    "surname": None,
    "name": None,
    "age": None,
    "email": None,
    "password": None,
    "position": "API_POSITION"
}).json())  # Корректный запрос (None - оставить параметр без изменений)
print(put("http://localhost:5000/api/v2/users/1", json={
    "name": "new name"
}).json())  # Недостаточно данных
print(put("http://localhost:5000/api/v2/users/450", json={
    "surname": None,
    "name": None,
    "age": None,
    "email": None,
    "password": None,
    "position": "API_POSITION2"
}).json())  # Несуществующий пользователь
print(post("http://localhost:5000/api/v2/users").json())  # Пустой запрос
print(get("http://localhost:5000/api/v2/users").json())  # Проверка добавления пользователя
print(delete("http://localhost:5000/api/v2/users/45").json())  # Корректный запрос
print(delete("http://localhost:5000/api/v2/users/450").json())  # Несуществующий пользователь

print(get("http://localhost:5000/api/v2/jobs").json())  # Корректный запрос
print(get("http://localhost:5000/api/v2/jobs/1").json())  # Корректный запрос
print(get("http://localhost:5000/api/v2/jobs/999").json())  # Несуществующая работа
print(post("http://localhost:5000/api/v2/jobs", json={
    "id": 45,
    "team_leader": 1,
    "job": "API_JOB",
    "work_size": 10,
    "collaborators": "2, 3",
    "end_date": (date.today() + timedelta(days=2)).toordinal(),
    "is_finished": False
}).json())  # Корректный запрос
print(post("http://localhost:5000/api/v2/jobs", json={
    "id": 45,
    "team_leader": 2,
    "job": "API_JOB2",
    "work_size": 3,
    "collaborators": "2, 3",
    "end_date": date.today().toordinal(),
    "is_finished": True
}).json())  # Работа уже существует
print(post("http://localhost:5000/api/v2/jobs", json={
    "id": 450,
    "team_leader": 450,
    "job": "API_JOB3",
    "work_size": 1,
    "collaborators": "1, 3",
    "end_date": (date.today() + timedelta(days=1)).toordinal(),
    "is_finished": False
}).json())  # Несуществующий тимлидер
print(post("http://localhost:5000/api/v2/jobs", json={
    "id": 460,
    "team_leader": 1,
    "collaborators": "2",
    "is_finished": True
}).json())  # Недостаточно данных
print(put("http://localhost:5000/api/v2/jobs/45", json={
    "team_leader": None,
    "job": None,
    "work_size": 5,
    "collaborators": "2, 3, 4",
    "end_date": (date.today() + timedelta(days=1)).toordinal(),
    "is_finished": True
}).json())  # Корректный запрос
print(put("http://localhost:5000/api/v2/jobs/450", json={
    "team_leader": 1,
    "job": "...",
    "work_size": None,
    "collaborators": None,
    "end_date": None,
    "is_finished": None
}).json())  # Несуществующая работа
print(put("http://localhost:5000/api/v2/jobs/45", json={
    "team_leader": 450,
    "job": None,
    "work_size": None,
    "collaborators": "2, 4",
    "end_date": (date.today() + timedelta(days=3)).toordinal(),
    "is_finished": False
}).json())  # Несуществующий тимлидер
print(put("http://localhost:5000/api/v2/jobs/1", json={
    "work_size": 5,
    "collaborators": "2, 3, 4",
    "end_date": (date.today() + timedelta(days=1)).toordinal()
}).json())  # Недостаточно данных
print(get("http://localhost:5000/api/v2/jobs").json())  # Проверка добавления записи
print(delete("http://localhost:5000/api/v2/jobs/45").json())  # Корректный запрос
print(delete("http://localhost:5000/api/v2/jobs/450").json())  # Несуществующая запись

# SkinsMarket — Django проект

Маркетплейс скінів для Dota 2, CS2 та Rust.

## Швидкий старт

```bash
# 1. Встановити залежності
pip install -r requirements.txt

# 2. Міграції
python manage.py makemigrations
python manage.py migrate

# 3. Створити суперкористувача
python manage.py createsuperuser

# 4. Наповнити тестовими даними
python manage.py shell < seed.py

# 5. Запустити сервер
python manage.py runserver
```

Відкрий: http://127.0.0.1:8000

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

## Структура лабораторних / комітів

```
git init
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Лаб 1 — початковий проект
git add .
git commit -m "lab1: init django project with app and templates"
git push -u origin main

# Лаб 2 — моделі та адмінка
git add skins/models.py skins/admin.py
git commit -m "lab2: add models (Game, Skin, Cart, Order, Review) and admin config"
git push

# Лаб 3 — головна сторінка, хедер, футер
git add templates/ static/
git commit -m "lab3: main page with header, footer, game categories, DB content"
git push

# Лаб 4 — сторінка скіна та категорії
git add templates/skins/skin_detail.html templates/skins/game_skins.html skins/views.py
git commit -m "lab4: skin detail page and category (game) page with buy button"
git push

# Лаб 5 — кошик, форми (відгуки, розсилка)
git add templates/skins/cart.html templates/skins/checkout.html skins/forms.py
git commit -m "lab5: cart, checkout, review form, newsletter form, avg rating"
git push

# Лаб 6 — авторизація, кабінет, зміна паролю
git add templates/registration/ skins/views.py
git commit -m "lab6: auth (login/logout/register), profile, password change/reset via email"
git push
```

## Адмін-панель
http://127.0.0.1:8000/admin/

## Функціонал
- Каталог скінів з фільтрами (гра, рідкість, ціна, пошук)
- Сторінка кожної гри (категорія)
- Сторінка скіна з фото, float-value, відгуками та оцінками
- Кошик та оформлення замовлення
- Продаж власних скінів
- Реєстрація / вхід / вихід / зміна паролю / відновлення через email
- Особистий кабінет (замовлення, власні скіни)
- Адмін бачить всі замовлення
- Підписка на розсилку (footer-форма)
- DRY: base.html з header та footer

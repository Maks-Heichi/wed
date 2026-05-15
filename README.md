# Django Catalog Project

Учебный проект на Django с приложением `catalog`.

## Что реализовано

- создан Django-проект с конфигурацией `config`;
- создано и подключено приложение `catalog`;
- настроены маршруты через `include` в основном `urls.py`;
- реализованы контроллеры для главной страницы и страницы контактов;
- добавлены Bootstrap-шаблоны `home.html` и `contacts.html`;
- подключена PostgreSQL, параметры БД вынесены в `.env`;
- добавлены модели `Category` и `Product`, миграции и админка;
- подготовлены фикстуры и команда `load_test_products`.

## Страницы

- `/` и `/home/` — главная страница;
- `/contacts/` — страница контактов;
- `/admin/` — административная панель.

Все URL-адреса заканчиваются на `/`.

## База данных

1. Скопировать шаблон окружения:
   - `copy .env.example .env` (Windows) или `cp .env.example .env` (Linux/macOS)
2. Указать в `.env` параметры PostgreSQL.
3. Создать пользователя и базу в pgAdmin или выполнить `scripts/init_postgres.sql`.
4. При ошибке доступа к схеме `public` — `scripts/fix_public_schema.sql`.

## Запуск проекта

1. Создать и активировать виртуальное окружение.
2. Установить зависимости:
   - `pip install -r requirements.txt`
3. Выполнить миграции:
   - `python manage.py migrate`
4. Загрузить тестовые данные (опционально):
   - `python manage.py load_test_products`
5. Создать суперпользователя:
   - `python manage.py createsuperuser`
6. Запустить сервер:
   - `python manage.py runserver`

После запуска проект доступен по адресу: `http://127.0.0.1:8000/`.

## Фикстуры и команды

- `catalog/fixtures/categories.json` — категории;
- `catalog/fixtures/products.json` — продукты;
- `python manage.py loaddata categories products` — загрузка фикстур;
- `python manage.py load_test_products` — очистка каталога и повторная загрузка фикстур.

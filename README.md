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
- подготовлены фикстуры и команда `load_test_products`;
- на главной странице выводится список товаров через `Product.objects.all()` и цикл в шаблоне;
- описание товара на главной обрезается до первых 100 символов;
- добавлен контроллер `product_detail`: товар извлекается по `pk` через ORM и передаётся в шаблон;
- добавлена страница товара `product_detail.html` (название, описание, цена, изображение, категория, даты);
- реализованы переходы с главной на карточку товара и обратно;
- выделен базовый шаблон `base.html` (шапка, подвал, Bootstrap, блоки `title` и `content`);
- создан подшаблон `includes/menu.html`, подключается во все страницы каталога;
- шаблоны `home.html`, `product_detail.html` и `contacts.html` наследуют `base.html`;
- добавлена модель `ContactMessage`, форма `ContactForm` с валидацией и сохранением в БД;
- сообщения формы отображаются в админ-панели.

## Страницы

- `/` и `/home/` — главная страница со списком товаров;
- `/products/<id>/` — подробная информация о товаре (`product_detail`);
- `/contacts/` — страница контактов с формой обратной связи;
- `/admin/` — административная панель.

Все URL-адреса заканчиваются на `/`.

## Шаблоны

- `templates/catalog/base.html` — общий каркас страницы;
- `templates/catalog/includes/menu.html` — главное меню;
- `templates/catalog/home.html` — каталог товаров;
- `templates/catalog/product_detail.html` — карточка товара;
- `templates/catalog/contacts.html` — контакты и форма.

Медиафайлы (изображения товаров) отдаются в режиме `DEBUG` по адресу `/media/`.

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

Примеры страниц:

- `http://127.0.0.1:8000/` — список товаров;
- `http://127.0.0.1:8000/products/1/` — товар с идентификатором 1.

Для работы каталога используйте `python manage.py runserver`, а не `python main.py` (старый HTTP-сервер без маршрута `/products/`).

## Фикстуры и команды

- `catalog/fixtures/categories.json` — категории;
- `catalog/fixtures/products.json` — продукты;
- `python manage.py loaddata categories products` — загрузка фикстур;
- `python manage.py load_test_products` — очистка каталога и повторная загрузка фикстур.

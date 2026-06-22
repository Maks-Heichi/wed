# Проект каталога на Django

Учебный проект на Django с приложениями `catalog`, `blog` и `users`.

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
- сообщения формы отображаются в админ-панели;
- контроллеры приложения `catalog` переведены на CBV: `ProductListView`, `ProductDetailView`, `ContactView`;
- для главной страницы используется `ListView` с `Product.objects.all()`;
- для страницы товара используется `DetailView` с получением объекта по `pk`;
- для страницы контактов используется `View` с методами `get` и `post`;
- создано приложение `blog`, зарегистрировано в `INSTALLED_APPS`;
- добавлен файл `blog/urls.py`, маршруты подключены через `include` с префиксом `blogs/`;
- добавлена модель `BlogPost` с полями: заголовок, содержимое, превью, дата создания, признак публикации, количество просмотров;
- в модели `BlogPost` описаны `Meta`, `verbose_name`, `verbose_name_plural` и метод `__str__`;
- для блога реализован полный CRUD на CBV: `BlogPostListView`, `BlogPostDetailView`, `BlogPostCreateView`, `BlogPostUpdateView`, `BlogPostDeleteView`;
- добавлена форма `BlogPostForm` для создания и редактирования записей;
- блоговые записи зарегистрированы в админ-панели (`BlogPostAdmin`);
- шаблоны блога наследуют `base.html` и используют главное меню через `includes/menu.html`;
- в `BlogPostListView.get_queryset()` выводятся только опубликованные записи;
- в `BlogPostDetailView.get_object()` увеличивается счётчик просмотров;
- в `BlogPostUpdateView` через `success_url` после редактирования выполняется переход на страницу статьи;
- реализован CRUD для продуктов через `ProductForm` (`ProductCreateView`, `ProductUpdateView`, `ProductDeleteView`);
- список запрещённых слов вынесен в настройки `FORBIDDEN_WORDS` в `config/settings.py`, валидация в `clean_name` и `clean_description` (регистр игнорируется);
- в `clean_price` проверяется, что цена не может быть отрицательной;
- стилизация полей формы продуктов выполняется в методе `__init__` (`form-control`, `form-check-input`);
- в `clean_image` проверяются формат (JPEG/PNG) и размер загружаемого файла (не более 5 МБ);
- создано приложение `users`, зарегистрировано в `INSTALLED_APPS`;
- модель `User` наследуется от `AbstractUser`, `USERNAME_FIELD = "email"`;
- в модели пользователя добавлены поля: аватар, номер телефона, страна;
- настроена кастомная модель пользователя через `AUTH_USER_MODEL = "users.User"`;
- реализована регистрация (`UserRegisterForm`, `RegisterView`) с подтверждением пароля;
- после регистрации отправляется приветственное письмо через SMTP (`send_mail`);
- реализована авторизация по email и паролю (`UserLoginForm`, `UserLoginView`);
- настроены `LOGIN_URL`, `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL`;
- доступ к просмотру, созданию, изменению и удалению продуктов закрыт через `LoginRequiredMixin`;
- список товаров на главной странице доступен всем пользователям, включая анонимных;
- в меню добавлены ссылки «Войти», «Регистрация» и «Выйти».

## Страницы

- `/` и `/home/` — главная страница со списком товаров (доступна всем);
- `/products/create/` — создание продукта (только для авторизованных);
- `/products/<id>/` — подробная информация о товаре (только для авторизованных);
- `/products/<id>/update/` — редактирование продукта (только для авторизованных);
- `/products/<id>/delete/` — удаление продукта (только для авторизованных);
- `/users/register/` — регистрация пользователя;
- `/users/login/` — авторизация пользователя;
- `/users/logout/` — выход из системы;
- `/contacts/` — страница контактов с формой обратной связи;
- `/blogs/` — список опубликованных статей (`blog:list`);
- `/blogs/create/` — создание статьи (`blog:create`);
- `/blogs/<id>/` — просмотр статьи (`blog:detail`);
- `/blogs/<id>/update/` — редактирование статьи (`blog:update`);
- `/blogs/<id>/delete/` — удаление статьи (`blog:delete`);
- `/admin/` — административная панель.

Все URL-адреса заканчиваются на `/`.

## Шаблоны

- `templates/catalog/base.html` — общий каркас страницы;
- `templates/catalog/includes/menu.html` — главное меню;
- `templates/catalog/home.html` — каталог товаров;
- `templates/catalog/product_detail.html` — карточка товара;
- `templates/catalog/contacts.html` — контакты и форма;
- `templates/blog/blogpost_list.html` — список статей;
- `templates/blog/blogpost_detail.html` — просмотр статьи;
- `templates/blog/blogpost_form.html` — форма создания и редактирования;
- `templates/blog/blogpost_confirm_delete.html` — подтверждение удаления;
- `templates/users/register.html` — регистрация пользователя;
- `templates/users/login.html` — авторизация пользователя.

Медиафайлы (изображения товаров и превью статей) отдаются в режиме `DEBUG` по адресу `/media/`.

## База данных

1. Скопировать шаблон окружения:
   - `copy .env.example .env` (Windows) или `cp .env.example .env` (Linux/macOS)
2. Указать в `.env` параметры PostgreSQL и почты (`EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`).
3. Создать пользователя и базу в pgAdmin или выполнить `scripts/init_postgres.sql`.
4. При ошибке доступа к схеме `public` — `scripts/fix_public_schema.sql`.
5. После подключения кастомной модели пользователя (`AUTH_USER_MODEL`) при необходимости пересоздайте базу данных и выполните миграции заново:
   - `python manage.py migrate`

## Запуск проекта

1. Создать и активировать виртуальное окружение.
2. Установить зависимости:
   - `pip install -r requirements.txt`
3. Выполнить миграции:
   - `python manage.py migrate`
4. Загрузить тестовые данные (опционально):
   - `python manage.py load_test_products`
5. Создать суперпользователя:
   - `python manage.py createsuperuser` (в качестве логина укажите email)
6. Запустить сервер:
   - `python manage.py runserver`

После запуска проект доступен по адресу: `http://127.0.0.1:8000/`.

Примеры страниц:

- `http://127.0.0.1:8000/` — список товаров;
- `http://127.0.0.1:8000/products/1/` — товар с идентификатором 1;
- `http://127.0.0.1:8000/blogs/` — список статей;
- `http://127.0.0.1:8000/blogs/create/` — создание статьи.

Для работы каталога и блога используйте `python manage.py runserver`, а не `python main.py` (старый HTTP-сервер без маршрутов `/products/` и `/blogs/`).

## Фикстуры и команды

- `catalog/fixtures/categories.json` — категории;
- `catalog/fixtures/products.json` — продукты;
- `python manage.py loaddata categories products` — загрузка фикстур;
- `python manage.py load_test_products` — очистка каталога и повторная загрузка фикстур.

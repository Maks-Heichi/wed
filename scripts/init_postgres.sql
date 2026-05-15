-- Создание пользователя и базы (pgAdmin или psql от postgres).
-- Пароль пользователя должен совпадать с DATABASE_PASSWORD в .env.

CREATE USER mydatabaseuser WITH PASSWORD 'mypassword';
CREATE DATABASE mydatabase OWNER mydatabaseuser ENCODING 'UTF8';
GRANT ALL PRIVILEGES ON DATABASE mydatabase TO mydatabaseuser;

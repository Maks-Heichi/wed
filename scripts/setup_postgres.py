"""Создание пользователя и базы PostgreSQL по переменным из .env."""

from __future__ import annotations

import argparse
import getpass
import os
import sys
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DB_NAME = os.getenv("DATABASE_NAME", "mydatabase")
DB_USER = os.getenv("DATABASE_USER", "mydatabaseuser")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "mypassword")
DB_HOST = os.getenv("DATABASE_HOST", "localhost")
DB_PORT = os.getenv("DATABASE_PORT", "5432")


def connect_as_postgres(password: str) -> psycopg2.extensions.connection:
    """Подключается к служебной базе postgres от имени суперпользователя."""
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password=password,
        host=DB_HOST,
        port=DB_PORT,
    )


def ensure_role(cursor: psycopg2.extensions.cursor) -> None:
    """Создаёт роль приложения, если её ещё нет."""
    cursor.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (DB_USER,))
    if cursor.fetchone():
        print(f"Пользователь {DB_USER} уже существует.")
        return

    cursor.execute(
        sql.SQL("CREATE USER {} WITH PASSWORD %s").format(sql.Identifier(DB_USER)),
        (DB_PASSWORD,),
    )
    print(f"Создан пользователь {DB_USER}.")


def ensure_database(cursor: psycopg2.extensions.cursor) -> None:
    """Создаёт базу проекта, если её ещё нет."""
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
    if cursor.fetchone():
        print(f"База данных {DB_NAME} уже существует.")
        return

    cursor.execute(
        sql.SQL("CREATE DATABASE {} OWNER {} ENCODING 'UTF8'").format(
            sql.Identifier(DB_NAME),
            sql.Identifier(DB_USER),
        )
    )
    print(f"Создана база данных {DB_NAME}.")


def verify_app_connection() -> bool:
    """Проверяет подключение с учётными данными из .env."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        conn.close()
        print("Проверка подключения приложения: OK")
        return True
    except psycopg2.Error as exc:
        print(f"Проверка подключения приложения не удалась: {exc}", file=sys.stderr)
        return False


def main() -> int:
    """Точка входа: инициализация PostgreSQL для Django."""
    parser = argparse.ArgumentParser(description="Инициализация PostgreSQL для Django")
    parser.add_argument(
        "--password",
        help="Пароль пользователя postgres (если не указан — запрос в консоли)",
    )
    args = parser.parse_args()

    postgres_password = args.password or getpass.getpass("Пароль пользователя postgres: ")

    try:
        conn = connect_as_postgres(postgres_password)
    except psycopg2.Error as exc:
        print(f"Не удалось подключиться как postgres: {exc}", file=sys.stderr)
        return 1

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    ensure_role(cursor)
    ensure_database(cursor)
    cursor.close()
    conn.close()

    return 0 if verify_app_connection() else 1


if __name__ == "__main__":
    raise SystemExit(main())

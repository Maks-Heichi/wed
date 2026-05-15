"""Мини-сервер: GET/HEAD → контакты из pages.html, POST → print в консоль, 404/500 из тех же секций."""

from __future__ import annotations

import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse
from urllib.parse import parse_qs

BASE_DIR = Path(__file__).resolve().parent
PAGES_FILE = BASE_DIR / "pages.html"

_SECTION_MARKERS = re.compile(r"<!--\s*section:(?P<name>\w+)\s*-->")


def read_pages_raw() -> str:
    """Читает pages.html целиком (with open)."""
    with open(PAGES_FILE, encoding="utf-8") as file:
        return file.read()


def parse_sections(text: str) -> dict[str, str]:
    """Делит текст по маркерам <!-- section:имя -->."""
    matches = list(_SECTION_MARKERS.finditer(text))
    if not matches:
        raise ValueError("В pages.html не найдены маркеры <!-- section:... -->")

    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        name = match.group("name")
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        chunk = text[start:end].strip()
        if not chunk:
            raise ValueError(f"Пустая секция: {name}")
        sections[name] = chunk
    return sections


def read_section_html(section: str) -> bytes:
    """Одна секция pages.html в байтах UTF-8."""
    raw = read_pages_raw()
    sections = parse_sections(raw)
    if section not in sections:
        raise KeyError(f"Нет секции {section!r} в {PAGES_FILE.name}")
    return sections[section].encode("utf-8")


def read_contacts_html() -> bytes:
    """Секция contacts."""
    return read_section_html("contacts")


def read_error_html(code: int) -> bytes:
    """Секция err404 или err500."""
    if code == 404:
        return read_section_html("err404")
    if code == 500:
        return read_section_html("err500")
    raise ValueError(f"Нет секции для HTTP {code}")


class ContactsHandler(BaseHTTPRequestHandler):
    """HTTP-обработчик приложения."""

    server_version = "HomeworkContacts/1.0"
    ROUTES = {
        "/": "home",
        "/home": "home",
        "/catalog": "catalog",
        "/category": "category",
        "/contacts": "contacts",
    }

    def send_error(self, code, message=None, explain=None):
        """404/500 из pages.html, остальное — как в базовом классе."""
        if code not in (404, 500):
            return super().send_error(code, message, explain)

        try:
            body = read_error_html(code)
        except (OSError, ValueError, KeyError):
            return super().send_error(code, message, explain)

        self.log_error("HTTP %s", code)
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.end_headers()
        if self.command != "HEAD":
            try:
                self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError):
                pass

    def _send_page(self, section: str) -> None:
        """200 + HTML секции; при сбое — 500."""
        try:
            body = read_section_html(section)
        except (OSError, ValueError, KeyError) as err:
            self.log_error("Не удалось загрузить секцию %s: %s", section, err)
            self.send_error(500)
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _resolve_route_section(self) -> str | None:
        """Возвращает имя секции по пути запроса."""
        parsed = urlparse(self.path)
        return self.ROUTES.get(parsed.path)

    def do_GET(self) -> None:
        """Отдает HTML-страницу по маршруту или 404."""
        section = self._resolve_route_section()
        if section is None:
            self.send_error(404)
            return
        self._send_page(section)

    def do_HEAD(self) -> None:
        """HEAD-версия do_GET без тела ответа."""
        section = self._resolve_route_section()
        if section is None:
            self.send_error(404)
            return
        self._send_page(section)

    def do_POST(self) -> None:
        """Печать тела POST, затем снова контакты."""
        try:
            length = int(self.headers.get("Content-Length", 0))
        except ValueError:
            self.log_error("Некорректный Content-Length")
            self.send_error(400)
            return

        try:
            raw = self.rfile.read(length)
            ctype = self.headers.get("Content-Type", "")

            if "application/x-www-form-urlencoded" in ctype:
                text = raw.decode("utf-8", errors="replace")
                data = parse_qs(text, keep_blank_values=True)
                print("POST form:", data)
            else:
                print("POST Content-Type:", ctype or "(нет)")
                print("POST body:", raw.decode("utf-8", errors="replace"))

            section = self._resolve_route_section()
            if section != "contacts":
                self.send_error(404)
                return
            self._send_page("contacts")
        except (OSError, KeyError, ValueError) as err:
            self.log_error("POST: %s", err)
            self.send_error(500)

    def do_PUT(self) -> None:
        """Для PUT возвращаем 404."""
        self.send_error(404)

    def do_DELETE(self) -> None:
        """Для DELETE возвращаем 404."""
        self.send_error(404)


def run(host: str = "127.0.0.1", port: int = 8000) -> None:
    """Старт HTTPServer (блокирует поток)."""
    with HTTPServer((host, port), ContactsHandler) as server:
        print(f"Сервер: http://{host}:{port}/")
        server.serve_forever()


if __name__ == "__main__":
    run()

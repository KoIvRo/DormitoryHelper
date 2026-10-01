"""Одноразовые административные команды приложения."""

from database.database import create_db
from database import models  # noqa: F401 — регистрирует модели в metadata


def main() -> None:
    """Идемпотентно создаёт отсутствующие таблицы."""
    create_db()


if __name__ == "__main__":
    main()

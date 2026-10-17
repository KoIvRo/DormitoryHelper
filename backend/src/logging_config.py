import json
import logging
import sys
from datetime import datetime, timezone

SERVICE_NAME = "dormitory-helper-backend"

# Служебные поля LogRecord. Остальные значения, переданные через ``extra``,
# являются полями события и должны попасть в итоговую JSON-запись.
_RESERVED_LOG_RECORD_FIELDS = {
    "args",
    "asctime",
    "color_message",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
    "taskName",
}


class JsonFormatter(logging.Formatter):
    """Преобразование одной записи LogRecord в один JSON-объект."""

    def format(self, record: logging.LogRecord) -> str:
        event = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc)
            .isoformat(timespec="milliseconds")
            .replace("+00:00", "Z"),
            "level": record.levelname.lower(),
            "message": record.getMessage(),
            "service.name": SERVICE_NAME,
            "logger": record.name,
        }

        for key, value in record.__dict__.items():
            if key not in _RESERVED_LOG_RECORD_FIELDS and not key.startswith("_"):
                event[key] = value

        if record.exc_info:
            event["exception.type"] = record.exc_info[0].__name__
            event["exception.message"] = str(record.exc_info[1])
            event["exception.stacktrace"] = self.formatException(record.exc_info)

        return json.dumps(event, ensure_ascii=False, default=str)


def configure_logging() -> None:
    """Настройка единого формата логов API и Uvicorn в stdout."""

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    root_logger = logging.getLogger()
    root_logger.handlers = [handler]
    root_logger.setLevel(logging.INFO)

    # Uvicorn создаёт собственные обработчики до импорта приложения.
    # Заменяем их, чтобы системные сообщения также записывались в JSON.
    for logger_name in ("uvicorn", "uvicorn.error"):
        uvicorn_logger = logging.getLogger(logger_name)
        uvicorn_logger.handlers = [handler]
        uvicorn_logger.propagate = False

    # HTTP-запросы журналируются в RequestLoggingMiddleware вместе с request_id
    # и временем выполнения, поэтому дублирующий access-log Uvicorn отключён.
    logging.getLogger("uvicorn.access").disabled = True


def log_fields(**fields):
    """Удаление пустых полей из записи лога."""

    return {key: value for key, value in fields.items() if value is not None}

"""Prometheus/OpenMetrics collectors for DormitoryHelper."""

from prometheus_client import Counter
from prometheus_fastapi_instrumentator import Instrumentator


USER_REGISTRATIONS = Counter(
    "dormitory_helper_user_registrations_total",
    "Number of successfully registered users.",
)

USER_LOGINS = Counter(
    "dormitory_helper_user_logins_total",
    "Number of user login attempts grouped by outcome.",
    ("outcome",),
)

ANNOUNCEMENTS_CREATED = Counter(
    "dormitory_helper_announcements_created_total",
    "Number of successfully created announcements grouped by category.",
    ("category",),
)

ANNOUNCEMENTS_UPDATED = Counter(
    "dormitory_helper_announcements_updated_total",
    "Number of successfully updated announcements grouped by category.",
    ("category",),
)

ANNOUNCEMENTS_DELETED = Counter(
    "dormitory_helper_announcements_deleted_total",
    "Number of successfully deleted announcements grouped by category.",
    ("category",),
)


def configure_metrics(app) -> None:
    """Instrument FastAPI and expose the unauthenticated /metrics endpoint."""
    Instrumentator(
        excluded_handlers=["/metrics", "/health/.*"],
        should_group_status_codes=False,
        should_ignore_untemplated=True,
        should_instrument_requests_inprogress=True,
        inprogress_name="dormitory_helper_http_requests_inprogress",
        inprogress_labels=True,
    ).instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)

import os
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


TARGET_URL = os.getenv("PROBE_TARGET_URL", "http://backend:8000/health/ready")
INTERVAL = float(os.getenv("PROBE_INTERVAL_SECONDS", "5"))
TIMEOUT = float(os.getenv("PROBE_TIMEOUT_SECONDS", "2"))

lock = threading.Lock()
state = {"success": 0, "duration": 0.0, "status_code": 0, "checks": 0}


def probe_forever() -> None:
    while True:
        started = time.monotonic()
        success, status_code = 0, 0
        try:
            with urllib.request.urlopen(TARGET_URL, timeout=TIMEOUT) as response:
                status_code = response.status
                success = int(200 <= status_code < 400)
        except urllib.error.HTTPError as error:
            status_code = error.code
        except (urllib.error.URLError, TimeoutError):
            pass
        duration = time.monotonic() - started
        with lock:
            state.update(
                success=success,
                duration=duration,
                status_code=status_code,
                checks=state["checks"] + 1,
            )
        time.sleep(max(0.0, INTERVAL - duration))


class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path not in ("/metrics", "/health"):
            self.send_error(404)
            return
        if self.path == "/health":
            body, content_type = b"ok\n", "text/plain"
        else:
            with lock:
                current = state.copy()
            target = TARGET_URL.replace("\\", "\\\\").replace('"', '\\"')
            body = (
                "# HELP dormitory_helper_probe_success Whether the last end-to-end probe succeeded.\n"
                "# TYPE dormitory_helper_probe_success gauge\n"
                f'dormitory_helper_probe_success{{target="{target}"}} {current["success"]}\n'
                "# HELP dormitory_helper_probe_duration_seconds Duration of the last probe.\n"
                "# TYPE dormitory_helper_probe_duration_seconds gauge\n"
                f'dormitory_helper_probe_duration_seconds{{target="{target}"}} {current["duration"]}\n'
                "# HELP dormitory_helper_probe_http_status_code HTTP status of the last probe, or 0 on transport error.\n"
                "# TYPE dormitory_helper_probe_http_status_code gauge\n"
                f'dormitory_helper_probe_http_status_code{{target="{target}"}} {current["status_code"]}\n'
                "# HELP dormitory_helper_probe_checks_total Number of completed probes.\n"
                "# TYPE dormitory_helper_probe_checks_total counter\n"
                f'dormitory_helper_probe_checks_total{{target="{target}"}} {current["checks"]}\n'
            ).encode()
            content_type = "text/plain; version=0.0.4; charset=utf-8"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, _format: str, *_args) -> None:
        return


if __name__ == "__main__":
    threading.Thread(target=probe_forever, daemon=True).start()
    ThreadingHTTPServer(("0.0.0.0", 9115), MetricsHandler).serve_forever()

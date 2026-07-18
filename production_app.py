from __future__ import annotations

import io
from collections import defaultdict, deque
from threading import Lock
from time import monotonic
from types import MethodType
from urllib.parse import urlsplit

from flask import Flask, Response, jsonify, request
from werkzeug.middleware.proxy_fix import ProxyFix

import database
import runtime_config
import web_app


MAX_REQUEST_BYTES = 64 * 1024
GENERAL_LIMIT = (300, 60)
AI_LIMIT = (30, 5 * 60)
AUTH_LIMIT = (20, 15 * 60)

app = Flask(__name__, static_folder=None)
app.config.update(
    MAX_CONTENT_LENGTH=MAX_REQUEST_BYTES,
    PROPAGATE_EXCEPTIONS=False,
)
if runtime_config.IS_PRODUCTION:
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

web_app.initialize_application()

rate_lock = Lock()
rate_buckets: dict[tuple[str, str], deque[float]] = defaultdict(deque)


def request_group() -> tuple[str, tuple[int, int]]:
    if request.path in {"/api/chat", "/api/caregiver-chat"}:
        return "ai", AI_LIMIT
    if request.path in {"/api/register", "/api/login", "/api/admin-login"}:
        return "auth", AUTH_LIMIT
    return "general", GENERAL_LIMIT


def rate_limit_exceeded() -> bool:
    group, (request_limit, window_seconds) = request_group()
    client_ip = request.remote_addr or "unknown"
    key = (client_ip, group)
    cutoff = monotonic() - window_seconds
    with rate_lock:
        bucket = rate_buckets[key]
        while bucket and bucket[0] <= cutoff:
            bucket.popleft()
        if len(bucket) >= request_limit:
            return True
        bucket.append(monotonic())
    return False


def origin_is_allowed() -> bool:
    origin = request.headers.get("Origin", "").rstrip("/")
    if not origin:
        return True
    parsed_origin = urlsplit(origin)
    if parsed_origin.scheme not in {"http", "https"} or not parsed_origin.netloc:
        return False
    if parsed_origin.netloc.casefold() == request.host.casefold():
        return True
    same_origin = request.host_url.rstrip("/")
    return origin == same_origin or origin in runtime_config.ALLOWED_ORIGINS


@app.before_request
def protect_request():
    if request.path == "/health":
        return None
    if request.method in {"POST", "PUT", "PATCH", "DELETE"} and not origin_is_allowed():
        return jsonify(error="Request origin is not allowed."), 403
    if rate_limit_exceeded():
        return jsonify(error="Too many requests. Please wait and try again."), 429
    return None


@app.after_request
def add_security_headers(response: Response) -> Response:
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = (
        "camera=(), geolocation=(), microphone=(self)"
    )
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; base-uri 'self'; form-action 'self'; "
        "frame-ancestors 'none'; object-src 'none'; img-src 'self' data:; "
        "font-src 'self'; style-src 'self'; script-src 'self'; connect-src 'self'"
    )
    if runtime_config.IS_PRODUCTION:
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
    if request.path.startswith("/api/") or request.path in {"/", "/index.html"}:
        response.headers["Cache-Control"] = "no-store"
    return response


@app.errorhandler(413)
def request_too_large(_error):
    return jsonify(error="Request is too large."), 413


@app.errorhandler(Exception)
def unexpected_error(error):
    app.logger.error("Unhandled request error: %s", type(error).__name__)
    if request.path.startswith("/api/") or request.path == "/health":
        return jsonify(error="AURA could not complete this request."), 500
    return Response("AURA could not load this page.", status=500, mimetype="text/plain")


@app.get("/health")
def health_check():
    try:
        with database.connect() as connection:
            connection.execute("SELECT 1").fetchone()
    except Exception:
        return jsonify(status="unhealthy", database="unavailable"), 503
    return jsonify(status="ok", database="available")


def dispatch_existing_handler() -> Response:
    handler = web_app.AuraWebHandler.__new__(web_app.AuraWebHandler)
    handler.command = request.method
    handler.path = request.full_path[:-1] if request.full_path.endswith("?") else request.full_path
    handler.request_version = "HTTP/1.1"
    handler.requestline = f"{request.method} {handler.path} HTTP/1.1"
    handler.client_address = (request.remote_addr or "", 0)
    handler.headers = request.headers
    handler.rfile = io.BytesIO(request.get_data(cache=False))
    handler.wfile = io.BytesIO()

    response_state: dict[str, object] = {"status": 500, "headers": []}

    def send_response(_handler, status: int, message: str | None = None) -> None:
        response_state["status"] = status

    def send_header(_handler, name: str, value: str) -> None:
        response_state["headers"].append((name, value))

    def end_headers(_handler) -> None:
        return None

    handler.send_response = MethodType(send_response, handler)
    handler.send_header = MethodType(send_header, handler)
    handler.end_headers = MethodType(end_headers, handler)

    if request.method in {"GET", "HEAD"}:
        handler.do_GET()
    elif request.method == "POST":
        handler.do_POST()
    else:
        return Response(status=405, headers={"Allow": "GET, HEAD, POST"})

    body = b"" if request.method == "HEAD" else handler.wfile.getvalue()
    response = Response(body, status=int(response_state["status"]))
    for name, value in response_state["headers"]:
        if name.lower() not in {"content-length", "connection", "server", "date"}:
            if name.lower() == "set-cookie":
                response.headers.add(name, value)
            else:
                response.headers[name] = value
    return response


@app.route("/", defaults={"path": ""}, methods=["GET", "HEAD", "POST"])
@app.route("/<path:path>", methods=["GET", "HEAD", "POST"])
def application_routes(path: str) -> Response:
    return dispatch_existing_handler()

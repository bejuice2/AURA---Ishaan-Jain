from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


BASE_DIR = Path(__file__).resolve().parent
ENVIRONMENT = os.getenv("AURA_ENV", "development").strip().lower()
IS_PRODUCTION = ENVIRONMENT == "production"


def env_flag(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_port() -> int:
    raw_value = os.getenv("PORT", "8000").strip()
    try:
        port = int(raw_value)
    except ValueError as error:
        raise RuntimeError("PORT must be a whole number.") from error
    if not 1 <= port <= 65535:
        raise RuntimeError("PORT must be between 1 and 65535.")
    return port


HOST = "0.0.0.0" if IS_PRODUCTION else "127.0.0.1"
PORT = env_port()
PUBLIC_DEMO = env_flag("AURA_PUBLIC_DEMO", False)
SECURE_COOKIES = IS_PRODUCTION
DATA_DIR = Path(os.getenv("AURA_DATA_DIR", str(BASE_DIR))).expanduser().resolve()
TIMEZONE_NAME = os.getenv("AURA_TIMEZONE", "").strip()
ALLOWED_ORIGINS = {
    origin.strip().rstrip("/")
    for origin in os.getenv("AURA_ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
}

try:
    CONFIGURED_TIMEZONE = ZoneInfo(TIMEZONE_NAME) if TIMEZONE_NAME else None
except ZoneInfoNotFoundError as error:
    raise RuntimeError(
        "AURA_TIMEZONE must be a valid IANA timezone name, such as America/New_York."
    ) from error


def local_now() -> datetime:
    if CONFIGURED_TIMEZONE is not None:
        return datetime.now(CONFIGURED_TIMEZONE)
    return datetime.now().astimezone()


def ensure_data_directory() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def production_configuration_errors() -> list[str]:
    if not IS_PRODUCTION:
        return []

    missing = []
    for name in (
        "OPENAI_API_KEY",
        "AURA_ADMIN_USERNAME",
        "AURA_ADMIN_PASSWORD",
        "AURA_TIMEZONE",
    ):
        if not os.getenv(name, "").strip():
            missing.append(name)

    errors = [f"Missing required environment variable: {name}" for name in missing]
    twilio_names = (
        "TWILIO_ACCOUNT_SID",
        "TWILIO_AUTH_TOKEN",
        "TWILIO_FROM_PHONE",
    )
    twilio_present = [bool(os.getenv(name, "").strip()) for name in twilio_names]
    if any(twilio_present) and not all(twilio_present):
        errors.append(
            "Twilio configuration is incomplete. Set all three TWILIO variables or none."
        )
    return errors

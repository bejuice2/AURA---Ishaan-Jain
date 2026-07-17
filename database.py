from __future__ import annotations

import csv
import hashlib
import hmac
import io
import json
import re
import secrets
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

import test_clock
import runtime_config


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = runtime_config.DATA_DIR / "aura.sqlite3"
EXPORT_PATH = runtime_config.DATA_DIR / "aura_task_attempts.csv"
DEFAULT_USER_ID = "patient-1"
PASSWORD_ITERATIONS = 120_000


DEFAULT_ROUTINES = [
    {
        "task_id": "brush-teeth",
        "task_name": "Brush teeth",
        "task_category": "Hygiene",
        "task_difficulty": 2,
        "task_importance": 4,
        "scheduled_time": "08:00",
        "time_of_day": "Morning",
        "repeat_schedule": "Daily",
        "instructions": [
            "Please go to the bathroom sink.",
            "Pick up your toothbrush.",
            "Put toothpaste on the brush.",
            "Brush your teeth.",
            "Rinse your mouth.",
        ],
        "active": True,
    },
    {
        "task_id": "breakfast",
        "task_name": "Eat breakfast",
        "task_category": "Meals",
        "task_difficulty": 2,
        "task_importance": 5,
        "scheduled_time": "08:30",
        "time_of_day": "Morning",
        "repeat_schedule": "Daily",
        "instructions": [
            "Please go to the kitchen.",
            "Sit at the table.",
            "Eat your breakfast.",
            "Take a drink of water.",
        ],
        "active": True,
    },
    {
        "task_id": "morning-medication",
        "task_name": "Morning medication",
        "task_category": "Medication",
        "task_difficulty": 4,
        "task_importance": 5,
        "scheduled_time": "09:00",
        "time_of_day": "Morning",
        "repeat_schedule": "Daily",
        "instructions": [
            "Please find your medication organizer.",
            "Open the morning section.",
            "Take the medicine exactly as prepared.",
            "Take a sip of water.",
        ],
        "active": True,
    },
    {
        "task_id": "hearing-aids",
        "task_name": "Put on hearing aids",
        "task_category": "Personal care",
        "task_difficulty": 3,
        "task_importance": 4,
        "scheduled_time": "09:15",
        "time_of_day": "Morning",
        "repeat_schedule": "Daily",
        "instructions": [
            "Please pick up your hearing aids.",
            "Put the left hearing aid in your left ear.",
            "Put the right hearing aid in your right ear.",
        ],
        "active": True,
    },
    {
        "task_id": "drink-water",
        "task_name": "Drink water",
        "task_category": "Hydration",
        "task_difficulty": 1,
        "task_importance": 3,
        "scheduled_time": "11:00",
        "time_of_day": "Morning",
        "repeat_schedule": "Daily",
        "instructions": [
            "Please pick up your water.",
            "Take a drink.",
        ],
        "active": True,
    },
    {
        "task_id": "lunch",
        "task_name": "Lunch",
        "task_category": "Meals",
        "task_difficulty": 2,
        "task_importance": 5,
        "scheduled_time": "12:30",
        "time_of_day": "Afternoon",
        "repeat_schedule": "Daily",
        "instructions": [
            "Please go to the kitchen.",
            "Sit at the table.",
            "Eat your lunch.",
        ],
        "active": True,
    },
    {
        "task_id": "exercises",
        "task_name": "Exercises",
        "task_category": "Activity",
        "task_difficulty": 4,
        "task_importance": 3,
        "scheduled_time": "16:00",
        "time_of_day": "Afternoon",
        "repeat_schedule": "Daily",
        "instructions": [
            "Please sit in a safe chair.",
            "Lift your feet slowly.",
            "Rest for a moment.",
            "Stretch your arms gently.",
        ],
        "active": True,
    },
    {
        "task_id": "evening-medication",
        "task_name": "Evening medication",
        "task_category": "Medication",
        "task_difficulty": 4,
        "task_importance": 5,
        "scheduled_time": "19:00",
        "time_of_day": "Evening",
        "repeat_schedule": "Daily",
        "instructions": [
            "Please find your medication organizer.",
            "Open the evening section.",
            "Take the medicine exactly as prepared.",
            "Take a sip of water.",
        ],
        "active": True,
    },
    {
        "task_id": "charge-hearing-aids",
        "task_name": "Charge hearing aids",
        "task_category": "Personal care",
        "task_difficulty": 3,
        "task_importance": 4,
        "scheduled_time": "20:30",
        "time_of_day": "Evening",
        "repeat_schedule": "Daily",
        "instructions": [
            "Please take out your hearing aids.",
            "Put them in the charger.",
            "Make sure the charger light is on.",
        ],
        "active": True,
    },
    {
        "task_id": "bedtime",
        "task_name": "Bedtime routine",
        "task_category": "Sleep",
        "task_difficulty": 3,
        "task_importance": 4,
        "scheduled_time": "21:00",
        "time_of_day": "Evening",
        "repeat_schedule": "Daily",
        "instructions": [
            "Please go to your bedroom.",
            "Put on your pajamas.",
            "Turn off the bright lights.",
            "Get into bed.",
        ],
        "active": True,
    },
]


def connect() -> sqlite3.Connection:
    runtime_config.ensure_data_directory()
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA busy_timeout = 3000")
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def row_to_dict(row: sqlite3.Row | None) -> dict | None:
    if row is None:
        return None
    data = dict(row)
    if "instructions" in data and isinstance(data["instructions"], str):
        data["instructions"] = json.loads(data["instructions"])
    return data


def rows_to_dicts(rows: list[sqlite3.Row]) -> list[dict]:
    return [row_to_dict(row) for row in rows]


def public_account(row: sqlite3.Row | dict | None) -> dict | None:
    if row is None:
        return None
    data = dict(row)
    return {
        "username": data["username"],
        "patient_name": data["patient_name"],
        "caregiver_name": data["caregiver_name"],
        "has_phone": bool(data.get("caregiver_phone", "")),
        "phone_last4": str(data.get("caregiver_phone", ""))[-4:],
        "sms_enabled": bool(data.get("sms_enabled", 0)),
    }


def password_hash(password: str, salt_hex: str) -> str:
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt_hex),
        PASSWORD_ITERATIONS,
    )
    return digest.hex()


def token_hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def today_context() -> dict:
    now = test_clock.now()
    hour = now.hour
    if hour < 12:
        time_of_day = "Morning"
    elif hour < 17:
        time_of_day = "Afternoon"
    else:
        time_of_day = "Evening"

    return {
        "date": now.strftime("%Y-%m-%d"),
        "day_of_week": now.strftime("%A"),
        "time_of_day": time_of_day,
        "time": now.strftime("%H:%M"),
        "timestamp": now.isoformat(timespec="seconds"),
    }


def init_db() -> None:
    with connect() as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS routines (
                user_id TEXT NOT NULL,
                task_id TEXT NOT NULL,
                task_name TEXT NOT NULL,
                task_category TEXT NOT NULL,
                task_difficulty INTEGER NOT NULL,
                task_importance INTEGER NOT NULL,
                scheduled_time TEXT NOT NULL,
                time_of_day TEXT NOT NULL,
                repeat_schedule TEXT NOT NULL,
                instructions TEXT NOT NULL,
                active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                PRIMARY KEY (user_id, task_id)
            );

            CREATE TABLE IF NOT EXISTS task_attempts (
                attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                date TEXT NOT NULL,
                day_of_week TEXT NOT NULL,
                time_of_day TEXT NOT NULL,
                scheduled_time TEXT NOT NULL,
                task_id TEXT NOT NULL,
                task_name TEXT NOT NULL,
                task_category TEXT NOT NULL,
                task_difficulty INTEGER NOT NULL,
                task_importance INTEGER NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0,
                missed INTEGER NOT NULL DEFAULT 0,
                reminders_needed INTEGER NOT NULL DEFAULT 0,
                help_requested INTEGER NOT NULL DEFAULT 0,
                confusion_flag INTEGER NOT NULL DEFAULT 0,
                time_to_complete INTEGER,
                raw_performance_score REAL NOT NULL DEFAULT 0,
                adjusted_performance_score REAL NOT NULL DEFAULT 0,
                caregiver_alert INTEGER NOT NULL DEFAULT 0,
                notes TEXT NOT NULL DEFAULT '',
                started_at TEXT NOT NULL,
                completed_at TEXT
            );

            CREATE TABLE IF NOT EXISTS caregiver_notes (
                note_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                note TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS alerts (
                alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                date TEXT NOT NULL,
                severity TEXT NOT NULL,
                reason TEXT NOT NULL,
                task_id TEXT,
                task_name TEXT,
                patient_message TEXT,
                text_status TEXT NOT NULL DEFAULT '',
                acknowledged INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS summaries (
                summary_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                date TEXT NOT NULL,
                summary TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS caregiver_chat (
                message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                role TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS patient_caregiver_messages (
                message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                sender TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS accounts (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                password_salt TEXT NOT NULL,
                caregiver_password_hash TEXT NOT NULL,
                caregiver_password_salt TEXT NOT NULL,
                patient_name TEXT NOT NULL,
                caregiver_name TEXT NOT NULL,
                caregiver_phone TEXT NOT NULL DEFAULT '',
                sms_enabled INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS auth_tokens (
                token_hash TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                FOREIGN KEY (username) REFERENCES accounts(username)
            );

            CREATE TABLE IF NOT EXISTS app_settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """
        )

        migrate_routines_table(db)
        ensure_default_routines(DEFAULT_USER_ID, db=db)

        columns = {
            row["name"]
            for row in db.execute("PRAGMA table_info(accounts)").fetchall()
        }
        if "caregiver_password_hash" not in columns:
            db.execute(
                "ALTER TABLE accounts ADD COLUMN caregiver_password_hash TEXT"
            )
        if "caregiver_password_salt" not in columns:
            db.execute(
                "ALTER TABLE accounts ADD COLUMN caregiver_password_salt TEXT"
            )
        if "caregiver_phone" not in columns:
            db.execute(
                "ALTER TABLE accounts ADD COLUMN caregiver_phone TEXT NOT NULL DEFAULT ''"
            )
        if "sms_enabled" not in columns:
            db.execute(
                "ALTER TABLE accounts ADD COLUMN sms_enabled INTEGER NOT NULL DEFAULT 0"
            )
        db.execute(
            "DELETE FROM auth_tokens WHERE username NOT IN (SELECT username FROM accounts WHERE caregiver_password_hash IS NOT NULL AND caregiver_password_hash != '')"
        )
        db.execute(
            "DELETE FROM accounts WHERE caregiver_password_hash IS NULL OR caregiver_password_hash = ''"
        )
        migrate_default_user_data_to_single_account(db)
        db.commit()


def account_count() -> int:
    with connect() as db:
        return int(db.execute("SELECT COUNT(*) FROM accounts").fetchone()[0])


def get_setting(key: str, default: str = "") -> str:
    with connect() as db:
        row = db.execute(
            "SELECT value FROM app_settings WHERE key = ?",
            (key,),
        ).fetchone()
        if row is None:
            return default
        return str(row["value"])


def set_setting(key: str, value: str) -> None:
    context = today_context()
    with connect() as db:
        db.execute(
            """
            INSERT INTO app_settings (key, value, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET
                value = excluded.value,
                updated_at = excluded.updated_at
            """,
            (key, value, context["timestamp"]),
        )
        db.commit()


def list_accounts() -> list[dict]:
    with connect() as db:
        return [
            public_account(row)
            for row in db.execute(
                """
                SELECT username, patient_name, caregiver_name
                FROM accounts
                ORDER BY patient_name, username
                """
            ).fetchall()
        ]


def list_accounts_with_dataset_stats() -> list[dict]:
    with connect() as db:
        rows = db.execute(
            """
            SELECT
                accounts.username,
                accounts.patient_name,
                accounts.caregiver_name,
                COUNT(task_attempts.attempt_id) AS records,
                COALESCE(SUM(task_attempts.completed), 0) AS completed,
                COALESCE(SUM(task_attempts.missed), 0) AS missed,
                ROUND(AVG(task_attempts.adjusted_performance_score), 1) AS adjusted_average,
                MAX(task_attempts.started_at) AS latest_activity
            FROM accounts
            LEFT JOIN task_attempts ON task_attempts.user_id = accounts.username
            GROUP BY accounts.username
            ORDER BY accounts.patient_name, accounts.username
            """
        ).fetchall()
        return rows_to_dicts(rows)


def migrate_routines_table(db: sqlite3.Connection) -> None:
    columns = {
        row["name"]
        for row in db.execute("PRAGMA table_info(routines)").fetchall()
    }
    if "user_id" in columns:
        return

    db.execute("ALTER TABLE routines RENAME TO routines_old")
    db.execute(
        """
        CREATE TABLE routines (
            user_id TEXT NOT NULL,
            task_id TEXT NOT NULL,
            task_name TEXT NOT NULL,
            task_category TEXT NOT NULL,
            task_difficulty INTEGER NOT NULL,
            task_importance INTEGER NOT NULL,
            scheduled_time TEXT NOT NULL,
            time_of_day TEXT NOT NULL,
            repeat_schedule TEXT NOT NULL,
            instructions TEXT NOT NULL,
            active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            PRIMARY KEY (user_id, task_id)
        )
        """
    )
    db.execute(
        """
        INSERT INTO routines (
            user_id, task_id, task_name, task_category, task_difficulty,
            task_importance, scheduled_time, time_of_day, repeat_schedule,
            instructions, active, created_at, updated_at
        )
        SELECT
            ?, task_id, task_name, task_category, task_difficulty,
            task_importance, scheduled_time, time_of_day, repeat_schedule,
            instructions, active, created_at, updated_at
        FROM routines_old
        """,
        (DEFAULT_USER_ID,),
    )
    db.execute("DROP TABLE routines_old")
    db.commit()


def ensure_default_routines(
    user_id: str = DEFAULT_USER_ID,
    db: sqlite3.Connection | None = None,
) -> None:
    close_db = db is None
    db = db or connect()
    count = db.execute(
        "SELECT COUNT(*) FROM routines WHERE user_id = ?",
        (user_id,),
    ).fetchone()[0]
    if count == 0:
        for routine in DEFAULT_ROUTINES:
            save_routine(routine, user_id=user_id, db=db)
    db.commit()
    if close_db:
        db.close()


def migrate_default_user_data_to_single_account(db: sqlite3.Connection) -> None:
    accounts = db.execute("SELECT username FROM accounts ORDER BY created_at").fetchall()
    if len(accounts) != 1:
        return
    username = accounts[0]["username"]
    if username == DEFAULT_USER_ID:
        return

    user_routine_count = db.execute(
        "SELECT COUNT(*) FROM routines WHERE user_id = ?",
        (username,),
    ).fetchone()[0]
    if user_routine_count == 0:
        db.execute(
            "UPDATE routines SET user_id = ? WHERE user_id = ?",
            (username, DEFAULT_USER_ID),
        )

    for table in [
        "task_attempts",
        "caregiver_notes",
        "alerts",
        "summaries",
        "caregiver_chat",
    ]:
        db.execute(
            f"UPDATE {table} SET user_id = ? WHERE user_id = ?",
            (username, DEFAULT_USER_ID),
        )


def create_account(
    username: str,
    password: str,
    caregiver_password: str,
    patient_name: str,
    caregiver_name: str,
    caregiver_phone: str = "",
) -> dict:
    now = today_context()["timestamp"]
    clean_username = username.strip()
    salt = secrets.token_hex(16)
    caregiver_salt = secrets.token_hex(16)
    account = {
        "username": clean_username,
        "password_hash": password_hash(password, salt),
        "password_salt": salt,
        "caregiver_password_hash": password_hash(caregiver_password, caregiver_salt),
        "caregiver_password_salt": caregiver_salt,
        "patient_name": patient_name.strip(),
        "caregiver_name": caregiver_name.strip(),
        "caregiver_phone": caregiver_phone.strip(),
        "sms_enabled": 1 if caregiver_phone.strip() else 0,
        "created_at": now,
        "updated_at": now,
    }
    with connect() as db:
        db.execute(
            """
            INSERT INTO accounts (
                username, password_hash, password_salt,
                caregiver_password_hash, caregiver_password_salt,
                patient_name, caregiver_name, caregiver_phone, sms_enabled,
                created_at, updated_at
            )
            VALUES (
                :username, :password_hash, :password_salt,
                :caregiver_password_hash, :caregiver_password_salt,
                :patient_name, :caregiver_name, :caregiver_phone, :sms_enabled,
                :created_at, :updated_at
            )
            """,
            account,
        )
        db.commit()
    ensure_default_routines(clean_username)
    return public_account(account)


def verify_account(username: str, password: str, caregiver_password: str) -> dict | None:
    with connect() as db:
        row = db.execute(
            "SELECT * FROM accounts WHERE username = ?",
            (username.strip(),),
        ).fetchone()
    if row is None:
        return None
    expected_hash = password_hash(password, row["password_salt"])
    if not hmac.compare_digest(expected_hash, row["password_hash"]):
        return None
    expected_caregiver_hash = password_hash(
        caregiver_password,
        row["caregiver_password_salt"],
    )
    if not hmac.compare_digest(
        expected_caregiver_hash,
        row["caregiver_password_hash"],
    ):
        return None
    return public_account(row)


def verify_caregiver_password(username: str, caregiver_password: str) -> bool:
    with connect() as db:
        row = db.execute(
            "SELECT caregiver_password_hash, caregiver_password_salt FROM accounts WHERE username = ?",
            (username.strip(),),
        ).fetchone()
    if row is None:
        return False
    expected_hash = password_hash(caregiver_password, row["caregiver_password_salt"])
    return hmac.compare_digest(expected_hash, row["caregiver_password_hash"])


def get_account(username: str) -> dict | None:
    with connect() as db:
        row = db.execute(
            "SELECT * FROM accounts WHERE username = ?",
            (username.strip(),),
        ).fetchone()
        return public_account(row)


def get_account_sms_settings(username: str) -> dict | None:
    with connect() as db:
        row = db.execute(
            "SELECT caregiver_phone, sms_enabled FROM accounts WHERE username = ?",
            (username.strip(),),
        ).fetchone()
    if row is None:
        return None
    return {
        "phone": str(row["caregiver_phone"] or ""),
        "enabled": bool(row["sms_enabled"]),
    }


def update_account_phone(username: str, caregiver_phone: str) -> dict | None:
    phone = caregiver_phone.strip()
    with connect() as db:
        db.execute(
            """
            UPDATE accounts
            SET caregiver_phone = ?, sms_enabled = ?, updated_at = ?
            WHERE username = ?
            """,
            (
                phone,
                1 if phone else 0,
                today_context()["timestamp"],
                username.strip(),
            ),
        )
        db.commit()
        row = db.execute(
            "SELECT * FROM accounts WHERE username = ?",
            (username.strip(),),
        ).fetchone()
    return public_account(row)


def set_account_sms_enabled(username: str, enabled: bool) -> dict | None:
    with connect() as db:
        row = db.execute(
            "SELECT caregiver_phone FROM accounts WHERE username = ?",
            (username.strip(),),
        ).fetchone()
        if row is None:
            return None
        if enabled and not str(row["caregiver_phone"] or ""):
            raise ValueError("Add a caregiver phone number at login first.")
        db.execute(
            "UPDATE accounts SET sms_enabled = ?, updated_at = ? WHERE username = ?",
            (
                1 if enabled else 0,
                today_context()["timestamp"],
                username.strip(),
            ),
        )
        db.commit()
        account_row = db.execute(
            "SELECT * FROM accounts WHERE username = ?",
            (username.strip(),),
        ).fetchone()
    return public_account(account_row)


def save_auth_token(username: str, token: str, expires_at: str) -> None:
    context = today_context()
    with connect() as db:
        db.execute(
            """
            INSERT INTO auth_tokens (token_hash, username, created_at, expires_at)
            VALUES (?, ?, ?, ?)
            """,
            (token_hash(token), username, context["timestamp"], expires_at),
        )
        db.commit()


def account_from_auth_token(token: str) -> dict | None:
    now = runtime_config.local_now().isoformat(timespec="seconds")
    with connect() as db:
        row = db.execute(
            """
            SELECT accounts.*
            FROM auth_tokens
            JOIN accounts ON accounts.username = auth_tokens.username
            WHERE auth_tokens.token_hash = ? AND auth_tokens.expires_at > ?
            """,
            (token_hash(token), now),
        ).fetchone()
        return public_account(row)


def delete_auth_token(token: str) -> None:
    with connect() as db:
        db.execute("DELETE FROM auth_tokens WHERE token_hash = ?", (token_hash(token),))
        db.commit()


def save_routine(
    data: dict,
    user_id: str = DEFAULT_USER_ID,
    db: sqlite3.Connection | None = None,
) -> dict:
    task_name = str(data.get("task_name", "")).strip()
    task_category = str(data.get("task_category", "Routine")).strip()
    scheduled_time = str(data.get("scheduled_time", "")).strip()
    time_of_day = str(data.get("time_of_day", "Morning")).strip()
    instructions = data.get("instructions") or []
    if isinstance(instructions, str):
        instructions = [line.strip() for line in instructions.splitlines() if line.strip()]
    else:
        instructions = [str(line).strip() for line in instructions if str(line).strip()]

    if not task_name:
        raise ValueError("Enter a task name.")
    if len(task_name) > 100:
        raise ValueError("Task name must be 100 characters or fewer.")
    if not task_category:
        raise ValueError("Enter a task category.")
    try:
        datetime.strptime(scheduled_time, "%H:%M")
    except ValueError as error:
        raise ValueError("Choose a valid scheduled time.") from error
    if time_of_day not in {"Morning", "Afternoon", "Evening"}:
        raise ValueError("Choose a valid time of day.")
    if not instructions:
        raise ValueError("Add at least one instruction step.")
    if len(instructions) > 25:
        raise ValueError("Use 25 instruction steps or fewer.")
    try:
        task_difficulty = int(data.get("task_difficulty", 3))
        task_importance = int(data.get("task_importance", 3))
    except (TypeError, ValueError) as error:
        raise ValueError("Difficulty and importance must be numbers from 1 to 5.") from error
    if task_difficulty not in range(1, 6) or task_importance not in range(1, 6):
        raise ValueError("Difficulty and importance must be from 1 to 5.")

    close_db = db is None
    db = db or connect()
    now = today_context()["timestamp"]
    task_id = str(data.get("task_id") or "").strip()
    if not task_id:
        task_id = re.sub(r"[^a-z0-9]+", "-", task_name.lower()).strip("-")
    if not task_id:
        task_id = f"task-{secrets.token_hex(4)}"

    payload = {
        "user_id": user_id,
        "task_id": task_id,
        "task_name": task_name,
        "task_category": task_category,
        "task_difficulty": task_difficulty,
        "task_importance": task_importance,
        "scheduled_time": scheduled_time,
        "time_of_day": time_of_day,
        "repeat_schedule": data.get("repeat_schedule", "Daily"),
        "instructions": json.dumps(instructions),
        "active": 1 if data.get("active", True) else 0,
        "created_at": now,
        "updated_at": now,
    }
    existing = db.execute(
        "SELECT created_at FROM routines WHERE user_id = ? AND task_id = ?",
        (user_id, task_id),
    ).fetchone()
    if existing:
        payload["created_at"] = existing["created_at"]

    db.execute(
        """
        INSERT INTO routines (
            user_id, task_id, task_name, task_category, task_difficulty, task_importance,
            scheduled_time, time_of_day, repeat_schedule, instructions, active,
            created_at, updated_at
        )
        VALUES (
            :user_id, :task_id, :task_name, :task_category, :task_difficulty,
            :task_importance, :scheduled_time, :time_of_day, :repeat_schedule,
            :instructions, :active, :created_at, :updated_at
        )
        ON CONFLICT(user_id, task_id) DO UPDATE SET
            task_name = excluded.task_name,
            task_category = excluded.task_category,
            task_difficulty = excluded.task_difficulty,
            task_importance = excluded.task_importance,
            scheduled_time = excluded.scheduled_time,
            time_of_day = excluded.time_of_day,
            repeat_schedule = excluded.repeat_schedule,
            instructions = excluded.instructions,
            active = excluded.active,
            updated_at = excluded.updated_at
        """,
        payload,
    )
    db.commit()
    if close_db:
        db.close()
    return get_routine(task_id, user_id=user_id)


def list_routines(
    active_only: bool = False,
    user_id: str = DEFAULT_USER_ID,
) -> list[dict]:
    with connect() as db:
        query = "SELECT * FROM routines WHERE user_id = ?"
        params: tuple[Any, ...] = (user_id,)
        if active_only:
            query += " AND active = 1"
        query += " ORDER BY scheduled_time, task_name"
        return rows_to_dicts(db.execute(query, params).fetchall())


def get_routine(task_id: str, user_id: str = DEFAULT_USER_ID) -> dict | None:
    with connect() as db:
        row = db.execute(
            "SELECT * FROM routines WHERE user_id = ? AND task_id = ?",
            (user_id, task_id),
        ).fetchone()
        return row_to_dict(row)


def delete_routine(task_id: str, user_id: str = DEFAULT_USER_ID) -> bool:
    with connect() as db:
        cursor = db.execute(
            "DELETE FROM routines WHERE user_id = ? AND task_id = ?",
            (user_id, task_id),
        )
        db.commit()
        return cursor.rowcount > 0


def get_next_routine(user_id: str = DEFAULT_USER_ID) -> dict | None:
    context = today_context()
    with connect() as db:
        rows = db.execute(
            """
            SELECT * FROM routines
            WHERE user_id = ? AND active = 1
            ORDER BY
                CASE WHEN scheduled_time >= ? THEN 0 ELSE 1 END,
                scheduled_time
            """,
            (user_id, context["time"]),
        ).fetchall()
        for row in rows:
            routine = row_to_dict(row)
            completed = db.execute(
                """
                SELECT 1 FROM task_attempts
                WHERE user_id = ? AND date = ? AND task_id = ? AND completed = 1
                LIMIT 1
                """,
                (user_id, context["date"], routine["task_id"]),
            ).fetchone()
            if not completed:
                return routine
    return None


def create_attempt(routine: dict, user_id: str = DEFAULT_USER_ID) -> int:
    context = today_context()
    with connect() as db:
        cursor = db.execute(
            """
            INSERT INTO task_attempts (
                user_id, date, day_of_week, time_of_day, scheduled_time,
                task_id, task_name, task_category, task_difficulty,
                task_importance, started_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                context["date"],
                context["day_of_week"],
                routine["time_of_day"],
                routine["scheduled_time"],
                routine["task_id"],
                routine["task_name"],
                routine["task_category"],
                routine["task_difficulty"],
                routine["task_importance"],
                context["timestamp"],
            ),
        )
        db.commit()
        return int(cursor.lastrowid)


def get_attempt(attempt_id: int) -> dict | None:
    with connect() as db:
        row = db.execute(
            "SELECT * FROM task_attempts WHERE attempt_id = ?",
            (attempt_id,),
        ).fetchone()
        return row_to_dict(row)


def update_attempt(attempt_id: int, **fields: Any) -> dict:
    if not fields:
        return get_attempt(attempt_id)
    assignments = ", ".join(f"{key} = ?" for key in fields)
    values = list(fields.values()) + [attempt_id]
    with connect() as db:
        db.execute(
            f"UPDATE task_attempts SET {assignments} WHERE attempt_id = ?",
            values,
        )
        db.commit()
    return get_attempt(attempt_id)


def list_attempts(
    limit: int = 500,
    user_id: str = DEFAULT_USER_ID,
) -> list[dict]:
    with connect() as db:
        return rows_to_dicts(
            db.execute(
                """
                SELECT * FROM task_attempts
                WHERE user_id = ?
                ORDER BY started_at DESC
                LIMIT ?
                """,
                (user_id, limit),
            ).fetchall()
        )


def list_today_attempts(user_id: str = DEFAULT_USER_ID) -> list[dict]:
    context = today_context()
    with connect() as db:
        return rows_to_dicts(
            db.execute(
                """
                SELECT * FROM task_attempts
                WHERE user_id = ? AND date = ?
                ORDER BY scheduled_time, started_at
                """,
                (user_id, context["date"]),
            ).fetchall()
        )


EXCEL_DATASET_HEADERS = [
    "user_id",
    "date",
    "day_of_week",
    "time_of_day",
    "scheduled_time",
    "task_name",
    "task_category",
    "task_importance",
    "patient_marked_complete",
    "reminders_needed",
    "help_requested",
    "visual_support_used",
    "confusion_flag",
    "time_to_complete_min",
    "performance_score",
    "task_status",
    "caregiver_alert_sent",
    "alert_reason",
    "recommended_action",
    "notes",
    "task_difficulty",
    "difficulty_score",
    "struggle_flag",
    "struggle_evidence",
    "completion_source",
    "caregiver_verified",
    "device_verified",
    "verified_completion_status",
    "completion_confidence_pct",
    "analysis_note",
    "difficulty_adjusted_score",
    "support_need_score",
    "support_need_level",
]


def yes_no(value: Any) -> str:
    return "Yes" if bool(value) else "No"


def importance_label(value: Any) -> str:
    importance = int(value or 0)
    if importance >= 5:
        return "Critical"
    if importance == 4:
        return "High"
    if importance == 3:
        return "Medium"
    return "Low"


def difficulty_label(value: Any) -> str:
    difficulty = int(value or 3)
    if difficulty <= 2:
        return "Easy"
    if difficulty == 3:
        return "Medium"
    return "Hard"


def difficulty_score(value: Any) -> int:
    difficulty = int(value or 3)
    if difficulty <= 2:
        return 1
    if difficulty == 3:
        return 2
    return 3


def completion_confidence(attempt: dict) -> int:
    if attempt.get("completed"):
        confidence = 65
        if int(attempt.get("reminders_needed") or 0) == 0:
            confidence += 10
        if not attempt.get("help_requested") and not attempt.get("confusion_flag"):
            confidence += 10
        return min(confidence, 85)
    if attempt.get("missed"):
        return 90
    return 45


def struggle_evidence(attempt: dict) -> str:
    evidence = []
    reminders = int(attempt.get("reminders_needed") or 0)
    if attempt.get("missed"):
        evidence.append("task missed")
    if reminders >= 3:
        evidence.append("multiple reminders")
    elif reminders > 0:
        evidence.append("reminder used")
    if attempt.get("help_requested"):
        evidence.append("help requested")
    if attempt.get("confusion_flag"):
        evidence.append("possible confusion")
    if float(attempt.get("adjusted_performance_score") or 0) < 60:
        evidence.append("low adjusted score")
    return "; ".join(evidence) if evidence else "no major struggle signal"


def support_need_score(attempt: dict) -> int:
    score = 100 - float(attempt.get("adjusted_performance_score") or 0)
    score += min(int(attempt.get("reminders_needed") or 0), 5) * 5
    if attempt.get("help_requested"):
        score += 18
    if attempt.get("confusion_flag"):
        score += 15
    if attempt.get("caregiver_alert"):
        score += 10
    return int(max(0, min(100, round(score))))


def support_need_level(score: int) -> str:
    if score >= 70:
        return "High"
    if score >= 40:
        return "Moderate"
    return "Low"


def alert_reason_for_attempt(attempt: dict) -> str:
    if not attempt.get("caregiver_alert"):
        return ""
    return struggle_evidence(attempt)


def recommended_action_for_attempt(attempt: dict) -> str:
    if attempt.get("missed") and int(attempt.get("task_importance") or 0) >= 4:
        return "Caregiver review recommended for this important missed task."
    if attempt.get("help_requested"):
        return "Caregiver support may be needed for this routine."
    if attempt.get("confusion_flag"):
        return "Use one-step instructions and review with caregiver."
    if int(attempt.get("reminders_needed") or 0) >= 3:
        return "Add extra reminders or simplify this routine."
    if float(attempt.get("adjusted_performance_score") or 0) < 60:
        return "Review timing and task difficulty."
    return "Continue current routine."


def task_status_for_attempt(attempt: dict) -> str:
    if attempt.get("completed"):
        return "Marked complete"
    if attempt.get("missed"):
        return "Missed"
    return "Started"


def excel_dataset_row(attempt: dict) -> dict:
    support_score = support_need_score(attempt)
    completed = bool(attempt.get("completed"))
    missed = bool(attempt.get("missed"))
    confidence = completion_confidence(attempt)
    if completed:
        verified_status = "Patient marked complete - unverified"
    elif missed:
        verified_status = "Not marked complete"
    else:
        verified_status = "In progress / not verified"
    struggle = (
        missed
        or int(attempt.get("reminders_needed") or 0) >= 3
        or bool(attempt.get("help_requested"))
        or bool(attempt.get("confusion_flag"))
        or float(attempt.get("adjusted_performance_score") or 0) < 60
    )
    return {
        "user_id": attempt.get("user_id", ""),
        "date": attempt.get("date", ""),
        "day_of_week": attempt.get("day_of_week", ""),
        "time_of_day": attempt.get("time_of_day", ""),
        "scheduled_time": attempt.get("scheduled_time", ""),
        "task_name": attempt.get("task_name", ""),
        "task_category": attempt.get("task_category", ""),
        "task_importance": importance_label(attempt.get("task_importance")),
        "patient_marked_complete": yes_no(completed),
        "reminders_needed": int(attempt.get("reminders_needed") or 0),
        "help_requested": yes_no(attempt.get("help_requested")),
        "visual_support_used": "No",
        "confusion_flag": yes_no(attempt.get("confusion_flag")),
        "time_to_complete_min": round((attempt.get("time_to_complete") or 0) / 60, 1)
        if attempt.get("time_to_complete") is not None
        else "",
        "performance_score": attempt.get("raw_performance_score", 0),
        "task_status": task_status_for_attempt(attempt),
        "caregiver_alert_sent": yes_no(attempt.get("caregiver_alert")),
        "alert_reason": alert_reason_for_attempt(attempt),
        "recommended_action": recommended_action_for_attempt(attempt),
        "notes": attempt.get("notes", ""),
        "task_difficulty": difficulty_label(attempt.get("task_difficulty")),
        "difficulty_score": difficulty_score(attempt.get("task_difficulty")),
        "struggle_flag": yes_no(struggle),
        "struggle_evidence": struggle_evidence(attempt),
        "completion_source": "Patient button" if completed else "No completion marker",
        "caregiver_verified": "No",
        "device_verified": "No",
        "verified_completion_status": verified_status,
        "completion_confidence_pct": confidence,
        "analysis_note": "Use patient_marked_complete carefully; it is not external verification.",
        "difficulty_adjusted_score": attempt.get("adjusted_performance_score", 0),
        "support_need_score": support_score,
        "support_need_level": support_need_level(support_score),
    }


def excel_dataset_rows(
    limit: int = 500,
    user_id: str = DEFAULT_USER_ID,
) -> list[dict]:
    return [
        excel_dataset_row(attempt)
        for attempt in list_attempts(limit=limit, user_id=user_id)
    ]


def save_alert(alert: dict, user_id: str = DEFAULT_USER_ID) -> dict:
    context = today_context()
    with connect() as db:
        cursor = db.execute(
            """
            INSERT INTO alerts (
                user_id, date, severity, reason, task_id, task_name,
                patient_message, text_status, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                context["date"],
                alert["severity"],
                alert["reason"],
                alert.get("task_id"),
                alert.get("task_name"),
                alert.get("patient_message", ""),
                alert.get("text_status", ""),
                context["timestamp"],
            ),
        )
        db.commit()
        alert["alert_id"] = int(cursor.lastrowid)
        alert["date"] = context["date"]
        alert["created_at"] = context["timestamp"]
        return alert


def list_alerts(limit: int = 50, user_id: str = DEFAULT_USER_ID) -> list[dict]:
    with connect() as db:
        return rows_to_dicts(
            db.execute(
                """
                SELECT * FROM alerts
                WHERE user_id = ?
                ORDER BY created_at DESC, alert_id DESC
                LIMIT ?
                """,
                (user_id, limit),
            ).fetchall()
        )


def update_alert_text_status(alert_id: int, text_status: str) -> None:
    with connect() as db:
        db.execute(
            "UPDATE alerts SET text_status = ? WHERE alert_id = ?",
            (text_status, alert_id),
        )
        db.commit()


def add_caregiver_chat(role: str, message: str, user_id: str = DEFAULT_USER_ID) -> None:
    with connect() as db:
        db.execute(
            """
            INSERT INTO caregiver_chat (user_id, role, message, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, role, message, today_context()["timestamp"]),
        )
        db.commit()


def list_caregiver_chat(
    limit: int = 40,
    user_id: str = DEFAULT_USER_ID,
) -> list[dict]:
    with connect() as db:
        rows = db.execute(
            """
            SELECT * FROM caregiver_chat
            WHERE user_id = ?
            ORDER BY created_at DESC, message_id DESC
            LIMIT ?
            """,
            (user_id, limit),
        ).fetchall()
        return list(reversed(rows_to_dicts(rows)))


def add_patient_caregiver_message(
    sender: str,
    message: str,
    user_id: str = DEFAULT_USER_ID,
) -> dict:
    with connect() as db:
        cursor = db.execute(
            """
            INSERT INTO patient_caregiver_messages (user_id, sender, message, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, sender, message, today_context()["timestamp"]),
        )
        db.commit()
        row = db.execute(
            "SELECT * FROM patient_caregiver_messages WHERE message_id = ?",
            (cursor.lastrowid,),
        ).fetchone()
        return row_to_dict(row)


def list_patient_caregiver_messages(
    limit: int = 80,
    user_id: str = DEFAULT_USER_ID,
) -> list[dict]:
    with connect() as db:
        rows = db.execute(
            """
            SELECT * FROM patient_caregiver_messages
            WHERE user_id = ?
            ORDER BY created_at DESC, message_id DESC
            LIMIT ?
            """,
            (user_id, limit),
        ).fetchall()
        return list(reversed(rows_to_dicts(rows)))


def clear_caregiver_messages_and_alerts(user_id: str = DEFAULT_USER_ID) -> None:
    with connect() as db:
        db.execute("DELETE FROM caregiver_chat WHERE user_id = ?", (user_id,))
        db.execute(
            "DELETE FROM patient_caregiver_messages WHERE user_id = ?",
            (user_id,),
        )
        db.execute("DELETE FROM alerts WHERE user_id = ?", (user_id,))
        db.commit()


def save_summary(summary: str, user_id: str = DEFAULT_USER_ID) -> None:
    context = today_context()
    with connect() as db:
        db.execute(
            """
            INSERT INTO summaries (user_id, date, summary, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, context["date"], summary, context["timestamp"]),
        )
        db.commit()


def clear_patient_dataset(user_id: str = DEFAULT_USER_ID) -> None:
    context = today_context()
    with connect() as db:
        db.execute("DELETE FROM task_attempts WHERE user_id = ?", (user_id,))
        db.execute("DELETE FROM caregiver_notes WHERE user_id = ?", (user_id,))
        db.execute("DELETE FROM alerts WHERE user_id = ?", (user_id,))
        db.execute("DELETE FROM summaries WHERE user_id = ?", (user_id,))
        db.execute("DELETE FROM caregiver_chat WHERE user_id = ?", (user_id,))
        db.execute("DELETE FROM patient_caregiver_messages WHERE user_id = ?", (user_id,))
        db.execute(
            """
            INSERT INTO app_settings (key, value, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET
                value = excluded.value,
                updated_at = excluded.updated_at
            """,
            (
                f"dataset_cleared_at:{user_id}",
                context["timestamp"],
                context["timestamp"],
            ),
        )
        db.commit()

    with connect() as db:
        db.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        db.execute("VACUUM")

    for export_path in BASE_DIR.glob("aura*_task_attempts.csv"):
        export_path.unlink(missing_ok=True)


def was_dataset_cleared_after_schedule(
    user_id: str,
    date: str,
    scheduled_time: str,
) -> bool:
    cleared_at = get_setting(f"dataset_cleared_at:{user_id}", "")
    if not cleared_at:
        return False
    try:
        cleared_context = datetime.fromisoformat(cleared_at)
    except ValueError:
        return False
    return (
        cleared_context.strftime("%Y-%m-%d") == date
        and scheduled_time <= cleared_context.strftime("%H:%M")
    )


def dataset_summary(user_id: str = DEFAULT_USER_ID) -> dict:
    with connect() as db:
        row = db.execute(
            """
            SELECT
                COUNT(*) AS total,
                COALESCE(SUM(completed), 0) AS completed,
                COALESCE(SUM(missed), 0) AS missed,
                COALESCE(SUM(help_requested), 0) AS help_requests,
                COALESCE(SUM(confusion_flag), 0) AS confusion_flags,
                ROUND(AVG(raw_performance_score), 1) AS raw_average,
                ROUND(AVG(adjusted_performance_score), 1) AS adjusted_average
            FROM task_attempts
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()
        return row_to_dict(row) or {}


def export_attempts_csv(
    path: Path = EXPORT_PATH,
    user_id: str = DEFAULT_USER_ID,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as file:
        write_attempts_csv(file, user_id)
    return path


def write_attempts_csv(file, user_id: str = DEFAULT_USER_ID) -> None:
    attempts = excel_dataset_rows(limit=100000, user_id=user_id)
    headers = EXCEL_DATASET_HEADERS
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    for attempt in attempts:
        row = {header: attempt.get(header, "") for header in headers}
        # Keep spreadsheet apps from converting narrow ISO date/time cells to #####.
        for field in ("date", "scheduled_time"):
            if row[field]:
                row[field] = f"\u200e{row[field]}"
        writer.writerow(row)


def export_attempts_csv_bytes(user_id: str = DEFAULT_USER_ID) -> bytes:
    output = io.StringIO(newline="")
    write_attempts_csv(output, user_id)
    return output.getvalue().encode("utf-8-sig")

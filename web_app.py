from __future__ import annotations

import base64
import json
import mimetypes
import os
import posixpath
import re
import secrets
from datetime import datetime, timedelta
from http import cookies
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Event, Lock, Thread
from urllib.parse import parse_qs, unquote, urlencode, urlparse
from urllib.request import Request, urlopen

from dotenv import load_dotenv

import database
import insights
from language_utils import (
    get_supported_languages,
    localize_patient_text,
    localize_text,
    normalize_language_code,
)
import test_clock
from main import AURA_CAREGIVER_MODEL, AURA_PATIENT_MODEL, client
from scoring import score_attempt


HOST = "127.0.0.1"
PORT = 8000
STATIC_DIR = Path(__file__).with_name("static")
USER_ID = database.DEFAULT_USER_ID
AUTH_COOKIE_MAX_AGE = 60 * 60 * 24 * 30
load_dotenv(Path(__file__).with_name(".env.admin"), override=False)
ADMIN_USERNAME = os.getenv("AURA_ADMIN_USERNAME", "").strip()
ADMIN_PASSWORD = os.getenv("AURA_ADMIN_PASSWORD", "")
try:
    TASK_GRACE_PERIOD_MINUTES = max(
        0,
        int(os.getenv("AURA_TASK_GRACE_PERIOD_MINUTES", "30")),
    )
except ValueError:
    TASK_GRACE_PERIOD_MINUTES = 30
MISSED_TASK_MONITOR_SECONDS = 2

session_lock = Lock()
overdue_lock = Lock()
sessions: dict[str, dict] = {}


CAREGIVER_CHAT_PROMPT = """
You are AURA's caregiver assistant.

You can answer general caregiver questions helpfully.
If the caregiver asks an unrelated everyday question, answer like a normal helpful AI assistant.
For patient-specific performance, routines, alerts, trends, or summaries, use only the stored patient records provided.
Never guess or invent patient data.
Use careful wording:
- "The data suggests..."
- "The current records indicate..."
- "Caregiver review is recommended..."

Never diagnose dementia, confusion, or any medical condition.
For medical questions, provide careful, general health information only when it is grounded in trusted medical sources from the medical_source_context.
Do not diagnose, prescribe treatment, change medication instructions, or claim certainty.
For urgent symptoms or possible emergencies, recommend contacting emergency services immediately.
Never change medication instructions.
Never replace caregivers, doctors, or emergency services.
If the caregiver asks a patient-specific question and the records do not answer it, say that.
If the caregiver asks a general non-medical question, answer normally and briefly.

Respond in the same language as the caregiver's question unless they request another language.
"""

CAREGIVER_MEDICAL_SEARCH_PROMPT = """
You are AURA's caregiver medical information lookup assistant.

Use web search only for trusted medical sources:
- U.S. government or public health sites such as CDC, NIH, NIA, MedlinePlus, FDA, CMS, or state/local health departments.
- Major academic medical centers or nationally recognized nonprofit medical organizations when government sources are insufficient.

Give general medical information and care-seeking guidance for a caregiver.
Never diagnose the patient.
Never prescribe, stop, start, or change medication.
Never replace a clinician, pharmacist, emergency dispatcher, or emergency services.
For emergency symptoms, clearly say to call emergency services now.
Mention the source organizations used.
Respond in the caregiver's language unless they request another language.
"""

PATIENT_AGENT_PROMPT = """
You are AURA, a warm general-purpose AI assistant inside a daily routine app.

First decide whether the patient's message is a health or safety concern.
Never diagnose, never give medical advice, and never change medication instructions.

Priority order:
1. If there is no current_task and no due_task, act like a normal helpful AI assistant.
2. If the patient asks an everyday unrelated question, answer it directly and helpfully.
3. If there is an active task, answer briefly, then add one short sentence with the current step.
4. If there is a due_task, answer briefly, then add one short sentence that gently prioritizes that task now.
5. If the patient asks what to do now, focus on the active or due task.

Patient style:
- Use clear, friendly language.
- Use simple words when giving routine instructions.
- Be calm and supportive.
- Keep every patient-facing answer to one or two concise sentences.
- Keep the complete answer under 40 words when possible.
- Give only one routine instruction at a time.
- Do not mention dementia.
- Do not use markdown.

Free chat mode:
- When current_task and due_task are both null, do not focus on routines.
- Answer naturally like a general-purpose chatbot.
- Use the recent conversation when it is relevant.
- Give a useful answer in one or two short sentences.
- You can answer everyday questions, planning questions, simple explanations, hobbies, food, clothes, weather planning, and friendly conversation.
- Still keep medical safety limits.

Special answers:
- If the patient asks who you are, say: "I am AURA. I help you with your day."
- If the patient says they are confused, say: "That's okay. I will help you one step at a time."

If a current task or due task exists, keep task reminders short and gentle.
Respond in the requested language code unless the patient asks for another language.

Return only valid JSON with this shape:
{
  "priority": "emergency | caregiver_review | task | chat",
  "answer": "patient-facing answer",
  "reason": "short caregiver-facing safety reason, or an empty string"
}

Priority rules:
- emergency: possible immediate danger, severe symptom, serious injury, self-harm, poisoning, overdose, fall with injury, chest or heart symptoms, breathing trouble, stroke signs, seizure, heavy bleeding, fainting, or similar urgent risk.
- caregiver_review: any non-urgent or unclear symptom, pain, injury, medication concern, or medical question.
- task: a current or overdue task needs to be prioritized and there is no health or safety concern.
- chat: no health concern and no current or overdue task.
- If uncertain between emergency and caregiver_review, choose emergency.
- For emergency, use one or two short sentences. Say that the caregiver was alerted, tell the patient to call 911 now, and give at most one situation-appropriate immediate action.
- For caregiver_review, use one or two short sentences. Say that the caregiver was alerted and give at most one situation-appropriate safe next step.
- Do not automatically say "stay where you are." Say that only when moving could clearly create more danger, such as after a serious fall or while very dizzy.
- For an unusual environmental danger, do not invent rescue techniques. Tell the patient to call 911 and follow the dispatcher's instructions.
- Never give a diagnosis, medication advice, or detailed treatment instructions.
"""

PATIENT_SAFETY_RESPONSE_PROMPT = """
You write AURA's immediate patient-facing safety response after the caregiver alert has already been saved.

Rules:
- Write only one or two short sentences.
- Keep the complete response under 30 words.
- Use simple, calm words and no markdown.
- Briefly refer to the patient's actual situation so the response does not sound generic.
- Clearly say that AURA alerted the caregiver.
- For an Emergency, clearly tell the patient to call 911 now and follow the dispatcher's instructions.
- Do not tell the patient how to move, escape, perform first aid, or treat the problem.
- Do not diagnose or recommend medicine.
- Do not say "stay where you are."
- Respond in the requested language.

Return only the patient-facing response.
"""

MODEL_FALLBACKS = {
    "caregiver": [
        "gpt-5-mini",
        "gpt-5",
        "gpt-4.1",
        "gpt-4o",
        "gpt-4o-mini",
    ],
    "patient": [
        "gpt-5-mini",
        "gpt-5",
        "gpt-4.1-mini",
        "gpt-4o-mini",
        "gpt-4o",
    ],
}


def ordered_model_choices(primary_model: str, role: str) -> list[str]:
    choices = [primary_model]
    env_choices = os.getenv(f"AURA_{role.upper()}_MODEL_FALLBACKS", "")
    if env_choices:
        choices.extend(model.strip() for model in env_choices.split(","))
    choices.extend(MODEL_FALLBACKS.get(role, []))

    deduped = []
    for model in choices:
        if model and model not in deduped:
            deduped.append(model)
    return deduped


def should_try_next_model(error: Exception) -> bool:
    text = str(error).lower()
    model_error_terms = [
        "model",
        "does not exist",
        "not found",
        "unsupported",
        "invalid",
        "permission",
        "access",
    ]
    network_error_terms = [
        "timed out",
        "timeout",
        "connection",
        "network",
        "socket",
        "api.openai.com",
    ]
    if any(term in text for term in network_error_terms):
        return False
    return any(term in text for term in model_error_terms)


def create_ai_response(role: str, primary_model: str, **request):
    last_error = None
    for model in ordered_model_choices(primary_model, role):
        try:
            return client.responses.create(**{**request, "model": model})
        except Exception as error:
            last_error = error
            if not should_try_next_model(error):
                break
    if last_error is not None:
        raise last_error
    raise RuntimeError("No AI model is configured.")


def ai_service_error_message(error: Exception, audience: str = "patient") -> str:
    error_text = str(error).lower()
    if "insufficient_quota" in error_text or "exceeded your current quota" in error_text:
        if audience == "caregiver":
            return (
                "AURA cannot reach OpenAI because the API account has no available quota. "
                "Add API billing or credits, then try again."
            )
        return (
            "AURA chat is temporarily unavailable. "
            "Please ask your caregiver to check the AI service."
        )
    if any(
        term in error_text
        for term in ("connection error", "getaddrinfo", "dns", "timed out", "timeout")
    ):
        if audience == "caregiver":
            return (
                "AURA could not connect to OpenAI after several attempts. "
                "Check the internet connection and try again."
            )
        return "I could not connect right now. Please try again in a moment."
    return "AURA cannot reach the AI service right now. Please try again."


def get_cookie_session(cookie_header: str | None) -> str:
    jar = cookies.SimpleCookie()
    if cookie_header:
        jar.load(cookie_header)
    session_id = jar.get("aura_session")
    if session_id is not None and session_id.value:
        return session_id.value
    return secrets.token_urlsafe(24)


def get_cookie_value(cookie_header: str | None, name: str) -> str | None:
    jar = cookies.SimpleCookie()
    if cookie_header:
        jar.load(cookie_header)
    value = jar.get(name)
    if value is None or not value.value:
        return None
    return value.value


def get_session_state(session_id: str) -> dict:
    if session_id not in sessions:
        sessions[session_id] = {
            "caregiver_authenticated": False,
            "dataset_authenticated": False,
            "admin_authenticated": False,
            "current_task": None,
            "patient_chat_history": [],
            "active_role": "patient",
        }
    return sessions[session_id]


def set_authenticated_session(session: dict, account: dict) -> None:
    session["authenticated"] = True
    session["account"] = account


def clear_authenticated_session(session: dict) -> None:
    session["authenticated"] = False
    session["account"] = None
    session["caregiver_authenticated"] = False
    session["dataset_authenticated"] = False
    session["admin_authenticated"] = False
    session["current_task"] = None
    session["patient_chat_history"] = []
    session["active_role"] = "patient"


def session_user_id(session: dict) -> str:
    account = session.get("account") or {}
    return str(account.get("username") or USER_ID)


def clear_patient_session_state(user_id: str) -> None:
    for state in sessions.values():
        if session_user_id(state) == user_id:
            state["current_task"] = None


def account_from_request(cookie_header: str | None, session: dict) -> dict | None:
    if session.get("authenticated") and session.get("account"):
        return session["account"]

    auth_token = get_cookie_value(cookie_header, "aura_auth")
    if not auth_token:
        return None

    account = database.account_from_auth_token(auth_token)
    if account is None:
        return None

    set_authenticated_session(session, account)
    return account


def create_auth_cookie(account: dict) -> str:
    token = secrets.token_urlsafe(32)
    expires_at = (datetime.now().astimezone() + timedelta(seconds=AUTH_COOKIE_MAX_AGE))
    database.save_auth_token(
        account["username"],
        token,
        expires_at.isoformat(timespec="seconds"),
    )
    return (
        f"aura_auth={token}; Path=/; Max-Age={AUTH_COOKIE_MAX_AGE}; "
        "SameSite=Lax; HttpOnly"
    )


def clear_auth_cookie(cookie_header: str | None) -> str:
    auth_token = get_cookie_value(cookie_header, "aura_auth")
    if auth_token:
        database.delete_auth_token(auth_token)
    return "aura_auth=; Path=/; Max-Age=0; SameSite=Lax; HttpOnly"


def route_path(raw_path: str) -> str:
    path = raw_path.split("?", 1)[0]
    if path != "/":
        path = path.rstrip("/")
    return path


def resolve_static_path(raw_path: str) -> Path | None:
    path = unquote(raw_path.split("?", 1)[0])
    if path == "/":
        path = "/index.html"

    normalized = posixpath.normpath(path.lstrip("/"))
    file_path = (STATIC_DIR / normalized).resolve()

    try:
        file_path.relative_to(STATIC_DIR.resolve())
    except ValueError:
        return None

    if not file_path.is_file():
        return None

    return file_path


def current_timestamp() -> str:
    return test_clock.now().isoformat(timespec="seconds")


def seconds_since(iso_timestamp: str | None) -> int | None:
    if not iso_timestamp:
        return None
    try:
        start = datetime.fromisoformat(iso_timestamp)
    except ValueError:
        return None
    return max(0, int((test_clock.now() - start).total_seconds()))


def patient_flags(message: str) -> dict:
    lower = message.lower()
    return {
        "help_requested": int("help" in lower),
        "confusion_flag": int(
            any(
                phrase in lower
                for phrase in [
                    "confused",
                    "i'm confused",
                    "im confused",
                    "lost",
                    "don't know",
                    "do not know",
                    "what do i do",
                ]
            )
        ),
    }


def emergency_alert_from_message(message: str, task: dict | None = None) -> dict | None:
    lower = message.lower()
    normalized = re.sub(r"\s+", " ", lower.replace("alot", "a lot")).strip()
    emergency_phrases = [
        "emergency",
        "urgent",
        "call 911",
        "911",
        "ambulance",
        "hospital now",
        "i am dying",
        "i'm dying",
        "im dying",
        "dying",
        "going to die",
        "about to die",
        "feel like i am dying",
        "feel like i'm dying",
        "fell",
        "fallen",
        "fall",
        "falling",
        "fell down",
        "fell over",
        "hurt really bad",
        "hurts really bad",
        "bad pain",
        "worst pain",
        "can't breathe",
        "cant breathe",
        "cannot breathe",
        "not breathing",
        "trouble breathing",
        "hard to breathe",
        "short of breath",
        "chest pain",
        "chest hurts",
        "chest ache",
        "chest aching",
        "chest is aching",
        "my chest is aching",
        "heart pain",
        "heart hurts",
        "heart ache",
        "heart aching",
        "heart is aching",
        "my heart is aching",
        "heart feels weird",
        "heart feels wrong",
        "pressure in my chest",
        "tight chest",
        "chest tightness",
        "bleeding",
        "bleed",
        "blood",
        "a lot of blood",
        "fire",
        "stroke",
        "face drooping",
        "slurred speech",
        "can't move my arm",
        "cant move my arm",
        "weak on one side",
        "heart attack",
        "passed out",
        "pass out",
        "fainted",
        "unconscious",
        "severe pain",
        "really bad pain",
        "very bad pain",
        "overdose",
        "took too much",
        "poison",
        "choking",
        "can't swallow",
        "cant swallow",
        "allergic reaction",
        "throat is closing",
        "seizure",
        "suicide",
        "kill myself",
        "want to die",
        "end my life",
    ]
    emergency_patterns = [
        r"\bi\s+(am|'m|m)\s+dying\b",
        r"\bi\s+(feel|think)\s+like\s+i\s+(am|'m|m)\s+dying\b",
        r"\bi\s+(fell|fallen|fainted)\b",
        r"\bi\s+(am|m|'m)?\s*(hurt|injured)\b",
        r"\bi\s+can'?t\s+get\s+up\b",
        r"\bi\s+cannot\s+get\s+up\b",
        r"\b(can'?t|cannot)\s+breathe\b",
        r"\b(chest|heart)\s+(pain|hurts|pressure)\b",
        r"\b(my\s+)?(chest|heart)\s+(is\s+|feels\s+)?(aching|hurting|painful|tight|heavy|squeezing)\b",
        r"\b(chest|heart)\s+(ache|aching|hurt|hurts|pain|pressure|tightness|squeezing)\b",
        r"\b(ache|aching|hurt|hurts|pain|pressure|tightness|squeezing)\s+(in\s+)?(my\s+)?(chest|heart)\b",
    ]
    if not any(phrase in normalized for phrase in emergency_phrases) and not any(
        re.search(pattern, normalized) for pattern in emergency_patterns
    ):
        return None
    return {
        "severity": "Emergency",
        "reason": "Patient message may indicate a serious safety risk. Contact the caregiver immediately and call emergency services if there may be danger.",
        "task_id": task.get("task_id") if task else None,
        "task_name": task.get("task_name") if task else None,
        "patient_message": message,
    }


def local_medical_safety_assessment(message: str) -> dict | None:
    normalized = re.sub(
        r"\s+",
        " ",
        message.lower().replace("alot", "a lot"),
    ).strip()
    urgent_patterns = [
        r"\b(chest|heart)\b.*\b(ache|aching|hurt|hurts|pain|pressure|tight|tightness|heavy|squeezing|weird|wrong)\b",
        r"\b(ache|aching|hurt|hurts|pain|pressure|tight|tightness|heavy|squeezing)\b.*\b(chest|heart)\b",
        r"\b(can'?t|cannot|hard to|trouble)\s+breathe\b",
        r"\b(short of breath|not breathing)\b",
        r"\b(stroke|heart attack|seizure|unconscious|passed out|fainted|overdose|poison|choking)\b",
        r"\b(fell|fallen|fall|bleeding|blood|severe pain|worst pain|really bad pain|very bad pain)\b",
        r"\b(i am dying|i'm dying|im dying|dying|going to die|want to die|kill myself|suicide|end my life)\b",
        r"\b(face droop|slurred speech|weak on one side|can't move|cant move)\b",
    ]
    if any(re.search(pattern, normalized) for pattern in urgent_patterns):
        return {
            "level": "emergency",
            "reason": "Patient described symptoms or safety language that may require urgent help.",
        }

    body_terms = [
        "head",
        "eye",
        "ear",
        "mouth",
        "throat",
        "neck",
        "shoulder",
        "arm",
        "hand",
        "finger",
        "back",
        "stomach",
        "belly",
        "abdomen",
        "leg",
        "knee",
        "foot",
        "toe",
        "skin",
        "heart",
        "chest",
        "brain",
    ]
    symptom_terms = [
        "ache",
        "aching",
        "hurt",
        "hurts",
        "pain",
        "sore",
        "sick",
        "dizzy",
        "nauseous",
        "vomit",
        "throw up",
        "diarrhea",
        "fever",
        "cough",
        "rash",
        "swollen",
        "bleed",
        "cut",
        "burn",
        "infection",
        "medicine",
        "medication",
        "pill",
        "dose",
        "allergic",
        "confused",
        "dehydrated",
        "weak",
        "numb",
    ]
    has_body = any(re.search(rf"\b{re.escape(term)}\b", normalized) for term in body_terms)
    has_symptom = any(re.search(rf"\b{re.escape(term)}\b", normalized) for term in symptom_terms)
    first_person_health = bool(
        re.search(r"\b(my|i|i'm|im|me)\b", normalized)
        and (has_body or has_symptom)
    )
    if first_person_health or (has_body and has_symptom):
        return {
            "level": "caregiver_review",
            "reason": "Patient described a health symptom or medical concern.",
        }
    return None


def extract_json_object(text: str) -> dict | None:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if not match:
            return None
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return None


def ai_safety_assessment(message: str, task: dict | None = None) -> dict:
    prompt = {
        "patient_message": message,
        "current_task": task.get("task_name") if task else None,
        "context": (
            "AURA is used by an elderly patient. Classify the patient message before any routine guidance. "
            "Any medical problem, health symptom, injury, pain, body problem, medication concern, or question about what is happening to the patient's body must not be treated as routine conversation. "
            "If the message could indicate a medical emergency, serious injury, severe symptom, immediate danger, "
            "self-harm risk, poisoning, overdose, fall injury, chest/heart pain or aching, breathing trouble, stroke signs, "
            "seizure, heavy bleeding, unconsciousness, or the patient says they may die, classify as emergency. "
            "If the message is a minor, non-urgent, or unclear medical concern, symptom, pain, medication concern, or health question, "
            "classify as caregiver_review. If uncertain between emergency and not emergency, choose emergency. "
            "Only choose none for ordinary conversation or routine/task messages without any health, body, injury, medication, or safety concern."
        ),
        "required_json": {
            "level": "emergency | caregiver_review | none",
            "reason": "short caregiver-facing reason",
        },
    }
    try:
        response = create_ai_response(
            "caregiver",
            AURA_CAREGIVER_MODEL,
            instructions=(
                "You are a conservative safety classifier for an elderly patient assistant. "
                "Return only valid JSON. Do not give patient instructions. "
                "Any patient health symptom, pain, injury, medication concern, or medical question must be classified as emergency or caregiver_review, never none. "
                "Use emergency for possible serious or urgent medical/safety risk, including chest/heart symptoms, breathing problems, severe pain, falls, bleeding, stroke signs, fainting, overdose, seizure, poisoning, self-harm, or danger. "
                "Use caregiver_review for minor or unclear medical concerns, mild symptoms, medication questions, or any non-urgent health concern. "
                "Use level none only when there is no health, safety, injury, or emergency concern."
            ),
            input=json.dumps(prompt, indent=2),
        )
    except Exception as error:
        return {
            "level": "classifier_unavailable",
            "reason": f"Safety classifier unavailable: {error}",
        }

    parsed = extract_json_object(response.output_text)
    if not parsed:
        return {
            "level": "classifier_unavailable",
            "reason": "Safety classifier returned an unreadable response.",
        }

    level = str(parsed.get("level", "none")).strip().lower()
    if level not in {"emergency", "caregiver_review", "none"}:
        level = "emergency"
    reason = str(parsed.get("reason", "")).strip()
    return {
        "level": level,
        "reason": reason or "Patient message may indicate a health or safety concern.",
    }


def safety_alert_from_message(message: str, task: dict | None = None) -> dict | None:
    local_assessment = local_medical_safety_assessment(message)
    assessment = ai_safety_assessment(message, task)
    level = assessment.get("level")
    if level == "none" and local_assessment is not None:
        assessment = local_assessment
        level = assessment.get("level")
    if level == "none":
        return None

    if level == "classifier_unavailable":
        if local_assessment is not None:
            assessment = local_assessment
            level = assessment.get("level")
        else:
            fallback = emergency_alert_from_message(message, task)
            if fallback:
                return fallback
            return None

    if level == "classifier_unavailable":
        fallback = emergency_alert_from_message(message, task)
        if fallback:
            return fallback
        return None

    severity = "Emergency" if level == "emergency" else "Caregiver review"
    if level == "emergency":
        reason = (
            assessment.get("reason")
            or "Patient message may indicate a serious safety risk."
        )
        reason = f"{reason} Contact the caregiver immediately and call emergency services if there may be danger."
    else:
        reason = (
            assessment.get("reason")
            or "Patient message may indicate a health concern. Caregiver review is recommended."
        )
    return {
        "severity": severity,
        "reason": reason,
        "task_id": task.get("task_id") if task else None,
        "task_name": task.get("task_name") if task else None,
        "patient_message": message,
    }


def normalize_phone_number(value: object) -> str:
    raw_phone = str(value or "").strip()
    if not raw_phone:
        return ""

    digits = re.sub(r"\D", "", raw_phone)
    if len(digits) == 10:
        return f"+1{digits}"
    if len(digits) == 11 and digits.startswith("1"):
        return f"+{digits}"
    if raw_phone.startswith("+") and 8 <= len(digits) <= 15:
        return f"+{digits}"
    raise ValueError("Enter a valid phone number, including the country code when outside the U.S.")


def text_service_is_configured() -> bool:
    return all(
        os.getenv(name)
        for name in (
            "TWILIO_ACCOUNT_SID",
            "TWILIO_AUTH_TOKEN",
            "TWILIO_FROM_PHONE",
        )
    )


def client_account_payload(account: dict | None) -> dict | None:
    if account is None:
        return None
    payload = dict(account)
    payload["sms_service_configured"] = text_service_is_configured()
    return payload


def text_alert_unavailable_status(user_id: str) -> str:
    settings = database.get_account_sms_settings(user_id)
    if settings is None or not settings["phone"]:
        return "Phone not configured"
    if not settings["enabled"]:
        return "Text alerts disabled"
    if not text_service_is_configured():
        return "Text service not configured"
    return ""


def send_text_alert(alert: dict, user_id: str) -> str:
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_phone = os.getenv("TWILIO_FROM_PHONE")
    settings = database.get_account_sms_settings(user_id)
    to_phone = settings["phone"] if settings else ""

    unavailable_status = text_alert_unavailable_status(user_id)
    if unavailable_status:
        return unavailable_status

    task_text = f" Task: {alert['task_name']}." if alert.get("task_name") else ""
    patient_message = str(alert.get("patient_message", "")).strip()
    message_text = f' Patient said: "{patient_message}"' if patient_message else ""
    body_text = (
        f"AURA {alert['severity']} alert: {alert['reason']}"
        f"{task_text}{message_text}"
    )
    body = urlencode(
        {
            "From": from_phone,
            "To": to_phone,
            "Body": body_text[:1500],
        }
    ).encode("utf-8")
    credentials = base64.b64encode(
        f"{account_sid}:{auth_token}".encode("utf-8")
    ).decode("ascii")
    request = Request(
        f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json",
        data=body,
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=10) as response:
            if 200 <= response.status < 300:
                return "Text sent"
            return f"Text failed with status {response.status}"
    except Exception as error:
        return f"Text failed: {error}"


def deliver_text_alert(saved_alert: dict, user_id: str) -> None:
    text_status = send_text_alert(saved_alert, user_id)
    database.update_alert_text_status(saved_alert["alert_id"], text_status)


def create_alert(alert: dict, user_id: str) -> dict:
    text_status = text_alert_unavailable_status(user_id)
    alert["text_status"] = text_status or "Sending"
    saved_alert = database.save_alert(alert, user_id=user_id)
    if not text_status:
        Thread(
            target=deliver_text_alert,
            args=(dict(saved_alert), user_id),
            name=f"aura-text-alert-{saved_alert['alert_id']}",
            daemon=True,
        ).start()
    chat_message = (
        f"{saved_alert['severity']} alert: {saved_alert['reason']}\n"
        f"Patient said: {saved_alert.get('patient_message', '')}\n"
        f"Text status: {saved_alert.get('text_status', '')}"
    )
    database.add_caregiver_chat("assistant", chat_message, user_id=user_id)
    return saved_alert


def patient_payload(
    user_message: str,
    answer: str,
    alert: dict | None = None,
    target_language: str | None = None,
    use_ai_phrasing: bool = True,
) -> dict:
    if not use_ai_phrasing:
        return {
            "answer": answer,
            "alert": alert,
        }
    return {
        "answer": localize_patient_text(
            client,
            AURA_PATIENT_MODEL,
            answer,
            user_message,
            target_language,
        ),
        "alert": alert,
    }


def score_and_update_attempt(attempt_id: int, **updates: object) -> dict:
    attempt = database.update_attempt(attempt_id, **updates)
    raw_score, adjusted_score = score_attempt(attempt)
    return database.update_attempt(
        attempt_id,
        raw_performance_score=raw_score,
        adjusted_performance_score=adjusted_score,
    )


def alert_for_attempt(
    attempt: dict,
    reason: str,
    user_id: str,
    severity: str = "Caregiver review",
) -> dict:
    alert = {
        "severity": severity,
        "reason": reason,
        "task_id": attempt.get("task_id"),
        "task_name": attempt.get("task_name"),
        "patient_message": attempt.get("notes", ""),
    }
    saved_alert = create_alert(alert, user_id)
    database.update_attempt(attempt["attempt_id"], caregiver_alert=1)
    return saved_alert


def missed_task_deadline(scheduled_time: str, reference_time: datetime) -> datetime:
    scheduled_clock_time = datetime.strptime(scheduled_time, "%H:%M").time()
    scheduled_at = datetime.combine(
        reference_time.date(),
        scheduled_clock_time,
        tzinfo=reference_time.tzinfo,
    )
    return scheduled_at + timedelta(minutes=TASK_GRACE_PERIOD_MINUTES)


def _mark_overdue_tasks(user_id: str) -> None:
    context = database.today_context()
    now = test_clock.now()
    routines = database.list_routines(active_only=True, user_id=user_id)
    today_attempts = database.list_today_attempts(user_id=user_id)
    attempted_task_ids = {attempt["task_id"] for attempt in today_attempts}

    for routine in routines:
        if routine["task_id"] in attempted_task_ids:
            continue
        try:
            missed_at = missed_task_deadline(routine["scheduled_time"], now)
        except ValueError:
            continue
        if now < missed_at:
            continue
        if database.was_dataset_cleared_after_schedule(
            user_id,
            context["date"],
            routine["scheduled_time"],
        ):
            continue

        attempt_id = database.create_attempt(routine, user_id=user_id)
        missed_attempt = score_and_update_attempt(
            attempt_id,
            completed=0,
            missed=1,
            completed_at=context["timestamp"],
            notes=(
                "Task was marked missed after the "
                f"{TASK_GRACE_PERIOD_MINUTES}-minute grace period."
            ),
        )

        is_important = int(routine["task_importance"]) >= 4
        reason = (
            "Important task was missed after the grace period. Caregiver review is recommended."
            if is_important
            else "Scheduled task was missed after the grace period. Caregiver review is recommended."
        )
        alert_for_attempt(missed_attempt, reason, user_id)


def mark_overdue_tasks(user_id: str) -> None:
    with overdue_lock:
        _mark_overdue_tasks(user_id)


def monitor_missed_tasks(stop_event: Event) -> None:
    while not stop_event.is_set():
        try:
            for account in database.list_accounts():
                mark_overdue_tasks(account["username"])
        except Exception as error:
            print(f"AURA missed-task monitor error: {type(error).__name__}: {error}")
        stop_event.wait(MISSED_TASK_MONITOR_SECONDS)


def start_task(
    session: dict,
    user_id: str,
    routine: dict | None = None,
) -> tuple[str, dict | None]:
    routine = routine or database.get_next_routine(user_id)
    if routine is None:
        session["current_task"] = None
        return "Hi. I'm here with you. You are okay.", None

    attempt_id = database.create_attempt(routine, user_id=user_id)
    session["current_task"] = {
        "task_id": routine["task_id"],
        "attempt_id": attempt_id,
        "step_index": 0,
    }
    first_step = routine["instructions"][0] if routine["instructions"] else "Please begin."
    return f"It's time to {routine['task_name']}. {first_step}", routine


def get_current_task(session: dict, user_id: str) -> tuple[dict | None, dict | None]:
    current = session.get("current_task")
    if not current:
        return None, None
    routine = database.get_routine(current["task_id"], user_id=user_id)
    attempt = database.get_attempt(current["attempt_id"])
    if routine is None or attempt is None:
        session["current_task"] = None
        return None, None
    return routine, attempt


def complete_current_step(session: dict, user_id: str) -> tuple[str, dict | None]:
    routine, attempt = get_current_task(session, user_id)
    if routine is None or attempt is None:
        return start_task(session, user_id)

    current = session["current_task"]
    instructions = routine["instructions"]
    step_index = int(current["step_index"])

    if step_index < len(instructions) - 1:
        step_index += 1
        current["step_index"] = step_index
        return f"Good. {instructions[step_index]}", None

    completed_at = current_timestamp()
    time_to_complete = seconds_since(attempt.get("started_at"))
    updated_attempt = score_and_update_attempt(
        attempt["attempt_id"],
        completed=1,
        missed=0,
        time_to_complete=time_to_complete,
        completed_at=completed_at,
        notes="Marked complete by patient.",
    )
    session["current_task"] = None
    return f"Good. {updated_attempt['task_name']} is marked complete.", None


def complete_current_task(
    session: dict,
    user_id: str,
    note: str = "Marked complete by patient.",
) -> tuple[str, dict | None]:
    routine, attempt = get_current_task(session, user_id)
    if routine is None or attempt is None:
        return start_task(session, user_id)

    completed_at = current_timestamp()
    time_to_complete = seconds_since(attempt.get("started_at"))
    updated_attempt = score_and_update_attempt(
        attempt["attempt_id"],
        completed=1,
        missed=0,
        time_to_complete=time_to_complete,
        completed_at=completed_at,
        notes=note,
    )
    session["current_task"] = None
    return f"Good. {updated_attempt['task_name']} is marked complete.", None


def task_words(routine: dict | None) -> set[str]:
    if routine is None:
        return set()
    text = " ".join(
        [
            str(routine.get("task_name", "")),
            str(routine.get("task_category", "")),
            str(routine.get("task_id", "")),
        ]
    ).lower()
    words = {word for word in re.findall(r"[a-z0-9]+", text) if len(word) >= 4}
    if "medicine" in text or "medication" in text:
        words.update({"medicine", "medication", "meds", "pill", "pills"})
    if "hearing" in text:
        words.update({"hearing", "aids"})
    return words


def patient_says_task_is_complete(message: str, routine: dict | None) -> bool:
    lower = message.lower().strip()
    words = task_words(routine)
    completion_phrases = [
        "done with",
        "finished with",
        "completed",
        "all done",
        "i did it",
        "i have done",
        "i already did",
        "already done",
        "i finished",
        "i am finished",
        "i'm finished",
    ]
    took_medication_phrases = [
        "i took my medication",
        "i took the medication",
        "i took my medicine",
        "i took the medicine",
        "i took my pills",
        "i took the pills",
        "i have taken my medication",
        "i have taken my medicine",
        "i'm done taking medication",
        "im done taking medication",
        "done taking medication",
        "done with taking medication",
    ]
    if any(phrase in lower for phrase in took_medication_phrases):
        return bool(words & {"medicine", "medication", "meds", "pill", "pills"})
    if "done" in lower and "taking medication" in lower:
        return bool(words & {"medicine", "medication", "meds", "pill", "pills"})
    if "done" in lower and "taking medicine" in lower:
        return bool(words & {"medicine", "medication", "meds", "pill", "pills"})
    if "done" in lower and "taking pills" in lower:
        return bool(words & {"medicine", "medication", "meds", "pill", "pills"})
    if "done" in lower and "hearing" in lower:
        return "hearing" in words
    if "finished" in lower and "hearing" in lower:
        return "hearing" in words
    if not any(phrase in lower for phrase in completion_phrases):
        return False
    if not words:
        return False
    if "medication" in lower or "medicine" in lower or "pills" in lower:
        return bool(words & {"medicine", "medication", "meds", "pill", "pills"})
    if "hearing" in lower:
        return "hearing" in words
    return any(word in lower for word in words)


def patient_requested_caregiver_help(message: str, routine: dict | None) -> bool:
    lower = message.lower().strip()
    direct_help_phrases = {
        "help",
        "help me",
        "please help",
        "help please",
        "i need help",
        "need help",
        "i need some help",
        "can you help me",
    }
    if lower in direct_help_phrases:
        return True
    if routine is None or "help" not in lower:
        return False
    task_help_phrases = [
        "help with this",
        "help with the task",
        "help me with this",
        "help me do this",
        "i need help with this",
        "i need help with the task",
    ]
    return any(phrase in lower for phrase in task_help_phrases)


def repeat_current_step(session: dict, user_id: str) -> str:
    routine, attempt = get_current_task(session, user_id)
    if routine is None or attempt is None:
        due = due_routine(user_id)
        if due is None:
            return "There is no task right now. I will remind you when it is time."
        answer, _ = start_task(session, user_id, due)
        return answer

    reminders_needed = int(attempt.get("reminders_needed") or 0) + 1
    updated_attempt = score_and_update_attempt(
        attempt["attempt_id"],
        reminders_needed=reminders_needed,
        notes="Reminder requested by patient.",
    )
    if reminders_needed >= 3:
        alert_for_attempt(
            updated_attempt,
            "Multiple reminders were required. Caregiver review is recommended.",
            user_id,
        )

    step_index = int(session["current_task"]["step_index"])
    return routine["instructions"][step_index]


def mark_help_requested(session: dict, message: str, user_id: str) -> tuple[str, dict | None]:
    routine, attempt = get_current_task(session, user_id)
    if attempt is None:
        alert = create_alert(
            {
                "severity": "Caregiver review",
                "reason": "Patient requested help outside an active task.",
                "patient_message": message,
            },
            user_id,
        )
        return "I let your caregiver know. Tell me what you need help with.", alert

    updated_attempt = score_and_update_attempt(
        attempt["attempt_id"],
        help_requested=1,
        caregiver_alert=1,
        notes=f"Help requested. Patient said: {message}",
    )
    alert = alert_for_attempt(
        updated_attempt,
        "Help was requested. Caregiver review is recommended.",
        user_id,
    )
    return "I let your caregiver know. Tell me what you need help with.", alert


def mark_confusion(session: dict, message: str, user_id: str) -> tuple[str, dict | None]:
    routine, attempt = get_current_task(session, user_id)
    alert = None
    if attempt is not None:
        updated_attempt = score_and_update_attempt(
            attempt["attempt_id"],
            confusion_flag=1,
            notes=f"Possible confusion flag. Patient said: {message}",
        )
        alert = alert_for_attempt(
            updated_attempt,
            "Possible confusion flag. Caregiver review is recommended.",
            user_id,
        )
    return "That's okay. I will help you one step at a time.", alert


def patient_task_summary(routine: dict | None) -> dict | None:
    if routine is None:
        return None
    instructions = routine.get("instructions") or []
    return {
        "task_id": routine.get("task_id"),
        "task_name": routine.get("task_name"),
        "task_category": routine.get("task_category"),
        "task_difficulty": routine.get("task_difficulty"),
        "task_importance": routine.get("task_importance"),
        "scheduled_time": routine.get("scheduled_time"),
        "time_of_day": routine.get("time_of_day"),
        "first_step": instructions[0] if instructions else None,
    }


def patient_agent_decision(
    session: dict,
    message: str,
    target_language: str | None,
    user_id: str,
) -> dict:
    routine, _attempt = get_current_task(session, user_id)
    instruction = current_instruction(session, user_id)
    due = due_routine(user_id)
    payload = {
        "patient_message": message,
        "recent_conversation": session.get("patient_chat_history", [])[-12:],
        "target_language_code": normalize_language_code(target_language),
        "current_task": patient_task_summary(routine),
        "current_step": instruction,
        "due_task": patient_task_summary(due),
        "quick_actions": ["Done", "Help"],
        "rules": [
            "If there is no current_task and no due_task, answer like a general AI assistant.",
            "If current_task is present, answer the question briefly and include the current_step.",
            "If due_task is present and no current_task is present, answer the question briefly and include the due_task first_step.",
            "Never provide diagnosis, medical advice, or medication changes.",
        ],
    }
    response = create_ai_response(
        "patient",
        AURA_PATIENT_MODEL,
        instructions=PATIENT_AGENT_PROMPT,
        input=json.dumps(payload, indent=2),
    )
    output = response.output_text.strip()
    parsed = extract_json_object(output)
    if parsed is None:
        if not output:
            raise RuntimeError("The patient AI returned an empty response.")
        return {
            "priority": "task" if routine is not None or due is not None else "chat",
            "answer": compact_patient_answer(output),
            "reason": "",
        }

    priority = str(parsed.get("priority", "chat")).strip().lower()
    if priority not in {"emergency", "caregiver_review", "task", "chat"}:
        priority = "emergency"
    answer = compact_patient_answer(str(parsed.get("answer", "")))
    if not answer:
        raise RuntimeError("The patient AI returned an empty answer.")
    return {
        "priority": priority,
        "answer": answer,
        "reason": str(parsed.get("reason", "")).strip(),
    }


def patient_agent_answer(
    session: dict,
    message: str,
    target_language: str | None,
    user_id: str,
) -> str:
    return patient_agent_decision(session, message, target_language, user_id)["answer"]


def patient_alert_from_assessment(
    assessment: dict,
    message: str,
    task: dict | None,
) -> dict:
    level = str(assessment.get("level", "caregiver_review")).strip().lower()
    severity = "Emergency" if level == "emergency" else "Caregiver review"
    reason = str(assessment.get("reason", "")).strip()
    if not reason:
        reason = (
            "Patient message may indicate a serious safety risk."
            if severity == "Emergency"
            else "Patient described a possible health or safety concern."
        )
    if severity == "Emergency" and "emergency services" not in reason.lower():
        reason = f"{reason} Contact the caregiver immediately and call emergency services if there may be danger."
    return {
        "severity": severity,
        "reason": reason,
        "task_id": task.get("task_id") if task else None,
        "task_name": task.get("task_name") if task else None,
        "patient_message": message,
    }


def compact_patient_answer(answer: str, max_words: int = 40) -> str:
    clean_answer = re.sub(r"\s+", " ", answer).strip()
    if not clean_answer:
        return clean_answer
    sentences = [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", clean_answer)
        if sentence.strip()
    ]
    compact_answer = " ".join(sentences[:2])
    words = compact_answer.split()
    if len(words) <= max_words:
        return compact_answer
    first_sentence = sentences[0]
    if len(first_sentence.split()) <= max_words:
        return first_sentence
    return f"{' '.join(words[:max_words]).rstrip('.,;:')}..."


def patient_safety_answer(
    session: dict,
    message: str,
    alert: dict,
    target_language: str | None,
    suggested_answer: str | None = None,
) -> str:
    response = create_ai_response(
        "patient",
        AURA_PATIENT_MODEL,
        instructions=PATIENT_SAFETY_RESPONSE_PROMPT,
        input=json.dumps(
            {
                "patient_message": message,
                "alert_severity": alert.get("severity"),
                "caregiver_reason": alert.get("reason"),
                "classification_draft": suggested_answer,
                "target_language_code": normalize_language_code(target_language),
                "recent_conversation": session.get("patient_chat_history", [])[-6:],
            },
            indent=2,
        ),
    )
    answer = compact_patient_answer(response.output_text, max_words=30)
    if not answer:
        raise RuntimeError("The patient safety response was empty.")
    return answer


def patient_safety_response(
    session: dict,
    message: str,
    target_language: str | None,
    user_id: str,
    routine: dict | None,
    attempt: dict | None,
    alert: dict,
    suggested_answer: str | None = None,
) -> dict:
    if attempt is not None:
        emergency_attempt = score_and_update_attempt(
            attempt["attempt_id"],
            help_requested=1,
            notes=f"Safety risk reported by patient. Patient said: {message}",
        )
        database.update_attempt(
            emergency_attempt["attempt_id"],
            caregiver_alert=1,
        )
    saved_alert = create_alert(alert, user_id)
    try:
        answer = patient_safety_answer(
            session,
            message,
            saved_alert,
            target_language,
            suggested_answer=suggested_answer,
        )
    except Exception as error:
        print(f"AURA patient safety response error: {type(error).__name__}: {error}")
        if saved_alert.get("severity") == "Emergency":
            answer = "I alerted your caregiver. Call 911 now and follow the dispatcher's instructions."
        else:
            answer = "I alerted your caregiver. Please tell them what happened."
    return patient_payload(
        message,
        answer,
        saved_alert,
        target_language,
        use_ai_phrasing=False,
    )


def patient_response(
    session: dict,
    message: str,
    target_language: str | None = None,
    user_id: str = USER_ID,
) -> dict:
    lower = message.lower().strip()
    routine, attempt = get_current_task(session, user_id)
    local_assessment = local_medical_safety_assessment(message)
    if local_assessment is not None:
        return patient_safety_response(
            session,
            message,
            target_language,
            user_id,
            routine,
            attempt,
            patient_alert_from_assessment(local_assessment, message, routine),
        )

    if "who are you" in lower:
        return patient_payload(message, "I am AURA. I help you with your day.", target_language=target_language)

    if "confused" in lower:
        answer, alert = mark_confusion(session, message, user_id)
        return patient_payload(message, answer, alert, target_language, use_ai_phrasing=False)

    if patient_requested_caregiver_help(message, routine):
        answer, alert = mark_help_requested(session, message, user_id)
        return patient_payload(message, answer, alert, target_language, use_ai_phrasing=False)

    if "what do i do now" in lower or "what should i do" in lower or lower in {"hi", "hello"}:
        if routine is not None:
            step_index = int(session["current_task"]["step_index"])
            return patient_payload(message, routine["instructions"][step_index], target_language=target_language)
        due = due_routine(user_id)
        if due is not None:
            answer, _ = start_task(session, user_id, due)
            return patient_payload(message, answer, target_language=target_language)
        decision = patient_agent_decision(session, message, target_language, user_id)
        if decision["priority"] in {"emergency", "caregiver_review"}:
            return patient_safety_response(
                session,
                message,
                target_language,
                user_id,
                routine,
                attempt,
                patient_alert_from_assessment(
                    {
                        "level": decision["priority"],
                        "reason": decision["reason"],
                    },
                    message,
                    routine,
                ),
                suggested_answer=decision["answer"],
            )
        return {"answer": decision["answer"], "alert": None}

    if patient_says_task_is_complete(message, routine):
        answer, alert = complete_current_task(
            session,
            user_id,
            note=f"Marked complete by patient. Patient said: {message}",
        )
        return patient_payload(message, answer, alert, target_language)

    if lower == "done" or "done" in lower or "finished" in lower:
        if routine is None:
            due = due_routine(user_id)
            if due is not None:
                attempt_id = database.create_attempt(due, user_id=user_id)
                updated_attempt = score_and_update_attempt(
                    attempt_id,
                    completed=1,
                    missed=0,
                    time_to_complete=0,
                    completed_at=current_timestamp(),
                    notes=f"Marked complete by patient. Patient said: {message}",
                )
                return patient_payload(
                    message,
                    f"Good. {updated_attempt['task_name']} is marked complete.",
                    target_language=target_language,
                )
            return patient_payload(
                message,
                "Okay. There is no task open right now.",
                target_language=target_language,
            )
        answer, alert = complete_current_step(session, user_id)
        return patient_payload(message, answer, alert, target_language)

    if "remind" in lower or "again" in lower:
        return patient_payload(message, repeat_current_step(session, user_id), target_language=target_language)

    if routine is None:
        due = due_routine(user_id)
        if due is not None:
            start_task(session, user_id, due)

    decision = patient_agent_decision(session, message, target_language, user_id)
    if decision["priority"] in {"emergency", "caregiver_review"}:
        current_routine, current_attempt = get_current_task(session, user_id)
        return patient_safety_response(
            session,
            message,
            target_language,
            user_id,
            current_routine,
            current_attempt,
            patient_alert_from_assessment(
                {
                    "level": decision["priority"],
                    "reason": decision["reason"],
                },
                message,
                current_routine,
            ),
            suggested_answer=decision["answer"],
        )
    return {"answer": decision["answer"], "alert": None}


def current_instruction(session: dict, user_id: str) -> str | None:
    routine, attempt = get_current_task(session, user_id)
    if routine is None or attempt is None:
        return None
    instructions = routine.get("instructions") or []
    if not instructions:
        return None
    step_index = int(session["current_task"].get("step_index", 0))
    if step_index < 0 or step_index >= len(instructions):
        return None
    return instructions[step_index]


def due_routine(user_id: str) -> dict | None:
    now = test_clock.now()
    today_attempts = database.list_today_attempts(user_id=user_id)
    resolved_task_ids = {
        attempt["task_id"]
        for attempt in today_attempts
        if int(attempt.get("completed") or 0) == 1
        or int(attempt.get("missed") or 0) == 1
    }
    due_tasks = []
    for routine in database.list_routines(active_only=True, user_id=user_id):
        if routine["task_id"] in resolved_task_ids:
            continue
        try:
            missed_at = missed_task_deadline(routine["scheduled_time"], now)
        except ValueError:
            continue
        scheduled_at = missed_at - timedelta(minutes=TASK_GRACE_PERIOD_MINUTES)
        if scheduled_at <= now < missed_at:
            due_tasks.append(routine)
    if not due_tasks:
        return None
    return sorted(due_tasks, key=lambda routine: routine["scheduled_time"])[0]


def patient_state_payload(session: dict, user_id: str) -> dict:
    mark_overdue_tasks(user_id)
    routine, _attempt = get_current_task(session, user_id)
    return {
        "currentTask": routine,
        "currentInstruction": current_instruction(session, user_id),
        "dueTask": due_routine(user_id),
        "quickActions": ["Done", "Help"],
        "clock": test_clock.state(),
    }


def format_real_wait(seconds: int | None) -> str:
    if seconds is None:
        return "Paused"
    if seconds <= 0:
        return "Now"
    hours, remainder = divmod(seconds, 3600)
    minutes, remaining_seconds = divmod(remainder, 60)
    if hours:
        return f"{hours} hr {minutes} min"
    if minutes:
        return f"{minutes} min {remaining_seconds} sec"
    return f"{remaining_seconds} sec"


def clock_task_times(user_id: str) -> list[dict]:
    now = test_clock.now()
    clock = test_clock.state()
    speed = float(clock.get("speed") or 0)
    tasks = []
    for routine in database.list_routines(active_only=True, user_id=user_id):
        try:
            scheduled_time = datetime.strptime(
                routine["scheduled_time"],
                "%H:%M",
            ).time()
        except ValueError:
            continue
        scheduled = datetime.combine(now.date(), scheduled_time, tzinfo=now.tzinfo)
        simulated_seconds = int((scheduled - now).total_seconds())
        is_past = simulated_seconds < 0
        if is_past:
            real_seconds = 0
        elif speed <= 0:
            real_seconds = None
        else:
            real_seconds = max(0, int(simulated_seconds / speed))
        task = dict(routine)
        task.update(
            {
                "isPast": is_past,
                "simulatedSecondsUntil": simulated_seconds,
                "realSecondsUntil": real_seconds,
                "realTimeUntil": "Passed" if is_past else format_real_wait(real_seconds),
            }
        )
        tasks.append(task)
    return tasks


def clock_payload(user_id: str) -> dict:
    return {
        "clock": test_clock.state(),
        "tasks": clock_task_times(user_id),
    }


def dashboard_payload(user_id: str) -> dict:
    mark_overdue_tasks(user_id)
    attempts = database.list_attempts(limit=1000, user_id=user_id)
    today_attempts = database.list_today_attempts(user_id=user_id)
    insight_data = insights.build_insights(attempts, today_attempts)
    summary = insights.automatic_summary(today_attempts, insight_data)
    return {
        "routines": database.list_routines(user_id=user_id),
        "todayActivity": today_attempts,
        "alerts": database.list_alerts(limit=20, user_id=user_id),
        "insights": insight_data,
        "summary": summary,
        "caregiverChat": database.list_caregiver_chat(limit=40, user_id=user_id),
        "clock": test_clock.state(),
    }


def dataset_payload(user_id: str) -> dict:
    records = database.excel_dataset_rows(limit=500, user_id=user_id)
    return {
        "summary": database.dataset_summary(user_id),
        "records": records,
        "columns": database.EXCEL_DATASET_HEADERS,
        "databasePath": str(database.DB_PATH),
    }


def dummy_dataset_insights() -> dict:
    source_path = Path.home() / "Downloads" / "Main dataset.xlsx"
    return {
        "sourcePath": str(source_path),
        "sourceFound": source_path.exists(),
        "summary": {
            "taskAttempts": 390,
            "fakeUsers": 1,
            "days": 30,
            "tasksPerDay": 13,
            "completionRate": "68.7%",
            "avgPerformanceScore": 68.0,
            "caregiverAlertRate": "52.6%",
            "confusionFlags": 67,
            "visualSupportsUsed": 57,
        },
        "timeOfDay": [
            {
                "label": "Morning",
                "avgPerformance": 80.8,
                "completionRate": "86.7%",
                "alertRate": "38.0%",
                "confusionFlags": 21,
                "interpretation": "Strongest time block in the dummy data.",
            },
            {
                "label": "Afternoon",
                "avgPerformance": 70.1,
                "completionRate": "66.7%",
                "alertRate": "48.3%",
                "confusionFlags": 11,
                "interpretation": "Moderate performance with some support needs.",
            },
            {
                "label": "Evening",
                "avgPerformance": 50.0,
                "completionRate": "48.3%",
                "alertRate": "75.0%",
                "confusionFlags": 35,
                "interpretation": "Weakest time block in the dummy data.",
            },
        ],
        "difficulty": [
            {
                "label": "Easy",
                "avgPerformance": 78.8,
                "struggleRate": "36.1%",
                "avgReminders": 1.66,
                "attempts": 180,
            },
            {
                "label": "Medium",
                "avgPerformance": 64.5,
                "struggleRate": "58.3%",
                "avgReminders": 2.04,
                "attempts": 120,
            },
            {
                "label": "Hard",
                "avgPerformance": 51.2,
                "struggleRate": "88.9%",
                "avgReminders": 2.16,
                "attempts": 90,
            },
        ],
        "keyFindings": [
            "The dummy data suggests morning routines are the strongest and evening routines need the most review.",
            "Hard tasks show the highest struggle rate, so task difficulty should be considered before blaming time of day alone.",
            "Hearing, exercise, bedtime, and medication-related routines appear to need more support.",
            "Patient-marked completion should not be treated as verified completion without caregiver or device confirmation.",
            "Caregiver alerts are system responses, so behavior signals such as reminders, help requests, possible confusion, and scores are better evidence for modeling.",
        ],
        "recommendedActions": [
            "Schedule harder routines during stronger time blocks when possible.",
            "Use shorter one-step instructions for hearing aid, medication, exercise, and bedtime routines.",
            "Trigger caregiver review for important missed tasks, repeated reminders, help requests, possible confusion, and very low adjusted performance.",
            "Track verification separately from patient-marked completion.",
            "Use Analysis_Ready-style fields for modeling to avoid circular reasoning from alert/recommendation columns.",
        ],
        "modelingNotes": [
            "Use task_difficulty and difficulty_adjusted_score to reduce time-versus-difficulty confounding.",
            "Use struggle_flag and struggle_evidence as behavior-based indicators.",
            "Do not use caregiver_alert_sent, alert_reason, or recommended_action as proof of struggle because those are generated after the system reacts.",
            "Keep raw performance and difficulty-adjusted performance separate so caregivers can see both actual behavior and challenge-weighted context.",
        ],
    }


def admin_payload(selected_user_id: str | None = None) -> dict:
    accounts = database.list_accounts_with_dataset_stats()
    account_ids = {account["username"] for account in accounts}
    selected = selected_user_id if selected_user_id in account_ids else None
    if selected is None and accounts:
        selected = accounts[0]["username"]
    return {
        "accounts": accounts,
        "selectedUserId": selected,
        "dataset": dataset_payload(selected) if selected else None,
        "databasePath": str(database.DB_PATH),
        "dummyInsights": dummy_dataset_insights(),
    }


def verify_admin_credentials(username: str, password: str) -> bool:
    return bool(ADMIN_USERNAME and ADMIN_PASSWORD) and secrets.compare_digest(
        username.strip(), ADMIN_USERNAME
    ) and secrets.compare_digest(password, ADMIN_PASSWORD)


def verify_admin_password(password: str) -> bool:
    return bool(ADMIN_PASSWORD) and secrets.compare_digest(password, ADMIN_PASSWORD)


def caregiver_question_needs_medical_lookup(question: str) -> bool:
    lower = question.lower()
    medical_terms = [
        "medical",
        "medicine",
        "medication",
        "drug",
        "dose",
        "dosage",
        "side effect",
        "symptom",
        "pain",
        "fever",
        "infection",
        "blood pressure",
        "diabetes",
        "stroke",
        "heart attack",
        "chest pain",
        "breathing",
        "fall",
        "fell",
        "injury",
        "bleeding",
        "dizzy",
        "confusion",
        "dehydration",
        "allergic",
        "seizure",
        "vomiting",
        "diarrhea",
        "doctor",
        "hospital",
        "urgent care",
        "should i call",
        "what should i do if",
    ]
    return any(term in lower for term in medical_terms)


def caregiver_answer(
    question: str,
    target_language: str | None = None,
    user_id: str = USER_ID,
) -> str:
    attempts = database.list_attempts(limit=1000, user_id=user_id)
    today_attempts = database.list_today_attempts(user_id=user_id)
    needs_medical_lookup = caregiver_question_needs_medical_lookup(question)
    patient_insights = insights.build_insights(attempts, today_attempts)
    ai_insight_context = {
        "detailSummary": patient_insights.get("detailSummary"),
        "recentTrend": patient_insights.get("recentTrend"),
        "bestTimeOfDay": patient_insights.get("bestTimeOfDay"),
        "worstTimeOfDay": patient_insights.get("worstTimeOfDay"),
        "bestDayOfWeek": patient_insights.get("bestDayOfWeek"),
        "worstDayOfWeek": patient_insights.get("worstDayOfWeek"),
        "hardestTask": patient_insights.get("hardestTask"),
        "hardestTaskCategory": patient_insights.get("hardestTaskCategory"),
        "tasksNeedingReminders": patient_insights.get("tasksNeedingReminders"),
        "tasksNeedingHelp": patient_insights.get("tasksNeedingHelp"),
        "keyFindings": patient_insights.get("keyFindings"),
        "recommendedActions": patient_insights.get("recommendedActions"),
    }
    payload = {
        "caregiver_question": question,
        "recent_conversation": database.list_caregiver_chat(
            limit=20,
            user_id=user_id,
        ),
        "task_attempts": attempts[-200:],
        "today_activity": today_attempts,
        "alerts": database.list_alerts(limit=50, user_id=user_id),
        "insights": ai_insight_context,
        "medical_lookup_enabled": needs_medical_lookup,
    }
    instructions = CAREGIVER_CHAT_PROMPT
    request = {
        "model": AURA_CAREGIVER_MODEL,
        "instructions": instructions,
        "input": json.dumps(payload, indent=2),
    }
    if needs_medical_lookup:
        request["instructions"] = (
            f"{CAREGIVER_CHAT_PROMPT}\n\n{CAREGIVER_MEDICAL_SEARCH_PROMPT}"
        )
        request["tools"] = [{"type": "web_search"}]
    response = create_ai_response(
        "caregiver",
        AURA_CAREGIVER_MODEL,
        **request,
    )
    return localize_text(
        client,
        AURA_CAREGIVER_MODEL,
        response.output_text,
        question,
        target_language,
    )


class AuraWebHandler(SimpleHTTPRequestHandler):
    server_version = "AuraWeb/2.0"

    def log_message(self, format: str, *args: object) -> None:
        return

    def send_json(
        self,
        status: int,
        payload: dict,
        session_id: str | None = None,
        extra_cookies: list[str] | None = None,
    ) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        if session_id:
            self.send_header(
                "Set-Cookie",
                (
                    f"aura_session={session_id}; Path=/; "
                    f"Max-Age={AUTH_COOKIE_MAX_AGE}; SameSite=Lax; HttpOnly"
                ),
            )
        for cookie_header in extra_cookies or []:
            self.send_header("Set-Cookie", cookie_header)
        self.end_headers()
        self.wfile.write(body)

    def read_json_body(self) -> dict:
        content_length = int(self.headers.get("Content-Length", "0"))
        if content_length == 0:
            return {}
        raw_body = self.rfile.read(content_length)
        return json.loads(raw_body.decode("utf-8"))

    def require_caregiver(self, session_id: str) -> bool:
        state = get_session_state(session_id)
        if (
            state.get("active_role") == "caregiver"
            and state.get("caregiver_authenticated")
        ):
            return True
        self.send_json(
            403,
            {"error": "Please sign in through the caregiver interface."},
            session_id=session_id,
        )
        return False

    def require_dataset_access(self, session_id: str) -> bool:
        state = get_session_state(session_id)
        if (
            state.get("active_role") == "caregiver"
            and state.get("caregiver_authenticated")
            and state.get("dataset_authenticated")
        ):
            return True
        self.send_json(
            403,
            {"error": "Please sign in through the caregiver interface."},
            session_id=session_id,
        )
        return False

    def require_admin(self, session_id: str) -> bool:
        state = get_session_state(session_id)
        if state.get("admin_authenticated"):
            return True
        self.send_json(
            403,
            {"error": "Admin username and password required."},
            session_id=session_id,
        )
        return False

    def require_auth(self, session_id: str) -> bool:
        session = get_session_state(session_id)
        account = account_from_request(self.headers.get("Cookie"), session)
        if account is not None:
            return True
        self.send_json(
            401,
            {"error": "Please sign in first."},
            session_id=session_id,
        )
        return False

    def do_GET(self) -> None:
        path = route_path(self.path)
        session_id = get_cookie_session(self.headers.get("Cookie"))
        session = get_session_state(session_id)

        if path == "/api/auth-state":
            account = account_from_request(self.headers.get("Cookie"), session)
            if account is not None:
                database.ensure_default_routines(account["username"])
                query = parse_qs(urlparse(self.path).query)
                requested_role = (query.get("role") or ["patient"])[0]
                active_role = "caregiver" if requested_role == "caregiver" else "patient"
                session["active_role"] = active_role
                session["caregiver_authenticated"] = active_role == "caregiver"
                session["dataset_authenticated"] = active_role == "caregiver"
            self.send_json(
                200,
                {
                    "authenticated": account is not None,
                    "hasAccount": database.account_count() > 0,
                    "account": client_account_payload(account),
                    "caregiverAuthenticated": bool(
                        session.get("caregiver_authenticated")
                    ),
                    "role": session.get("active_role", "patient"),
                },
                session_id=session_id,
            )
            return

        if path == "/api/languages":
            self.send_json(
                200,
                {"languages": get_supported_languages()},
                session_id=session_id,
            )
            return

        if path == "/api/admin":
            if not self.require_admin(session_id):
                return
            query = parse_qs(urlparse(self.path).query)
            selected_user_id = (query.get("user_id") or [None])[0]
            self.send_json(
                200,
                admin_payload(selected_user_id),
                session_id=session_id,
            )
            return

        if path == "/api/patient-state":
            if not self.require_auth(session_id):
                return
            user_id = session_user_id(session)
            self.send_json(
                200,
                patient_state_payload(session, user_id),
                session_id=session_id,
            )
            return

        if path == "/api/clock":
            if not self.require_auth(session_id):
                return
            if not self.require_caregiver(session_id):
                return
            self.send_json(
                200,
                clock_payload(session_user_id(session)),
                session_id=session_id,
            )
            return

        if path == "/api/caregiver":
            if not self.require_auth(session_id):
                return
            if not self.require_caregiver(session_id):
                return
            self.send_json(
                200,
                dashboard_payload(session_user_id(session)),
                session_id=session_id,
            )
            return

        if path == "/api/caregiver-notifications":
            if not self.require_auth(session_id):
                return
            if not self.require_caregiver(session_id):
                return
            user_id = session_user_id(session)
            mark_overdue_tasks(user_id)
            alerts = database.list_alerts(limit=20, user_id=user_id)
            latest_alert_id = max(
                (int(alert.get("alert_id") or 0) for alert in alerts),
                default=0,
            )
            self.send_json(
                200,
                {
                    "alerts": alerts,
                    "latestAlertId": latest_alert_id,
                },
                session_id=session_id,
            )
            return

        if path == "/api/patient-caregiver-chat":
            if not self.require_auth(session_id):
                return
            self.send_json(
                200,
                {
                    "messages": database.list_patient_caregiver_messages(
                        limit=80,
                        user_id=session_user_id(session),
                    )
                },
                session_id=session_id,
            )
            return

        if path == "/api/dataset":
            if not self.require_auth(session_id):
                return
            if not self.require_dataset_access(session_id):
                return
            self.send_json(
                200,
                dataset_payload(session_user_id(session)),
                session_id=session_id,
            )
            return

        if path == "/api/export":
            if not self.require_auth(session_id):
                return
            if not self.require_caregiver(session_id):
                return
            export_path = database.export_attempts_csv(user_id=session_user_id(session))
            content = export_path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.send_header(
                "Content-Disposition",
                'attachment; filename="aura_task_attempts.csv"',
            )
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return

        if path == "/api/admin-export":
            if not self.require_admin(session_id):
                return
            query = parse_qs(urlparse(self.path).query)
            selected_user_id = (query.get("user_id") or [""])[0]
            if not database.get_account(selected_user_id):
                self.send_json(
                    404,
                    {"error": "Unknown account."},
                    session_id=session_id,
                )
                return
            export_path = database.export_attempts_csv(user_id=selected_user_id)
            content = export_path.read_bytes()
            safe_name = re.sub(r"[^a-zA-Z0-9_-]+", "-", selected_user_id).strip("-")
            self.send_response(200)
            self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.send_header(
                "Content-Disposition",
                f'attachment; filename="aura_{safe_name}_task_attempts.csv"',
            )
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return

        if path.startswith("/api/"):
            self.send_json(404, {"error": "Unknown endpoint."}, session_id=session_id)
            return

        file_path = resolve_static_path(self.path)
        if file_path is None:
            self.send_error(404)
            return
        content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        content = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self) -> None:
        path = route_path(self.path)
        session_id = get_cookie_session(self.headers.get("Cookie"))
        session = get_session_state(session_id)

        if path == "/api/register":
            body = self.read_json_body()
            username = str(body.get("username", "")).strip()
            password = str(body.get("password", ""))
            caregiver_password = str(body.get("caregiver_password", ""))
            patient_name = str(body.get("patient_name", "")).strip()
            caregiver_name = str(body.get("caregiver_name", "")).strip()
            role = "caregiver" if body.get("role") == "caregiver" else "patient"
            try:
                caregiver_phone = normalize_phone_number(body.get("caregiver_phone", ""))
            except ValueError as error:
                self.send_json(
                    400,
                    {"error": str(error)},
                    session_id=session_id,
                )
                return

            if not all(
                [
                    username,
                    password,
                    caregiver_password,
                    patient_name,
                    caregiver_name,
                ]
            ):
                self.send_json(
                    400,
                    {"error": "Please fill in every sign up field."},
                    session_id=session_id,
                )
                return
            if len(password) < 4:
                self.send_json(
                    400,
                    {"error": "Password must be at least 4 characters."},
                    session_id=session_id,
                )
                return
            if len(caregiver_password) < 4:
                self.send_json(
                    400,
                    {"error": "Caregiver password must be at least 4 characters."},
                    session_id=session_id,
                )
                return
            if database.get_account(username) is not None:
                self.send_json(
                    409,
                    {"error": "That username already exists."},
                    session_id=session_id,
                )
                return

            account = database.create_account(
                username=username,
                password=password,
                caregiver_password=caregiver_password,
                patient_name=patient_name,
                caregiver_name=caregiver_name,
                caregiver_phone=caregiver_phone,
            )
            database.ensure_default_routines(account["username"])
            set_authenticated_session(session, account)
            session["active_role"] = role
            session["caregiver_authenticated"] = role == "caregiver"
            session["dataset_authenticated"] = role == "caregiver"
            self.send_json(
                200,
                {
                    "ok": True,
                    "authenticated": True,
                    "account": client_account_payload(account),
                    "hasAccount": True,
                    "role": role,
                },
                session_id=session_id,
                extra_cookies=[create_auth_cookie(account)],
            )
            return

        if path == "/api/login":
            body = self.read_json_body()
            username = str(body.get("username", "")).strip()
            role = "caregiver" if body.get("role") == "caregiver" else "patient"
            try:
                caregiver_phone = normalize_phone_number(body.get("caregiver_phone", ""))
            except ValueError as error:
                self.send_json(
                    400,
                    {"error": str(error)},
                    session_id=session_id,
                )
                return
            account = database.verify_account(
                username,
                str(body.get("password", "")),
                str(body.get("caregiver_password", "")),
            )
            if account is None:
                self.send_json(
                    401,
                    {"error": "Incorrect username, password, or caregiver password."},
                    session_id=session_id,
                )
                return
            if caregiver_phone:
                account = database.update_account_phone(username, caregiver_phone)
            set_authenticated_session(session, account)
            session["active_role"] = role
            session["caregiver_authenticated"] = role == "caregiver"
            session["dataset_authenticated"] = role == "caregiver"
            database.ensure_default_routines(account["username"])
            self.send_json(
                200,
                {
                    "ok": True,
                    "authenticated": True,
                    "account": client_account_payload(account),
                    "hasAccount": True,
                    "role": role,
                },
                session_id=session_id,
                extra_cookies=[create_auth_cookie(account)],
            )
            return

        if path == "/api/admin-login":
            body = self.read_json_body()
            if not verify_admin_credentials(
                str(body.get("username", "")),
                str(body.get("password", "")),
            ):
                self.send_json(
                    401,
                    {"error": "Incorrect admin username or password."},
                    session_id=session_id,
                )
                return
            session["admin_authenticated"] = True
            self.send_json(
                200,
                {"ok": True, "admin": admin_payload()},
                session_id=session_id,
            )
            return

        if path == "/api/admin-logout":
            session["admin_authenticated"] = False
            self.send_json(200, {"ok": True}, session_id=session_id)
            return

        if path == "/api/logout":
            clear_authenticated_session(session)
            self.send_json(
                200,
                {"ok": True, "authenticated": False},
                session_id=session_id,
                extra_cookies=[clear_auth_cookie(self.headers.get("Cookie"))],
            )
            return

        if not self.require_auth(session_id):
            return

        if path == "/api/sms-settings":
            if not self.require_caregiver(session_id):
                return
            body = self.read_json_body()
            enabled = body.get("enabled")
            if not isinstance(enabled, bool):
                self.send_json(
                    400,
                    {"error": "Choose whether text messages should be on or off."},
                    session_id=session_id,
                )
                return
            try:
                account = database.set_account_sms_enabled(
                    session_user_id(session),
                    enabled,
                )
            except ValueError as error:
                self.send_json(
                    400,
                    {"error": str(error)},
                    session_id=session_id,
                )
                return
            if account is None:
                self.send_json(
                    404,
                    {"error": "Account not found."},
                    session_id=session_id,
                )
                return
            session["account"] = account
            self.send_json(
                200,
                {"ok": True, "account": client_account_payload(account)},
                session_id=session_id,
            )
            return

        if path == "/api/caregiver-login":
            body = self.read_json_body()
            account = session.get("account")
            if account is None:
                self.send_json(
                    401,
                    {"error": "Please sign in first."},
                    session_id=session_id,
                )
                return
            if not database.verify_caregiver_password(
                account["username"],
                str(body.get("password", "")),
            ):
                self.send_json(
                    401,
                    {"error": "Incorrect caregiver password."},
                    session_id=session_id,
                )
                return
            session["caregiver_authenticated"] = True
            self.send_json(200, {"ok": True}, session_id=session_id)
            return

        if path == "/api/dataset-login":
            body = self.read_json_body()
            account = session.get("account")
            if account is None:
                self.send_json(
                    401,
                    {"error": "Please sign in first."},
                    session_id=session_id,
                )
                return
            if not database.verify_caregiver_password(
                account["username"],
                str(body.get("password", "")),
            ):
                self.send_json(
                    401,
                    {"error": "Incorrect caregiver password."},
                    session_id=session_id,
                )
                return
            session["dataset_authenticated"] = True
            self.send_json(
                200,
                {"ok": True, "dataset": dataset_payload(session_user_id(session))},
                session_id=session_id,
            )
            return

        if path == "/api/clock":
            if not self.require_caregiver(session_id):
                return
            body = self.read_json_body()
            action = str(body.get("action", "speed"))
            if action == "reset":
                clock_state = test_clock.reset()
            else:
                try:
                    requested_speed = float(body.get("speed", 1))
                except (TypeError, ValueError):
                    self.send_json(
                        400,
                        {"error": "Clock speed must be a number."},
                        session_id=session_id,
                    )
                    return
                clock_state = test_clock.set_speed(requested_speed)
            self.send_json(
                200,
                {
                    **clock_payload(session_user_id(session)),
                    "dashboard": dashboard_payload(session_user_id(session))
                    if session.get("caregiver_authenticated")
                    else None,
                },
                session_id=session_id,
            )
            return

        if path == "/api/clear":
            session["current_task"] = None
            session["patient_chat_history"] = []
            self.send_json(200, {"ok": True}, session_id=session_id)
            return

        if path == "/api/routines":
            if not self.require_caregiver(session_id):
                return
            user_id = session_user_id(session)
            routine = database.save_routine(self.read_json_body(), user_id=user_id)
            self.send_json(
                200,
                {
                    "routine": routine,
                    "routines": database.list_routines(user_id=user_id),
                    "dashboard": dashboard_payload(user_id),
                },
                session_id=session_id,
            )
            return

        if path == "/api/routines/delete":
            if not self.require_caregiver(session_id):
                return
            body = self.read_json_body()
            task_id = str(body.get("task_id", "")).strip()
            if not task_id:
                self.send_json(
                    400,
                    {"error": "Missing task id."},
                    session_id=session_id,
                )
                return
            user_id = session_user_id(session)
            deleted = database.delete_routine(task_id, user_id=user_id)
            current = session.get("current_task")
            if current and current.get("task_id") == task_id:
                session["current_task"] = None
            self.send_json(
                200,
                {
                    "ok": True,
                    "deleted": deleted,
                    "routines": database.list_routines(user_id=user_id),
                    "dashboard": dashboard_payload(user_id),
                },
                session_id=session_id,
            )
            return

        if path == "/api/caregiver-chat":
            if not self.require_caregiver(session_id):
                return
            body = self.read_json_body()
            question = str(body.get("message", "")).strip()
            target_language = normalize_language_code(body.get("language"))
            if not question:
                self.send_json(400, {"error": "Please type a question first."})
                return
            user_id = session_user_id(session)
            database.add_caregiver_chat("caregiver", question, user_id=user_id)
            try:
                answer = caregiver_answer(question, target_language, user_id)
            except Exception as error:
                answer = ai_service_error_message(error, audience="caregiver")
                print(f"AURA caregiver AI error: {type(error).__name__}: {error}")
                database.add_caregiver_chat("assistant", answer, user_id=user_id)
                self.send_json(
                    503,
                    {"error": answer},
                    session_id=session_id,
                )
                return
            database.add_caregiver_chat("assistant", answer, user_id=user_id)
            self.send_json(
                200,
                {
                    "answer": answer,
                    "dashboard": dashboard_payload(user_id),
                },
                session_id=session_id,
            )
            return

        if path == "/api/caregiver-reset":
            if not self.require_caregiver(session_id):
                return
            user_id = session_user_id(session)
            database.clear_caregiver_messages_and_alerts(user_id)
            self.send_json(
                200,
                {
                    "ok": True,
                    "dashboard": dashboard_payload(user_id),
                },
                session_id=session_id,
            )
            return

        if path == "/api/patient-caregiver-chat":
            if not self.require_auth(session_id):
                return
            body = self.read_json_body()
            sender = str(body.get("sender", "")).strip().lower()
            message = str(body.get("message", "")).strip()
            if sender not in {"patient", "caregiver"}:
                self.send_json(
                    400,
                    {"error": "Choose patient or caregiver as the sender."},
                    session_id=session_id,
                )
                return
            if sender == "caregiver" and not self.require_caregiver(session_id):
                return
            if not message:
                self.send_json(
                    400,
                    {"error": "Please type a message first."},
                    session_id=session_id,
                )
                return
            user_id = session_user_id(session)
            saved = database.add_patient_caregiver_message(
                sender,
                message,
                user_id=user_id,
            )
            self.send_json(
                200,
                {
                    "message": saved,
                    "messages": database.list_patient_caregiver_messages(
                        limit=80,
                        user_id=user_id,
                    ),
                },
                session_id=session_id,
            )
            return

        if path == "/api/dataset-clear":
            body = self.read_json_body()
            account = session.get("account")
            if account is None:
                self.send_json(
                    401,
                    {"error": "Please sign in first."},
                    session_id=session_id,
                )
                return
            if not database.verify_caregiver_password(
                account["username"],
                str(body.get("password", "")),
            ):
                self.send_json(
                    401,
                    {"error": "Incorrect caregiver password."},
                    session_id=session_id,
                )
                return
            if body.get("confirm") is not True:
                self.send_json(
                    400,
                    {"error": "Final confirmation is required."},
                    session_id=session_id,
                )
                return
            user_id = session_user_id(session)
            database.clear_patient_dataset(user_id)
            clear_patient_session_state(user_id)
            session["dataset_authenticated"] = True
            self.send_json(
                200,
                {
                    "ok": True,
                    "dataset": dataset_payload(user_id),
                    "dashboard": dashboard_payload(user_id),
                    "currentTask": None,
                },
                session_id=session_id,
            )
            return

        if path == "/api/chat":
            body = self.read_json_body()
            user_message = str(body.get("message", "")).strip()
            target_language = normalize_language_code(body.get("language"))
            if not user_message:
                self.send_json(
                    400,
                    {"error": "Please type a message first."},
                    session_id=session_id,
                )
                return
            user_id = session_user_id(session)
            try:
                result = patient_response(session, user_message, target_language, user_id)
            except Exception as error:
                answer = ai_service_error_message(error, audience="patient")
                print(f"AURA patient AI error: {type(error).__name__}: {error}")
                self.send_json(
                    503,
                    {"error": answer},
                    session_id=session_id,
                )
                return
            history = session.setdefault("patient_chat_history", [])
            history.extend(
                [
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": result["answer"]},
                ]
            )
            session["patient_chat_history"] = history[-24:]
            self.send_json(
                200,
                {
                    "answer": result["answer"],
                    "alert": result["alert"],
                    "currentTask": get_current_task(session, user_id)[0],
                    "currentInstruction": current_instruction(session, user_id),
                    "dueTask": due_routine(user_id),
                    "clock": test_clock.state(),
                    "dashboard": dashboard_payload(user_id)
                    if session.get("caregiver_authenticated")
                    else None,
                },
                session_id=session_id,
            )
            return

        self.send_json(404, {"error": "Unknown endpoint."}, session_id=session_id)


def run() -> None:
    database.init_db()
    monitor_stop = Event()
    monitor_thread = Thread(
        target=monitor_missed_tasks,
        args=(monitor_stop,),
        name="aura-missed-task-monitor",
        daemon=True,
    )
    monitor_thread.start()
    server = ThreadingHTTPServer((HOST, PORT), AuraWebHandler)
    print(f"AURA web app running at http://{HOST}:{PORT}")
    print(f"SQLite database: {database.DB_PATH}")
    try:
        server.serve_forever()
    finally:
        monitor_stop.set()
        server.server_close()


if __name__ == "__main__":
    run()

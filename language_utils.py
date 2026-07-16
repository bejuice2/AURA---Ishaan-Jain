from __future__ import annotations

import json


SUPPORTED_LANGUAGES = [
    {"code": "auto", "name": "Auto detect", "native": "Auto detect"},
    {"code": "en-US", "name": "English", "native": "English"},
    {"code": "es-ES", "name": "Spanish", "native": "Espanol"},
    {"code": "es-MX", "name": "Spanish (Mexico)", "native": "Espanol (Mexico)"},
    {"code": "fr-FR", "name": "French", "native": "Francais"},
    {"code": "de-DE", "name": "German", "native": "Deutsch"},
    {"code": "it-IT", "name": "Italian", "native": "Italiano"},
    {"code": "pt-BR", "name": "Portuguese (Brazil)", "native": "Portugues (Brasil)"},
    {"code": "pt-PT", "name": "Portuguese", "native": "Portugues"},
    {"code": "zh-CN", "name": "Chinese (Simplified)", "native": "Chinese Simplified"},
    {"code": "zh-TW", "name": "Chinese (Traditional)", "native": "Chinese Traditional"},
    {"code": "ja-JP", "name": "Japanese", "native": "Japanese"},
    {"code": "ko-KR", "name": "Korean", "native": "Korean"},
    {"code": "hi-IN", "name": "Hindi", "native": "Hindi"},
    {"code": "bn-BD", "name": "Bengali", "native": "Bengali"},
    {"code": "ur-PK", "name": "Urdu", "native": "Urdu"},
    {"code": "ar-SA", "name": "Arabic", "native": "Arabic"},
    {"code": "he-IL", "name": "Hebrew", "native": "Hebrew"},
    {"code": "ru-RU", "name": "Russian", "native": "Russian"},
    {"code": "uk-UA", "name": "Ukrainian", "native": "Ukrainian"},
    {"code": "pl-PL", "name": "Polish", "native": "Polski"},
    {"code": "nl-NL", "name": "Dutch", "native": "Nederlands"},
    {"code": "sv-SE", "name": "Swedish", "native": "Svenska"},
    {"code": "no-NO", "name": "Norwegian", "native": "Norsk"},
    {"code": "da-DK", "name": "Danish", "native": "Dansk"},
    {"code": "fi-FI", "name": "Finnish", "native": "Suomi"},
    {"code": "el-GR", "name": "Greek", "native": "Greek"},
    {"code": "tr-TR", "name": "Turkish", "native": "Turkce"},
    {"code": "vi-VN", "name": "Vietnamese", "native": "Tieng Viet"},
    {"code": "th-TH", "name": "Thai", "native": "Thai"},
    {"code": "id-ID", "name": "Indonesian", "native": "Bahasa Indonesia"},
    {"code": "ms-MY", "name": "Malay", "native": "Bahasa Melayu"},
    {"code": "tl-PH", "name": "Filipino", "native": "Filipino"},
    {"code": "fa-IR", "name": "Persian", "native": "Persian"},
    {"code": "ro-RO", "name": "Romanian", "native": "Romana"},
    {"code": "cs-CZ", "name": "Czech", "native": "Cestina"},
    {"code": "hu-HU", "name": "Hungarian", "native": "Magyar"},
    {"code": "sw-KE", "name": "Swahili", "native": "Kiswahili"},
]

LANGUAGE_BY_CODE = {language["code"]: language for language in SUPPORTED_LANGUAGES}


def get_supported_languages() -> list[dict]:
    return SUPPORTED_LANGUAGES


def normalize_language_code(code: str | None) -> str:
    if not code:
        return "auto"
    clean_code = str(code).strip()
    if clean_code in LANGUAGE_BY_CODE:
        return clean_code
    short_code = clean_code.split("-", 1)[0].lower()
    for language_code in LANGUAGE_BY_CODE:
        if language_code.lower().split("-", 1)[0] == short_code:
            return language_code
    return "auto"


def language_name(code: str | None) -> str:
    normalized = normalize_language_code(code)
    return LANGUAGE_BY_CODE.get(normalized, LANGUAGE_BY_CODE["auto"])["name"]


def localize_text(
    client,
    model: str,
    assistant_text: str,
    user_message: str,
    target_language: str | None = None,
) -> str:
    normalized_language = normalize_language_code(target_language)
    selected_language = language_name(normalized_language)
    prompt = """
You are AURA's language tool.

Rewrite the assistant text for the correct language.

Rules:
- If target_language is Auto detect, match the language of the user's message.
- If the user requests another language, use the requested language.
- If target_language is a specific language, use that language unless the user explicitly requests a different one.
- If the final language is English and the text is already English, return it unchanged.
- Keep the meaning, tone, and brevity.
- Keep names, numbers, task labels, and safety wording intact.
- Keep medical and emergency wording careful and accurate.
- Return only the rewritten text. No explanation.
"""

    try:
        response = client.responses.create(
            model=model,
            instructions=prompt,
            input=json.dumps(
                {
                    "user_message": user_message,
                    "assistant_text": assistant_text,
                    "target_language": selected_language,
                    "target_language_code": normalized_language,
                },
                ensure_ascii=False,
            ),
        )
        output = response.output_text.strip()
        return output or assistant_text
    except Exception:
        return assistant_text


def localize_patient_text(
    client,
    model: str,
    assistant_text: str,
    user_message: str,
    target_language: str | None = None,
) -> str:
    normalized_language = normalize_language_code(target_language)
    selected_language = language_name(normalized_language)
    prompt = """
You are AURA's patient phrasing tool.

Rewrite only the approved assistant text for an elderly patient routine assistant.
The app has already chosen the action. Do not choose a new action.

Rules:
- If target_language is Auto detect, match the language of the user's message.
- If the user requests another language, use the requested language.
- If target_language is a specific language, use that language unless the user explicitly requests another one.
- Use very short sentences.
- Use simple words.
- Give only one instruction at a time.
- Keep a calm, supportive tone.
- Do not add explanations.
- Do not mention dementia.
- Do not diagnose anything.
- Do not give medical advice.
- Do not change medication instructions.
- Keep names, numbers, task labels, and emergency wording accurate.
- Preserve the meaning of the approved text.
- Return only the rewritten text. No explanation.
"""

    try:
        response = client.responses.create(
            model=model,
            instructions=prompt,
            input=json.dumps(
                {
                    "user_message": user_message,
                    "approved_assistant_text": assistant_text,
                    "target_language": selected_language,
                    "target_language_code": normalized_language,
                },
                ensure_ascii=False,
            ),
        )
        output = response.output_text.strip()
        return output or assistant_text
    except Exception:
        return assistant_text

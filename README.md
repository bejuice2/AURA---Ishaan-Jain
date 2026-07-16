# AURA Local Web App

AURA is a local AI-assisted daily routine helper for elderly patients and caregivers. It supports sign in, short patient conversations, persistent routine tracking, per-user patient datasets, caregiver insights, caregiver chat, alerts, and CSV export.

AURA is not a medical device. It does not diagnose, treat, replace caregivers, replace clinicians, or replace emergency services.

## Run It

Create a private `.env` from the safe template before starting AURA:

```powershell
Copy-Item .env.example .env
```

Replace every placeholder in `.env` with private local values. The admin username
and password are configured with `AURA_ADMIN_USERNAME` and `AURA_ADMIN_PASSWORD`.
The real `.env`, SQLite databases, exported datasets, and private-key files are
excluded by the repository `.gitignore`.

```powershell
cd "C:\Users\ishaa\Downloads\AIF\AI AGENT"
python -m pip install -r requirements.txt
python web_app.py
```

Open:

```text
http://127.0.0.1:8000
```

To view all account datasets in a separate local app, run:

```powershell
python dataset_viewer_app.py
```

Open:

```text
http://127.0.0.1:8001
```

The dataset viewer reads directly from `aura.sqlite3`.

The caregiver password is part of sign in. Enter it when you create the account or log in.
Existing accounts that did not store a caregiver password are removed during startup migration.

## Language Tool

The top bar has a language selector. `Auto detect` replies in the language the user types. Choosing a specific language makes AURA reply in that language unless the user asks for another language.

The language tool supports many common languages and also sets the browser speech recognition and spoken reply language when the browser supports those features.

Patient chat uses rule-based task logic first. A patient-specific phrasing helper can then simplify and translate the approved response, but it does not choose tasks, change actions, or add medical guidance.

## Test Clock

The top of the app has a testing clock. It is for local testing only.

- `Speed` changes how quickly AURA's schedule time moves.
- `Custom` lets you type a custom speed amount and apply it with `Set Speed`.
- `Paused` freezes the testing clock.
- `Reset Time` returns AURA to the real current time at `1x`.

The testing clock is used for schedule checks, missed-task detection, task dates, alerts, and completion timing.

## Changed Files

- `web_app.py`: local HTTP API, patient task flow, caregiver routes, dataset access, alerts, CSV export.
- `dataset_viewer_app.py`: separate local app for viewing all account datasets from SQLite.
- `language_utils.py`: supported languages, caregiver localization, and patient-safe phrasing helper.
- `database.py`: SQLite schema, login accounts, per-user routines and datasets, persistence helpers, CSV export.
- `scoring.py`: raw and adjusted performance scoring.
- `insights.py`: dashboard analytics, trends, and automatic summaries.
- `test_clock.py`: adjustable testing clock used by schedule and task timing logic.
- `static/index.html`: sign in, patient/caregiver tab UI, routine form, dataset view, dashboard, alerts, export.
- `static/app.js`: sign in, logout, patient chat, caregiver auth, dashboard rendering, routine saving/deleting, dataset viewing/clearing, testing clock controls, and language selection.
- `static/styles.css`: sign in, tab layout, language selector, caregiver dashboard, dataset table, routine, insight, and testing clock styling.
- `README.md`: documentation.

## Database

SQLite database:

```text
aura.sqlite3
```

Tables:

- `routines`: per-user task schedule, difficulty, importance, steps, active status.
- `task_attempts`: patient performance records for every task attempt.
- `caregiver_notes`: caregiver notes for future extension.
- `alerts`: caregiver alerts and text status.
- `summaries`: generated summaries for future extension.
- `caregiver_chat`: caregiver questions and AURA answers.
- `accounts`: username, password hash, caregiver password hash, patient name, and caregiver name.
- `auth_tokens`: saved-device login tokens.

Passwords are stored as salted PBKDF2 hashes. Saved device login uses an HTTP-only cookie and a SQLite token record.

Each account uses its username as the `user_id`, so task attempts, alerts, caregiver chat, summaries, caregiver notes, and routines are separated by logged-in user.

`task_attempts` stores:

`user_id`, `date`, `day_of_week`, `time_of_day`, `scheduled_time`, `task_name`, `task_category`, `task_difficulty`, `task_importance`, `completed`, `reminders_needed`, `help_requested`, `confusion_flag`, `time_to_complete`, `raw_performance_score`, `adjusted_performance_score`, `caregiver_alert`, and `notes`.

## Scoring

Raw score starts from:

- `100` if marked complete.
- `35` if not complete.

Penalties:

- `-8` per reminder, up to 5 reminders.
- `-18` if help was requested.
- `-15` for a possible confusion flag.
- Time penalty if completion takes longer than expected.

Adjusted score modifies raw score by task difficulty:

- Easy tasks are adjusted downward.
- Hard tasks are adjusted upward.

Caregiver analytics use adjusted performance so easy and hard tasks are not treated the same.

## Insights

The caregiver dashboard computes:

- Today's activity.
- Completed and missed tasks.
- Help requests.
- Possible confusion flags.
- Caregiver alerts.
- Raw and adjusted performance.
- Best and worst time of day.
- Best and worst day of week.
- Hardest category.
- Hardest task.
- Recent trend.
- Suggested caregiver follow-up.

The caregiver page uses internal tabs for schedule, performance insights, AURA update, recent activity, and dataset.
The caregiver `Reset` button clears caregiver chat messages and safety alerts only. It does not delete routines or task performance history.

The caregiver `Dataset` tab requires the caregiver password again. It shows records directly from SQLite, including date, scheduled time, task, status, reminders, help requests, possible confusion flags, raw score, adjusted score, and notes.

The `Clear Dataset` button permanently deletes the logged-in patient's task history, alerts, caregiver notes, summaries, and caregiver chat after a warning and caregiver password confirmation. It does not delete scheduled routines.

Caregiver chat answers only from stored records.

## Routines

Caregivers can create routines in the caregiver tab.
Each routine has a `Delete` button that permanently removes that scheduled task for the logged-in user.

Each routine stores:

- `task_id`
- `task_name`
- `task_category`
- `task_difficulty`
- `task_importance`
- `scheduled_time`
- `time_of_day`
- `repeat_schedule`
- step-by-step instructions
- active status

The patient only sees one step at a time.

## Alerts

Alerts are generated for:

- Important missed tasks.
- Multiple reminders.
- Help requests.
- Possible confusion flags.
- Emergency phrases.

Emergency phrasing tells the patient to contact the caregiver or emergency services.

## Text Alerts

Safety alerts appear in the caregiver interface automatically. Caregivers can add
an optional phone number while creating an account or logging in. The number is
stored for that account and can be enabled or disabled from `Reminders`.

To send real SMS texts, add the Twilio service credentials to `.env`:

```text
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_FROM_PHONE=+15555555555
```

The caregiver phone is entered in AURA, not `.env`. When Twilio is unavailable or
text messages are disabled, AURA still records emergency and missed-task alerts
in SQLite and shows them in the caregiver interface.

## Export

The caregiver tab has an `Export CSV` link. It exports:

```text
aura_task_attempts.csv
```

## Notes

Keep `OPENAI_API_KEY` in `.env`. Do not put it in browser files.
Never put real API keys, Twilio credentials, admin credentials, patient exports,
or SQLite database files in `.env.example` or any committed source file.

The default OpenAI model is `gpt-5.5-pro`. To use a different model while testing, add this to `.env`:

```text
AURA_MODEL=gpt-5.5-pro
```

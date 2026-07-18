# AURA

AURA is an AI-assisted daily routine application for patients and caregivers. It
provides patient task guidance, caregiver alerts, routine management, persistent
per-account performance datasets, caregiver insights, direct chat, CSV export,
and optional SMS notifications.

> AURA is a demonstration prototype, not a medical device. It does not diagnose,
> treat, replace clinicians or caregivers, or replace emergency services. Use
> synthetic data for public demonstrations. Do not use this deployment for real
> patient information without an appropriate security, privacy, legal, and
> compliance review.

## Architecture

- Frontend: plain HTML, CSS, and JavaScript in `static/`.
- Backend: Python HTTP application adapted to Flask/WSGI for production.
- Production server: Waitress.
- AI: OpenAI API, called only from the backend.
- Persistence: one SQLite database under `AURA_DATA_DIR`.
- Hosting: one Render Python web service with one persistent disk.

The frontend and backend are served from the same origin. No separate frontend
host, CORS configuration, or managed database is required for this architecture.
Keep the Render service at one instance while it uses SQLite.

## Local Setup

Requirements: Python 3.12 and an OpenAI API key.

```powershell
Copy-Item .env.example .env
python -m pip install -r requirements.txt
python web_app.py
```

Set private values in `.env`, then open `http://127.0.0.1:8000`.

The separate local administrator dataset viewer can be started with:

```powershell
python dataset_viewer_app.py
```

It is available at `http://127.0.0.1:8001`. This viewer is local-only and is not
the Render production entry point.

## Production Commands

Build:

```text
pip install -r requirements.txt
```

Start:

```text
python serve.py
```

`serve.py` validates production configuration, binds Waitress to `0.0.0.0`, and
uses the hosting platform's `PORT` environment variable.

## Environment Variables

Required in production:

| Name | Purpose |
| --- | --- |
| `OPENAI_API_KEY` | Private OpenAI API credential. |
| `AURA_ADMIN_USERNAME` | Private AURA administrator username. |
| `AURA_ADMIN_PASSWORD` | Strong private AURA administrator password. |
| `AURA_ENV` | Set to `production` on Render. |
| `AURA_DATA_DIR` | Set to the persistent disk path, `/var/data`. |
| `AURA_TIMEZONE` | IANA timezone, such as `America/Chicago`. |

Production settings included by `render.yaml`:

| Name | Default |
| --- | --- |
| `PYTHON_VERSION` | `3.12.11` |
| `AURA_PUBLIC_DEMO` | `true` |
| `AURA_CAREGIVER_MODEL` | `gpt-5-mini` |
| `AURA_PATIENT_MODEL` | `gpt-5-mini` |
| `AURA_OPENAI_TIMEOUT` | `30` |
| `AURA_OPENAI_RETRIES` | `5` |
| `AURA_TASK_GRACE_PERIOD_MINUTES` | `30` |

Optional settings:

| Name | Purpose |
| --- | --- |
| `AURA_ALLOWED_ORIGINS` | Additional trusted origins. Leave unset for same-origin deployment. |
| `AURA_MODEL` | Legacy caregiver-model fallback. |
| `AURA_CAREGIVER_MODEL_FALLBACKS` | Comma-separated caregiver model fallbacks. |
| `AURA_PATIENT_MODEL_FALLBACKS` | Comma-separated patient model fallbacks. |
| `TWILIO_ACCOUNT_SID` | Twilio account identifier. |
| `TWILIO_AUTH_TOKEN` | Twilio secret credential. |
| `TWILIO_FROM_PHONE` | Twilio sender phone number. |

Set all three Twilio variables or none. Render supplies `PORT`; do not hardcode it.
Never commit `.env` or enter secret values into `render.yaml`.

## Data Storage

AURA stores accounts, salted password hashes, authentication tokens, routines,
task attempts, alerts, summaries, chats, and caregiver notes in SQLite. Each
account's records are separated by its username-based `user_id`.

Locally, the default database is `aura.sqlite3` in the project directory. On
Render, `AURA_DATA_DIR=/var/data` places it on the attached persistent disk.
Only files under that mount path survive deploys and restarts.

Do not commit or upload the local SQLite database. A public demonstration should
start with an empty database and synthetic accounts. Use the caregiver CSV export
for deliberate, non-sensitive backups. A persistent disk disables normal
zero-downtime deploys and cannot be shared by horizontally scaled instances.

## Deploy To Render

The repository includes one Render Blueprint, `render.yaml`. It declares a paid
Starter web service, a 1 GB persistent disk, one application instance, a health
check, production commands, and non-secret environment settings.

1. Push the reviewed repository to GitHub without `.env`, `.env.admin`, databases,
   exports, logs, credentials, caches, or patient data.
2. Sign in to the Render Dashboard with GitHub.
3. Select **New**, then **Blueprint**.
4. Connect the GitHub repository containing this file.
5. Review the declared Starter service and persistent disk cost.
6. Enter `OPENAI_API_KEY`, `AURA_ADMIN_USERNAME`, and `AURA_ADMIN_PASSWORD` when
   Render prompts for the `sync: false` variables. Do not paste them into source.
7. Apply the Blueprint and watch the deployment logs.
8. Open the generated `https://<service-name>.onrender.com` address.
9. Confirm `/health` returns an `ok` status and the database is available.

To enable Twilio later, open the service's **Environment** page, add all three
Twilio variables, and select **Save and deploy**.

## Verify A Deployment

Use synthetic data and verify:

1. The welcome, login, patient, and caregiver screens load over HTTPS.
2. A demonstration account can be created and restored after refresh.
3. Routines can be created and deleted.
4. Patient Help creates an immediate caregiver alert and notification badge.
5. Patient-caregiver chat and AURA chat work.
6. Dataset records remain after a service restart or redeploy.
7. CSV export downloads correctly.
8. `/health` reports `{"status":"ok","database":"available"}`.
9. Browser developer tools show no failed static assets or API requests.

## Future Deployments

`autoDeployTrigger: commit` causes every commit pushed to the linked branch to
trigger a Render build and deployment. A failed build leaves the previous working
deployment in place. Review database compatibility before deploying schema changes.

## Security

The root `.gitignore` excludes environment files, virtual environments, UV caches,
SQLite databases and sidecars, exports, uploads, logs, private keys, credentials,
and common editor files. `.env.example` is intentionally retained and contains
placeholders only.

Before every push, inspect:

```powershell
git status --short
git diff --check
git check-ignore -v .env .env.admin aura.sqlite3 .venv .uv-cache
```

Do not upload real patient records or claim that this prototype is medically or
legally compliant.

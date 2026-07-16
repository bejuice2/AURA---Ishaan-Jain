from __future__ import annotations

import csv
import html
import io
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlencode, urlparse

import database


HOST = "127.0.0.1"
PORT = 8001


def esc(value: object) -> str:
    if value is None:
        return ""
    return html.escape(str(value), quote=True)


def fetch_accounts() -> list[dict]:
    with database.connect() as db:
        rows = db.execute(
            """
            SELECT
                accounts.username,
                accounts.patient_name,
                accounts.caregiver_name,
                accounts.created_at,
                COUNT(task_attempts.attempt_id) AS records,
                ROUND(AVG(task_attempts.adjusted_performance_score), 1) AS adjusted_average
            FROM accounts
            LEFT JOIN task_attempts ON task_attempts.user_id = accounts.username
            GROUP BY accounts.username
            ORDER BY accounts.patient_name, accounts.username
            """
        ).fetchall()
        accounts = database.rows_to_dicts(rows)

        legacy_count = db.execute(
            """
            SELECT COUNT(*) FROM task_attempts
            WHERE user_id = ? AND user_id NOT IN (SELECT username FROM accounts)
            """,
            (database.DEFAULT_USER_ID,),
        ).fetchone()[0]
        if legacy_count:
            accounts.append(
                {
                    "username": database.DEFAULT_USER_ID,
                    "patient_name": "Legacy patient-1",
                    "caregiver_name": "Legacy data",
                    "created_at": "",
                    "records": legacy_count,
                    "adjusted_average": None,
                }
            )
        return accounts


def fetch_dataset(user_id: str) -> dict:
    return {
        "summary": database.dataset_summary(user_id),
        "records": database.list_attempts(limit=5000, user_id=user_id),
        "routines": database.list_routines(user_id=user_id),
        "alerts": database.list_alerts(limit=100, user_id=user_id),
    }


def status_for(record: dict) -> str:
    if record.get("completed"):
        return "Marked complete"
    if record.get("missed"):
        return "Missed"
    return "Started"


def yes_no(value: object) -> str:
    return "Yes" if value else "No"


def metric(label: str, value: object) -> str:
    return f"""
    <section class="metric">
      <strong>{esc(value if value is not None else "No data")}</strong>
      <span>{esc(label)}</span>
    </section>
    """


def account_link(account: dict, selected: str) -> str:
    username = str(account["username"])
    href = "/?" + urlencode({"user_id": username})
    selected_class = " is-active" if username == selected else ""
    return f"""
    <a class="account-card{selected_class}" href="{href}">
      <strong>{esc(account.get("patient_name") or username)}</strong>
      <span>{esc(account.get("caregiver_name") or "Caregiver not set")}</span>
      <small>{esc(account.get("records", 0))} records</small>
    </a>
    """


def render_rows(records: list[dict]) -> str:
    if not records:
        return '<tr><td colspan="12">No task records found for this account.</td></tr>'

    rows = []
    for record in records:
        rows.append(
            f"""
            <tr>
              <td>{esc(record.get("date"))}</td>
              <td>{esc(record.get("day_of_week"))}</td>
              <td>{esc(record.get("scheduled_time"))}</td>
              <td>{esc(record.get("time_of_day"))}</td>
              <td>{esc(record.get("task_name"))}</td>
              <td>{esc(record.get("task_category"))}</td>
              <td>{esc(status_for(record))}</td>
              <td>{esc(record.get("reminders_needed"))}</td>
              <td>{esc(yes_no(record.get("help_requested")))}</td>
              <td>{esc(yes_no(record.get("confusion_flag")))}</td>
              <td>{esc(record.get("adjusted_performance_score"))}</td>
              <td>{esc(record.get("notes"))}</td>
            </tr>
            """
        )
    return "\n".join(rows)


def render_app(selected_user_id: str | None = None) -> bytes:
    database.init_db()
    accounts = fetch_accounts()
    if not selected_user_id and accounts:
        selected_user_id = accounts[0]["username"]

    dataset = fetch_dataset(selected_user_id) if selected_user_id else {
        "summary": {},
        "records": [],
        "routines": [],
        "alerts": [],
    }
    summary = dataset["summary"]
    records = dataset["records"]
    selected_account = next(
        (account for account in accounts if account["username"] == selected_user_id),
        None,
    )
    export_href = "/export?" + urlencode({"user_id": selected_user_id or ""})

    page = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>AURA Dataset Viewer</title>
    <style>
      :root {{
        --bg: #f6f7f4;
        --panel: #ffffff;
        --ink: #1d2523;
        --muted: #66716d;
        --line: #dfe5df;
        --brand: #2f6f73;
        --brand-dark: #24575a;
        --accent: #c86f42;
        --shadow: 0 18px 55px rgba(29, 37, 35, 0.11);
      }}
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0;
        background: var(--bg);
        color: var(--ink);
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }}
      .shell {{
        display: grid;
        grid-template-columns: 280px minmax(0, 1fr);
        min-height: 100vh;
      }}
      aside {{
        padding: 22px;
        border-right: 1px solid var(--line);
        background: #ffffff;
      }}
      main {{ padding: 26px; min-width: 0; }}
      h1, h2, h3, p {{ margin-top: 0; }}
      h1 {{ margin-bottom: 6px; font-size: 1.55rem; }}
      h2 {{ margin-bottom: 14px; font-size: 1.2rem; }}
      .source {{
        margin: 0 0 18px;
        color: var(--muted);
        font-size: 0.88rem;
        overflow-wrap: anywhere;
      }}
      .account-list {{ display: grid; gap: 9px; }}
      .account-card {{
        display: grid;
        gap: 4px;
        padding: 12px;
        border: 1px solid var(--line);
        border-radius: 8px;
        color: inherit;
        text-decoration: none;
        background: #f7faf8;
      }}
      .account-card.is-active {{
        border-color: var(--brand);
        background: #edf6f4;
      }}
      .account-card strong {{ color: var(--brand-dark); }}
      .account-card span, .account-card small {{ color: var(--muted); }}
      .header {{
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 16px;
        margin-bottom: 16px;
      }}
      .export {{
        min-height: 42px;
        padding: 10px 14px;
        border-radius: 8px;
        background: var(--brand);
        color: #ffffff;
        font-weight: 800;
        text-decoration: none;
      }}
      .metrics {{
        display: grid;
        grid-template-columns: repeat(6, minmax(0, 1fr));
        gap: 10px;
        margin-bottom: 16px;
      }}
      .metric {{
        min-height: 86px;
        padding: 14px;
        border: 1px solid var(--line);
        border-radius: 8px;
        background: var(--panel);
        box-shadow: 0 8px 28px rgba(29, 37, 35, 0.06);
      }}
      .metric strong {{
        display: block;
        margin-bottom: 7px;
        color: var(--brand-dark);
        font-size: 1.55rem;
        line-height: 1;
      }}
      .metric span {{ color: var(--muted); font-size: 0.86rem; }}
      .panel {{
        border: 1px solid var(--line);
        border-radius: 8px;
        background: var(--panel);
        box-shadow: var(--shadow);
        overflow: hidden;
      }}
      .table-wrap {{ max-height: 62vh; overflow: auto; }}
      table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
      th, td {{
        padding: 10px 12px;
        border-bottom: 1px solid var(--line);
        text-align: left;
        vertical-align: top;
      }}
      th {{
        position: sticky;
        top: 0;
        background: #f7faf8;
        color: var(--brand-dark);
        font-size: 0.74rem;
        text-transform: uppercase;
        z-index: 1;
      }}
      td:last-child {{ min-width: 260px; color: var(--muted); }}
      .empty {{
        padding: 18px;
        color: var(--muted);
      }}
      @media (max-width: 980px) {{
        .shell {{ grid-template-columns: 1fr; }}
        aside {{ border-right: 0; border-bottom: 1px solid var(--line); }}
        .metrics {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
        .header {{ flex-direction: column; }}
      }}
    </style>
  </head>
  <body>
    <div class="shell">
      <aside>
        <h1>AURA Dataset Viewer</h1>
        <p class="source">SQLite file: {esc(database.DB_PATH)}</p>
        <h2>Accounts</h2>
        <div class="account-list">
          {"".join(account_link(account, selected_user_id or "") for account in accounts) or '<p class="empty">No accounts found.</p>'}
        </div>
      </aside>
      <main>
        <div class="header">
          <div>
            <h1>{esc((selected_account or {}).get("patient_name") or selected_user_id or "No account selected")}</h1>
            <p class="source">User dataset key: {esc(selected_user_id or "")}</p>
          </div>
          <a class="export" href="{export_href}">Export CSV</a>
        </div>
        <div class="metrics">
          {metric("Records", summary.get("total", 0))}
          {metric("Marked complete", summary.get("completed", 0))}
          {metric("Missed", summary.get("missed", 0))}
          {metric("Help requests", summary.get("help_requests", 0))}
          {metric("Possible confusion", summary.get("confusion_flags", 0))}
          {metric("Adjusted average", summary.get("adjusted_average"))}
        </div>
        <section class="panel">
          <div class="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Day</th>
                  <th>Time</th>
                  <th>Part of day</th>
                  <th>Task</th>
                  <th>Category</th>
                  <th>Status</th>
                  <th>Reminders</th>
                  <th>Help</th>
                  <th>Possible confusion</th>
                  <th>Adjusted score</th>
                  <th>Notes</th>
                </tr>
              </thead>
              <tbody>
                {render_rows(records)}
              </tbody>
            </table>
          </div>
        </section>
      </main>
    </div>
  </body>
</html>"""
    return page.encode("utf-8")


def export_csv(user_id: str) -> bytes:
    dataset = fetch_dataset(user_id)
    records = dataset["records"]
    output = io.StringIO()
    headers = [
        "user_id",
        "date",
        "day_of_week",
        "time_of_day",
        "scheduled_time",
        "task_name",
        "task_category",
        "task_difficulty",
        "task_importance",
        "completed",
        "missed",
        "reminders_needed",
        "help_requested",
        "confusion_flag",
        "time_to_complete",
        "raw_performance_score",
        "adjusted_performance_score",
        "caregiver_alert",
        "notes",
    ]
    writer = csv.DictWriter(output, fieldnames=headers)
    writer.writeheader()
    for record in records:
        writer.writerow({header: record.get(header, "") for header in headers})
    return output.getvalue().encode("utf-8")


class DatasetViewerHandler(BaseHTTPRequestHandler):
    server_version = "AuraDatasetViewer/1.0"

    def log_message(self, format: str, *args: object) -> None:
        return

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        user_id = params.get("user_id", [""])[0]

        if parsed.path == "/export":
            body = export_csv(user_id)
            self.send_response(200)
            self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.send_header(
                "Content-Disposition",
                f'attachment; filename="aura_dataset_{user_id or "all"}.csv"',
            )
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if parsed.path != "/":
            self.send_error(404)
            return

        body = render_app(user_id or None)
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run() -> None:
    database.init_db()
    server = ThreadingHTTPServer((HOST, PORT), DatasetViewerHandler)
    print(f"AURA dataset viewer running at http://{HOST}:{PORT}")
    print(f"SQLite database: {database.DB_PATH}")
    server.serve_forever()


if __name__ == "__main__":
    run()

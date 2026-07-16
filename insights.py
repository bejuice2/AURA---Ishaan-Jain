from __future__ import annotations

from collections import defaultdict
from statistics import mean


def average(items: list[float]) -> float | None:
    if not items:
        return None
    return round(mean(items), 1)


def group_average(attempts: list[dict], key: str) -> dict[str, float]:
    groups: dict[str, list[float]] = defaultdict(list)
    for attempt in attempts:
        value = attempt.get(key)
        score = attempt.get("adjusted_performance_score")
        if value and score is not None:
            groups[str(value)].append(float(score))
    return {name: average(scores) for name, scores in groups.items()}


def best_and_worst(grouped_scores: dict[str, float]) -> tuple[str | None, str | None]:
    if not grouped_scores:
        return None, None
    best = max(grouped_scores, key=grouped_scores.get)
    worst = min(grouped_scores, key=grouped_scores.get)
    return best, worst


def completion_counts(attempts: list[dict]) -> dict:
    return {
        "total": len(attempts),
        "completed": sum(1 for attempt in attempts if attempt.get("completed")),
        "missed": sum(1 for attempt in attempts if attempt.get("missed")),
        "helpRequests": sum(1 for attempt in attempts if attempt.get("help_requested")),
        "confusionFlags": sum(1 for attempt in attempts if attempt.get("confusion_flag")),
        "caregiverAlerts": sum(1 for attempt in attempts if attempt.get("caregiver_alert")),
    }


def percentage(count: int | float, total: int) -> str:
    if total <= 0:
        return "No data"
    return f"{(float(count) / total) * 100:.1f}%"


def score_average(attempts: list[dict], key: str) -> float | None:
    return average(
        [
            float(attempt[key])
            for attempt in attempts
            if attempt.get(key) is not None
        ]
    )


def attempt_needs_support(attempt: dict) -> bool:
    adjusted_score = attempt.get("adjusted_performance_score")
    return bool(
        attempt.get("missed")
        or int(attempt.get("reminders_needed") or 0) >= 2
        or attempt.get("help_requested")
        or attempt.get("confusion_flag")
        or (adjusted_score is not None and float(adjusted_score) < 60)
    )


def detail_row(label: str, attempts: list[dict]) -> dict:
    total = len(attempts)
    completed = sum(1 for attempt in attempts if attempt.get("completed"))
    missed = sum(1 for attempt in attempts if attempt.get("missed"))
    alerts = sum(1 for attempt in attempts if attempt.get("caregiver_alert"))
    help_requests = sum(1 for attempt in attempts if attempt.get("help_requested"))
    confusion = sum(1 for attempt in attempts if attempt.get("confusion_flag"))
    support = sum(1 for attempt in attempts if attempt_needs_support(attempt))
    reminders = sum(int(attempt.get("reminders_needed") or 0) for attempt in attempts)
    adjusted = score_average(attempts, "adjusted_performance_score")
    raw = score_average(attempts, "raw_performance_score")
    avg_difficulty = average(
        [float(attempt.get("task_difficulty") or 0) for attempt in attempts]
    )

    if total < 3:
        interpretation = "Early signal based on a limited number of attempts."
    elif adjusted is not None and adjusted >= 80 and completed / total >= 0.8:
        interpretation = "The current records indicate comparatively strong performance."
    elif adjusted is not None and (adjusted < 60 or support / total >= 0.6):
        interpretation = "The data suggests this area may need additional caregiver review."
    else:
        interpretation = "The current records indicate mixed performance and support needs."

    return {
        "label": label,
        "attempts": total,
        "avgPerformance": adjusted,
        "avgRawPerformance": raw,
        "avgDifficulty": avg_difficulty,
        "completionRate": percentage(completed, total),
        "missedRate": percentage(missed, total),
        "alertRate": percentage(alerts, total),
        "helpRate": percentage(help_requests, total),
        "struggleRate": percentage(support, total),
        "avgReminders": round(reminders / total, 2) if total else None,
        "confusionFlags": confusion,
        "interpretation": interpretation,
    }


def grouped_detail_rows(
    attempts: list[dict],
    key: str,
    preferred_order: list[str] | None = None,
) -> list[dict]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for attempt in attempts:
        value = attempt.get(key)
        if value:
            groups[str(value)].append(attempt)
    labels = list(groups)
    if preferred_order:
        order = {label: index for index, label in enumerate(preferred_order)}
        labels.sort(key=lambda label: (order.get(label, len(order)), label))
    else:
        labels.sort()
    return [detail_row(label, groups[label]) for label in labels]


def difficulty_detail_rows(attempts: list[dict]) -> list[dict]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for attempt in attempts:
        try:
            difficulty = int(attempt.get("task_difficulty") or 0)
        except (TypeError, ValueError):
            difficulty = 0
        if difficulty <= 0:
            continue
        label = "Easy" if difficulty <= 2 else "Medium" if difficulty == 3 else "Hard"
        groups[label].append(attempt)
    return [
        detail_row(label, groups[label])
        for label in ("Easy", "Medium", "Hard")
        if groups.get(label)
    ]


def task_detail_rows(attempts: list[dict], limit: int = 8) -> list[dict]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for attempt in attempts:
        task_name = attempt.get("task_name")
        if task_name:
            groups[str(task_name)].append(attempt)
    rows = [detail_row(label, items) for label, items in groups.items()]
    rows.sort(
        key=lambda row: (
            row["avgPerformance"] is None,
            row["avgPerformance"] if row["avgPerformance"] is not None else 101,
            -row["attempts"],
        )
    )
    return rows[:limit]


def trend_detail(attempts: list[dict]) -> list[dict]:
    daily_scores: dict[str, list[float]] = defaultdict(list)
    for attempt in attempts:
        date = attempt.get("date")
        score = attempt.get("adjusted_performance_score")
        if date and score is not None:
            daily_scores[str(date)].append(float(score))
    dates = sorted(daily_scores)
    if len(dates) < 2:
        return [
            {
                "label": "Recent versus earlier records",
                "earlierAverage": None,
                "recentAverage": None,
                "change": None,
                "daysCompared": len(dates),
                "interpretation": "At least two days of records are needed for a trend comparison.",
            }
        ]
    daily_averages = [(date, mean(daily_scores[date])) for date in dates]
    midpoint = len(daily_averages) // 2
    earlier_values = [value for _date, value in daily_averages[:midpoint]]
    recent_values = [value for _date, value in daily_averages[midpoint:]]
    earlier = average(earlier_values)
    recent = average(recent_values)
    change = round(recent - earlier, 1) if earlier is not None and recent is not None else None
    if change is None:
        interpretation = "Not enough scored records are available for comparison."
    elif change >= 5:
        interpretation = "The data suggests recent adjusted performance is improving."
    elif change <= -5:
        interpretation = "The data suggests recent adjusted performance is declining. Caregiver review is recommended."
    else:
        interpretation = "The current records indicate relatively stable adjusted performance."
    return [
        {
            "label": "Recent versus earlier records",
            "earlierAverage": earlier,
            "recentAverage": recent,
            "change": f"{change:+.1f}" if change is not None else None,
            "daysCompared": len(dates),
            "interpretation": interpretation,
        }
    ]


def most_common_low_score(attempts: list[dict], key: str) -> str | None:
    scored = [
        (attempt.get(key), attempt.get("adjusted_performance_score"))
        for attempt in attempts
        if attempt.get(key) and attempt.get("adjusted_performance_score") is not None
    ]
    if not scored:
        return None
    grouped: dict[str, list[float]] = defaultdict(list)
    for name, score in scored:
        grouped[str(name)].append(float(score))
    return min(grouped, key=lambda name: mean(grouped[name]))


def reminder_tasks(attempts: list[dict]) -> list[str]:
    counts: dict[str, int] = defaultdict(int)
    for attempt in attempts:
        if int(attempt.get("reminders_needed") or 0) > 0:
            counts[attempt["task_name"]] += int(attempt.get("reminders_needed") or 0)
    return [
        name
        for name, _ in sorted(counts.items(), key=lambda item: item[1], reverse=True)[:5]
    ]


def help_tasks(attempts: list[dict]) -> list[str]:
    counts: dict[str, int] = defaultdict(int)
    for attempt in attempts:
        if attempt.get("help_requested"):
            counts[attempt["task_name"]] += 1
    return [
        name
        for name, _ in sorted(counts.items(), key=lambda item: item[1], reverse=True)[:5]
    ]


def recent_trend(attempts: list[dict]) -> str:
    completed_attempts = [
        attempt for attempt in attempts if attempt.get("adjusted_performance_score") is not None
    ]
    chronological = list(reversed(completed_attempts))
    if len(chronological) < 6:
        return "Not enough records yet"
    midpoint = len(chronological) // 2
    earlier = average([float(item["adjusted_performance_score"]) for item in chronological[:midpoint]])
    recent = average([float(item["adjusted_performance_score"]) for item in chronological[midpoint:]])
    if recent is None or earlier is None:
        return "Not enough records yet"
    if recent >= earlier + 5:
        return "Improving"
    if recent <= earlier - 5:
        return "Declining"
    return "Stable"


def build_insights(attempts: list[dict], today_attempts: list[dict]) -> dict:
    day_scores = group_average(attempts, "day_of_week")
    time_scores = group_average(attempts, "time_of_day")
    best_day, worst_day = best_and_worst(day_scores)
    best_time, worst_time = best_and_worst(time_scores)

    raw_scores = [
        float(attempt["raw_performance_score"])
        for attempt in attempts
        if attempt.get("raw_performance_score") is not None
    ]
    adjusted_scores = [
        float(attempt["adjusted_performance_score"])
        for attempt in attempts
        if attempt.get("adjusted_performance_score") is not None
    ]

    recommendations = []
    hardest_task = most_common_low_score(attempts, "task_name")
    hardest_category = most_common_low_score(attempts, "task_category")
    tasks_needing_reminders = reminder_tasks(attempts)
    tasks_needing_help = help_tasks(attempts)
    trend = recent_trend(attempts)
    time_details = grouped_detail_rows(
        attempts,
        "time_of_day",
        ["Morning", "Afternoon", "Evening", "Night"],
    )
    difficulty_details = difficulty_detail_rows(attempts)
    day_details = grouped_detail_rows(
        attempts,
        "day_of_week",
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    )
    task_details = task_detail_rows(attempts)
    trend_details = trend_detail(attempts)

    overall_counts = completion_counts(attempts)
    total = overall_counts["total"]
    total_reminders = sum(
        int(attempt.get("reminders_needed") or 0) for attempt in attempts
    )
    dates = sorted({str(attempt["date"]) for attempt in attempts if attempt.get("date")})
    completion_rate = percentage(overall_counts["completed"], total)
    alert_rate = percentage(overall_counts["caregiverAlerts"], total)
    help_rate = percentage(overall_counts["helpRequests"], total)
    raw_average = average(raw_scores)
    adjusted_average = average(adjusted_scores)

    if worst_time:
        recommendations.append(
            f"The data suggests reviewing routines scheduled in the {worst_time.lower()}."
        )
    if tasks_needing_reminders:
        recommendations.append(
            f"Additional reminders may help with {tasks_needing_reminders[0]}."
        )
    if tasks_needing_help:
        recommendations.append(
            f"Caregiver review is recommended for {tasks_needing_help[0]}."
        )
    if trend == "Declining":
        recommendations.append(
            "The current records indicate a recent decline. Caregiver review is recommended."
        )

    important_missed = [
        str(attempt.get("task_name"))
        for attempt in attempts
        if attempt.get("missed") and int(attempt.get("task_importance") or 0) >= 4
    ]
    if important_missed:
        recommendations.append(
            f"Caregiver review is recommended for important missed tasks, including {important_missed[0]}."
        )

    key_findings = []
    if time_details:
        scored_times = [row for row in time_details if row["avgPerformance"] is not None]
        if scored_times:
            strongest_time = max(scored_times, key=lambda row: row["avgPerformance"])
            weakest_time = min(scored_times, key=lambda row: row["avgPerformance"])
            key_findings.append(
                f"The data suggests {strongest_time['label'].lower()} is the strongest time block "
                f"(adjusted average {strongest_time['avgPerformance']} across {strongest_time['attempts']} attempts)."
            )
            if strongest_time["label"] != weakest_time["label"]:
                key_findings.append(
                    f"{weakest_time['label']} has the lowest adjusted average "
                    f"({weakest_time['avgPerformance']} across {weakest_time['attempts']} attempts); "
                    f"task difficulty and support needs should be reviewed before changing schedules."
                )
    if difficulty_details:
        hard_row = next((row for row in difficulty_details if row["label"] == "Hard"), None)
        easy_row = next((row for row in difficulty_details if row["label"] == "Easy"), None)
        if hard_row:
            comparison = (
                f" compared with {easy_row['avgPerformance']} for easy tasks"
                if easy_row and easy_row["avgPerformance"] is not None
                else ""
            )
            key_findings.append(
                f"Hard tasks average {hard_row['avgPerformance']} adjusted performance{comparison}, "
                f"with a {hard_row['struggleRate']} support-need rate."
            )
    if task_details:
        hardest = task_details[0]
        key_findings.append(
            f"{hardest['label']} currently has the lowest task-level adjusted average "
            f"({hardest['avgPerformance']}) and averages {hardest['avgReminders']} reminders "
            f"across {hardest['attempts']} attempts."
        )
    if trend_details:
        key_findings.append(trend_details[0]["interpretation"])
    if not key_findings:
        key_findings.append(
            "The current records are not yet sufficient for reliable pattern comparisons."
        )

    recommended_actions = list(dict.fromkeys(recommendations))
    if worst_time and hardest_task:
        recommended_actions.append(
            f"Review whether {hardest_task} can use shorter one-step instructions or be scheduled outside the {worst_time.lower()}, when practical."
        )
    recommended_actions.append(
        "Treat patient-marked completion as unverified unless a caregiver or device confirms it."
    )
    if total < 12:
        recommended_actions.append(
            "Continue collecting task attempts before making major schedule changes; the current sample is limited."
        )

    data_notes = [
        f"This analysis uses {total} stored task attempts across {len(dates)} day{'s' if len(dates) != 1 else ''}. Small groups can change substantially as new records are added.",
        "Adjusted performance accounts for task difficulty; raw and adjusted scores are shown separately to reduce time-versus-difficulty confounding.",
        "Reminder requests, help requests, possible confusion flags, missed tasks, and scores are behavior signals. Caregiver alerts are system responses and are not used as proof of struggle.",
        "A patient marking a task complete does not verify that the task was completed correctly; caregiver or device verification remains separate.",
    ]

    return {
        "counts": completion_counts(today_attempts),
        "overallCounts": overall_counts,
        "rawPerformance": raw_average,
        "adjustedPerformance": adjusted_average,
        "bestTimeOfDay": best_time,
        "worstTimeOfDay": worst_time,
        "bestDayOfWeek": best_day,
        "worstDayOfWeek": worst_day,
        "hardestTaskCategory": hardest_category,
        "hardestTask": hardest_task,
        "tasksNeedingReminders": tasks_needing_reminders,
        "tasksNeedingHelp": tasks_needing_help,
        "recentTrend": trend,
        "recommendations": recommended_actions,
        "detailSummary": {
            "taskAttempts": total,
            "days": len(dates),
            "dateRange": f"{dates[0]} to {dates[-1]}" if dates else "No records yet",
            "completionRate": completion_rate,
            "rawAverage": raw_average,
            "adjustedAverage": adjusted_average,
            "caregiverAlertRate": alert_rate,
            "helpRequestRate": help_rate,
            "confusionFlags": overall_counts["confusionFlags"],
            "totalReminders": total_reminders,
        },
        "timeOfDayDetails": time_details,
        "difficultyDetails": difficulty_details,
        "dayOfWeekDetails": day_details,
        "taskDetails": task_details,
        "trendDetails": trend_details,
        "keyFindings": key_findings,
        "recommendedActions": recommended_actions,
        "dataNotes": data_notes,
    }


def automatic_summary(today_attempts: list[dict], insights: dict) -> str:
    if not today_attempts:
        return "No patient activity has been recorded today."

    completed = [
        attempt["task_name"]
        for attempt in today_attempts
        if attempt.get("completed")
    ]
    missed = [
        attempt["task_name"]
        for attempt in today_attempts
        if attempt.get("missed")
    ]
    reminder_attempts = [
        attempt
        for attempt in today_attempts
        if int(attempt.get("reminders_needed") or 0) > 0
    ]
    help_attempts = [
        attempt["task_name"]
        for attempt in today_attempts
        if attempt.get("help_requested")
    ]

    parts = []
    if completed:
        parts.append(f"{', '.join(completed)} were marked complete.")
    if reminder_attempts:
        reminder_text = ", ".join(
            f"{attempt['task_name']} required {attempt['reminders_needed']} reminder"
            f"{'' if int(attempt['reminders_needed']) == 1 else 's'}"
            for attempt in reminder_attempts
        )
        parts.append(f"{reminder_text}.")
    if missed:
        parts.append(f"{', '.join(missed)} were missed.")
    if help_attempts:
        parts.append(f"Caregiver help was requested for {', '.join(help_attempts)}.")
    if insights.get("recommendations"):
        parts.append(insights["recommendations"][0])

    return " ".join(parts)

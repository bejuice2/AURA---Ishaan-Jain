from __future__ import annotations


def clamp(value: float, minimum: float = 0, maximum: float = 100) -> float:
    return max(minimum, min(maximum, value))


def raw_performance_score(
    completed: bool,
    reminders_needed: int,
    help_requested: bool,
    confusion_flag: bool,
    time_to_complete: int | None,
) -> float:
    score = 100.0 if completed else 35.0
    score -= min(reminders_needed, 5) * 8

    if help_requested:
        score -= 18

    if confusion_flag:
        score -= 15

    if time_to_complete is not None:
        if time_to_complete > 20 * 60:
            score -= 12
        elif time_to_complete > 10 * 60:
            score -= 6

    return round(clamp(score), 1)


def adjusted_performance_score(raw_score: float, task_difficulty: int) -> float:
    difficulty = max(1, min(5, int(task_difficulty or 3)))
    adjustment = {
        1: -8,
        2: -4,
        3: 0,
        4: 4,
        5: 8,
    }[difficulty]
    return round(clamp(raw_score + adjustment), 1)


def score_attempt(attempt: dict) -> tuple[float, float]:
    raw_score = raw_performance_score(
        completed=bool(attempt.get("completed")),
        reminders_needed=int(attempt.get("reminders_needed") or 0),
        help_requested=bool(attempt.get("help_requested")),
        confusion_flag=bool(attempt.get("confusion_flag")),
        time_to_complete=attempt.get("time_to_complete"),
    )
    adjusted_score = adjusted_performance_score(
        raw_score=raw_score,
        task_difficulty=int(attempt.get("task_difficulty") or 3),
    )
    return raw_score, adjusted_score

from __future__ import annotations

from datetime import datetime, timedelta
from threading import Lock

import runtime_config


_lock = Lock()
_real_anchor = runtime_config.local_now()
_sim_anchor = _real_anchor
_speed = 1.0


def now() -> datetime:
    with _lock:
        real_elapsed = runtime_config.local_now() - _real_anchor
        simulated_elapsed = real_elapsed.total_seconds() * _speed
        return _sim_anchor + timedelta(seconds=simulated_elapsed)


def state() -> dict:
    current = now()
    with _lock:
        speed = _speed
    return {
        "iso": current.isoformat(timespec="seconds"),
        "date": current.strftime("%Y-%m-%d"),
        "time": current.strftime("%I:%M:%S %p"),
        "speed": speed,
    }


def set_speed(speed: float) -> dict:
    global _real_anchor, _sim_anchor, _speed
    safe_speed = max(0.0, min(float(speed), 240.0))
    current = now()
    with _lock:
        _sim_anchor = current
        _real_anchor = runtime_config.local_now()
        _speed = safe_speed
    return state()


def reset() -> dict:
    global _real_anchor, _sim_anchor, _speed
    with _lock:
        _real_anchor = runtime_config.local_now()
        _sim_anchor = _real_anchor
        _speed = 1.0
    return state()

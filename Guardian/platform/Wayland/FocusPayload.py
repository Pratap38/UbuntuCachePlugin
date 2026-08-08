from datetime import datetime

from Guardian.models.DesktopEnvironment import DesktopEnv
from Guardian.models.WindowInfo import WindowInfo


def normalize_focus_payload(payload: dict) -> dict:
    return {
        "application": payload.get("application", "Unknown"),
        "app_id": payload.get("app_id", ""),
        "pid": int(payload.get("pid", -1)),
        "title": payload.get("title", ""),
        "window_id": payload.get("window_id", "WAYLAND"),
        "focused": bool(payload.get("focused", True)),
        "timestamp": payload.get("timestamp", datetime.now().isoformat()),
    }


def window_info_from_focus_payload(payload: dict) -> WindowInfo:
    data = normalize_focus_payload(payload)
    return WindowInfo(
        windoId=data["window_id"],
        pID=data["pid"],
        application=data["application"],
        title=data["title"],
        focused=data["focused"],
        timestamp=datetime.fromisoformat(data["timestamp"])
        if isinstance(data["timestamp"], str)
        else data["timestamp"],
        environment=DesktopEnv.WAYLAND,
    )

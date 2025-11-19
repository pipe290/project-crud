# app/utils/logger.py
import datetime
import json
import os

LOG_PATH = "app/logs/excel_logs.json"

os.makedirs("app/logs", exist_ok=True)

def log_excel_event(event: str, details: dict = None):
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "event": event,
        "details": details or {}
    }

    try:
        if not os.path.exists(LOG_PATH):
            with open(LOG_PATH, "w") as f:
                json.dump([], f)

        with open(LOG_PATH, "r+") as f:
            data = json.load(f)
            data.append(entry)
            f.seek(0)
            json.dump(data, f, indent=2)
    except Exception as e:
        print("ERROR WRITING LOG:", e)

import win32evtlog
import json
from datetime import datetime, timedelta

LOG_TYPE = 'Security'
TARGET_EVENT_IDS = [4625, 4688, 4720]  # failed login, process create, user creation
OUTPUT_FILE = 'logs/parsed_logs.json'
MAX_EVENTS = 100

def extract_event_data(event):
    try:
        time_generated = event.TimeGenerated.Format()
        dt_obj = datetime.strptime(time_generated, "%c")
    except:
        time_generated = "Unknown"
        dt_obj = None

    event_id = getattr(event, "EventID", -1)

    try:
        message = str(event.StringInserts) if event.StringInserts else "No message"
    except:
        message = "No message"

    # Default user
    user = "Unknown"

    # Special handling for User Creation (4720)
    if event_id == 4720 and event.StringInserts:
        # first element in StringInserts = new username
        user = event.StringInserts[0]

    # Failed logins (4625) and others might include username in StringInserts too
    elif event_id == 4625 and event.StringInserts:
        # usually 5th element is username (depends on Windows version)
        user = event.StringInserts[5] if len(event.StringInserts) > 5 else "Unknown"

    return {
        "timestamp": time_generated,
        "datetime_obj": dt_obj.isoformat() if dt_obj else None,
        "event_id": event_id,
        "user": user,
        "event_message": message
    }

def read_logs():
    log_handle = win32evtlog.OpenEventLog(None, LOG_TYPE)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

    events = []
    total = 0

    cutoff_time = datetime.now() - timedelta(hours=1)

    while total < MAX_EVENTS:
        records = win32evtlog.ReadEventLog(log_handle, flags, 0)
        if not records:
            break
        for event in records:
            if event.EventID in TARGET_EVENT_IDS:
                try:
                    event_time = datetime.strptime(event.TimeGenerated.Format(), "%c")
                except:
                    continue

                if event_time >= cutoff_time:  # only last 1 hour
                    data = extract_event_data(event)
                    events.append(data)
                    total += 1
                    if total >= MAX_EVENTS:
                        break

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(events, f, indent=4)

    print(f"[+] Saved {len(events)} security logs (last 1 hour) to {OUTPUT_FILE}")

if __name__ == "__main__":
    read_logs()

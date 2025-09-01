import os, json, datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGDIR = os.path.join(BASE, "logs")

def read_json(path, default=[]):
    try:
        with open(path, 'r') as f: return json.load(f)
    except Exception:
        return default

def write_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def plan_actions(explained_logs):
    """Plan actions for each explained anomaly (but don’t execute yet)."""
    actions = []
    for log in explained_logs:
        threat = log.get("threat_type", "").lower()
        action = "Send alert to admin"
        status = "planned"

        # --- Rule-based planner ---
        if "failed login" in threat:
            action = f"Block IP {log.get('log',{}).get('ip','Unknown')}"
        elif "suspicious process" in threat:
            action = f"Kill process {log.get('log',{}).get('process','Unknown')}"
        elif "malware" in threat:
            action = f"Quarantine file {log.get('log',{}).get('file','Unknown')}"
        elif "user creation" in threat or "unauthorized user" in threat:
            action = f"Delete user {log.get('user')}"
        else:
            action = "Send alert to admin"

        user = log.get("user")
        actions.append({
            "timestamp": log.get("timestamp", datetime.datetime.now().isoformat()),
            "threat_type": threat,
            "action": action,
            "status": status,
            "log": {"user":user},
            "explanation":log.get('explanation'),
            "event_id":log.get('event_id')
        })

    outpath = os.path.join(LOGDIR, "planned_actions.json")
    write_json(outpath, actions)
    print(f"[+] Planned {len(actions)} actions → {outpath}")
    return actions

if __name__ == "__main__":
    explained_path = os.path.join(LOGDIR, "anomalies_explained.json")
    explained = read_json(explained_path, [])
    plan_actions(explained)

import os, json, datetime, shutil

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGDIR = os.path.join(BASE, "logs")
QUARANTINE = os.path.join(BASE, "quarantine")

# ⚠️ Safety switch: set False to actually execute system-level commands
DRY_RUN = False

def read_json(path, default=[]):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception:
        return default

def write_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

# --- Actions ---
def block_ip(ip):
    if DRY_RUN:
        print(f"[DRY RUN] Would block IP {ip}")
    else:
        os.system(f'netsh advfirewall firewall add rule name="Block_{ip}" dir=in action=block remoteip={ip}')

def kill_process(proc):
    if DRY_RUN:
        print(f"[DRY RUN] Would kill process {proc}")
    else:
        os.system(f'taskkill /F /IM {proc}')

def quarantine_file(path):
    if DRY_RUN:
        print(f"[DRY RUN] Would quarantine file {path}")
    else:
        os.makedirs(QUARANTINE, exist_ok=True)
        if os.path.exists(path):
            shutil.move(path, os.path.join(QUARANTINE, os.path.basename(path)))

def delete_user(user):
    clean_user = str(user).strip()
    if "\\" in clean_user:  # strip domain prefix
        clean_user = clean_user.split("\\")[-1]

    print(f"[DEBUG] Trying to delete user → {clean_user}")

    if DRY_RUN:
        print(f"[DRY RUN] Would delete user {clean_user}")
    else:
        os.system(f'net user "{clean_user}" /delete')

# --- Core executor ---
def execute_actions(plans):
    executed = []
    for plan in plans:
        threat = plan.get("threat_type", "").lower()
        log = plan.get("log", {})
        status, action_taken = "skipped", "No action"

        if "failed login" in threat:
            ip = log.get("ip", "Unknown")
            block_ip(ip)
            action_taken, status = f"Blocked IP {ip}", "executed"

        elif "suspicious process" in threat:
            proc = log.get("process", "unknown.exe")
            kill_process(proc)
            action_taken, status = f"Killed process {proc}", "executed"

        elif "malware" in threat:
            file_path = log.get("file", "unknown_file.exe")
            quarantine_file(file_path)
            action_taken, status = f"Quarantined file {file_path}", "executed"

        elif "unauthorized user" in threat:
            user = log.get("user")
            delete_user(user)
            action_taken, status = f"Deleted user {user}", "executed"

        else:
            print(f"[INFO] No mapped action for threat: {threat}")
            action_taken = "Alerted admin"
            status = "not_mapped"

        plan["action"] = action_taken
        plan["status"] = status
        executed.append(plan)

    outpath = os.path.join(LOGDIR, "actions.json")
    write_json(outpath, executed)
    print(f"[+] Executed {len(executed)} actions → {outpath}")
    return executed

if __name__ == "__main__":
    plans = read_json(os.path.join(LOGDIR, "planned_actions.json"), [])
    execute_actions(plans)
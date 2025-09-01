from flask import Flask, jsonify, send_from_directory
import os, json, subprocess, sys, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
LOGDIR = os.path.join(BASE, "logs")
STATIC = os.path.join(BASE, "web")

def run_module(script_path, args=[]):
    """Run a Python script sequentially using the same interpreter"""
    if not os.path.exists(script_path):
        print(f"[!] Missing script: {script_path}")
        return
    print(f"[*] Running {os.path.basename(script_path)} ...")
    subprocess.run([sys.executable, script_path] + args, check=True)

def read_json(path, default):
    try:
        with open(path,'r') as f:
            return json.load(f)
    except Exception:
        return default

def write_json(path, data):
    with open(path,'w') as f:
        json.dump(data, f, indent=4)

def run_pipeline():
    print("[*] Running CyberSentinel pipeline...")

    os.makedirs(LOGDIR, exist_ok=True)

    # 1. Collect logs
    run_module(os.path.join(BASE, "logs", "win_log_reader.py"))

    # 2. Detect anomalies
    run_module(os.path.join(BASE, "ml", "anomaly_model.py"))
    anomalies_path = os.path.join(LOGDIR,"anomalies.json")
    anomalies = read_json(anomalies_path, [])

    if len(anomalies) == 0:
        print("[!] No anomalies found. Injecting dummy threat for demo.")
        dummy = {
            "timestamp": datetime.datetime.now().isoformat(),
            "threat_type": "Failed Login Attempt",
            "log": {"event_id": 4625, "ip": "192.168.1.10"},
            "severity": "critical",
            "explanation": "Multiple failed login attempts detected from IP 192.168.1.10"
        }
        anomalies = [dummy]
        write_json(anomalies_path, anomalies)

    # 3. Explain anomalies
    run_module(os.path.join(BASE, "agent", "explainer.py"))

    # 4. Plan actions
    run_module(os.path.join(BASE, "agent", "planner.py"))

    # 5. Execute actions
    run_module(os.path.join(BASE, "agent", "takeactions.py"))

    print("[*] Pipeline finished. Dashboard data written to logs/")

if __name__ == '__main__':
    run_pipeline()

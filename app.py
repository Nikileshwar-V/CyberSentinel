import os, sys, subprocess, time
from flask import Flask, render_template
import json, webbrowser

def resource_path(relative_path):
    """Get absolute path to resource (works in dev and PyInstaller exe)."""
    if hasattr(sys, '_MEIPASS'):  # running in PyInstaller bundle
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Flask app setup
app = Flask(
    __name__,
    template_folder=resource_path("templates"),
    static_folder=resource_path("web")
)

BASE = resource_path("")   # project root
LOGDIR = resource_path("logs")

def start_server():
    """Start server.py before Flask"""
    server_path = os.path.join(BASE, "server.py")
    # Use sys.executable so it works in exe and python
    process = subprocess.Popen(
        [sys.executable, server_path],
        cwd=BASE
    )
    # wait a little for server.py to start writing logs
    time.sleep(2)
    return process

def read_json(filename):
    """Read JSON file safely."""
    path = os.path.join(LOGDIR, filename)
    if os.path.exists(path):
        with open(path, "r") as f:
            try:
                return json.load(f)
            except Exception:
                return []
    return []

@app.route("/threatlogs", endpoint="threatlogs")
def show_threatlogs():
    anomalies = read_json("parsed_logs.json")
    return render_template("threatlogs.html", anomalies=anomalies)


@app.route("/")
def dashboard():
    anomalies = read_json("anomalies_explained.json")
    actions = read_json("actions.json")

    total_threats = len(anomalies)
    resolved_threats = sum(1 for a in actions if a.get("status") == "executed")
    active_threats = total_threats - resolved_threats

    chart_labels = [a.get("timestamp", "")[-8:-3] for a in anomalies]
    chart_data = list(range(1, len(anomalies) + 1))

    return render_template(
        "dashboard.html",
        total_threats=total_threats,
        active_threats=active_threats,
        resolved_threats=resolved_threats,
        actions=actions,
        chart_labels=chart_labels,
        chart_data=chart_data
    )

if __name__ == "__main__":
    # Start server.py before Flask
    start_server()
    app.run(debug=True)

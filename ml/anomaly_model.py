import json
import pandas as pd
from sklearn.ensemble import IsolationForest
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # CyberSentinel/
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'parsed_logs.json')
OUTPUT_FILE = os.path.join(BASE_DIR, 'logs', 'anomalies.json')


def load_logs():
    """Load parsed logs safely."""
    if not os.path.exists(LOG_FILE):
        print(f"[!] Log file not found: {LOG_FILE}")
        return []
    try:
        with open(LOG_FILE, 'r') as f:
            logs = json.load(f)
            return logs if isinstance(logs, list) else []
    except Exception as e:
        print(f"[!] Failed to load logs: {e}")
        return []


def extract_features(logs):
    """Extract features from logs for ML model."""
    if not logs:
        return pd.DataFrame(), None

    df = pd.DataFrame(logs)

    # Ensure required columns exist
    if 'timestamp' not in df.columns:
        df['timestamp'] = pd.NaT
    if 'user' not in df.columns:
        df['user'] = "unknown"
    if 'event_id' not in df.columns:
        df['event_id'] = 0

    # Convert timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors="coerce")

    # Feature engineering
    df['hour'] = df['timestamp'].dt.hour.fillna(0).astype(int)
    df['user_encoded'] = df['user'].astype('category').cat.codes
    df['event_id'] = pd.to_numeric(df['event_id'], errors='coerce').fillna(0)

    features = df[['event_id', 'hour', 'user_encoded']]
    return df, features


def detect_anomalies(logs):
    """Train IsolationForest and detect anomalies."""
    df, X = extract_features(logs)

    if df.empty or X is None or X.empty:
        print("[!] No logs available for anomaly detection.")
        with open(OUTPUT_FILE, 'w') as f:
            json.dump([], f, indent=4)
        return []

    # Train Isolation Forest
    model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
    df['anomaly'] = model.fit_predict(X)

    # -1 = anomaly
    anomalies = df[df['anomaly'] == -1]
    print(f"[+] Detected {len(anomalies)} anomalies out of {len(df)} logs.")

    # Save anomalies
    anomalies = anomalies.copy()
    anomalies['timestamp'] = anomalies['timestamp'].astype(str)  # JSON-safe
    anomalies_to_save = anomalies.drop(columns=['user_encoded', 'hour', 'anomaly']).to_dict(orient='records')

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(anomalies_to_save, f, indent=4)


    return anomalies_to_save


if __name__ == "__main__":
    logs = load_logs()
    detect_anomalies(logs)

import os, json, datetime
import ollama  # using your working local Ollama setup

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
ANOMALY_FILE = os.path.join(LOG_DIR, "anomalies.json")
OUTPUT_FILE = os.path.join(LOG_DIR, "anomalies_explained.json")

def create_prompt(log_entry):
    return f"""
You are a cybersecurity analyst AI. Explain the following Windows Security Event Log in plain English in one line wihtin 10 to 15 words.
the explaination should be very easily understandable even by a kid.

Timestamp: {log_entry.get('timestamp', 'Unknown')}
Event ID: {log_entry.get('event_id', 'Unknown')}
User: {log_entry.get('user', 'Unknown')}
Event Message: {log_entry.get('event_message', 'No message provided')}

What does this log indicate? Is this a failed login, user creation, suspicious process, or malware? 
Answer in one line as if reporting to a SOC analyst.
"""

def classify_threat(event_id):
    """Rule-based classification of event IDs"""
    mapping = {
        4625: "Failed Login Attempt",
        4688: "Suspicious Process",
        4720: "Unauthorized User Creation"
    }
    return mapping.get(event_id, "Unknown")

def explain_with_llm(prompt):
    try:
        response = ollama.chat(model="tinyllama", messages=[
            {"role": "user", "content": prompt}
        ])
        return response["message"]["content"]
    except Exception as e:
        return f"[LLM Error] {str(e)}"

def main():
    if not os.path.exists(ANOMALY_FILE):
        print(f"[!] Anomaly log file not found: {ANOMALY_FILE}")
        return

    try:
        with open(ANOMALY_FILE, "r") as f:
            anomalies = json.load(f)
    except json.JSONDecodeError:
        print("[!] Could not parse anomalies.json")
        return

    if not anomalies:
        print(" No anomalies found.")
        return

    explained = []
    for idx, log in enumerate(anomalies, start=1):
        print(f"\n🔍 Explaining Anomaly #{idx}")

        # --- Rule-based threat type ---
        threat_type = classify_threat(log.get("event_id", -1))

        # --- AI explanation ---
        prompt = create_prompt(log)
        explanation = explain_with_llm(prompt)

        # attach both to the log
        log["explanation"] = explanation
        log["threat_type"] = threat_type

        explained.append(log)

        print(" Explanation:\n", explanation)
        print(" Classified Threat Type:", threat_type)
        print("=" * 80)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(explained, f, indent=4)

    print(f"[+] Saved explained anomalies to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

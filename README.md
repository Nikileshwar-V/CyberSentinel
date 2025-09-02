# 🛡️ CyberSentinel: Autonomous AI Agent for Threat Hunting & Self-Healing Networks

## 📌 Overview

**CyberSentinel** is an advanced AI-driven cybersecurity framework designed to autonomously detect, explain, and mitigate threats in real time. By integrating anomaly detection, natural language explanations, and automated self-healing, CyberSentinel redefines how organizations approach threat response and network resilience.

This project was built as part of an MCA academic research initiative to demonstrate the potential of **AI-powered cybersecurity automation**. CyberSentinel combines cutting-edge techniques from **machine learning, NLP, and security engineering** to deliver a scalable, modular solution.

---

## 🚀 Features

* **🔍 Intelligent Log Monitoring:** Continuously analyzes Windows system logs for suspicious activities.
* **📊 Anomaly Detection:** ML-powered models to detect unusual patterns in real-time.
* **🧠 Log Explanation (NLP-powered):** Converts raw anomalies into human-readable explanations for better incident understanding.
* **⚡ Autonomous Threat Response:** Plans and executes mitigation steps (block IPs, terminate malicious processes, isolate system components).
* **🛠️ Self-Healing Networks:** Restores system stability post-attack by automatically applying corrective measures.
* **📈 Web Dashboard (Flask):** Interactive visualization of anomalies, threat reports, and actions taken.
* **🖥️ CLI Mode:** Lightweight terminal interface for quick testing and log monitoring.

---

## 🏗️ Project Structure

```bash
CyberSentinel/
│
├── app.py # Flask application entry
├── server.py # CLI / local server runner
├── run_log_collector.bat # Script to collect Windows logs
│
├── agent/ # AI agent modules
│ ├── explainer.py # Explains anomalies
│ ├── planner.py # Maps threats to responses
│ └── takeactions.py # Executes planned actions
│
├── ml/ # Machine learning models
│ └── anomaly_model.py # Trains & runs anomaly detection
│
├── logs/ # Generated logs & results
│ ├── parsed_logs.json
│ ├── anomalies.json
│ ├── actions.json
│ ├── anomalies_explained.json
│ ├── planned_actions.json
│ ├── config.json
│ ├── sample_log.json
│ └── win_log_reader.py
│
├── templates/ # Flask HTML templates
│ ├── dashboard.html
│ └── threatlogs.html

---

## 🔧 Tech Stack

* **Programming Language:** Python 3.10+
* **Frameworks:** Flask, Scikit-learn, TensorFlow (optional), PyTorch (for NLP models)
* **Libraries:** Pandas, NumPy, Matplotlib, OpenCV, Transformers (HuggingFace)
* **Database:** SQLite (lightweight, modular)
* **Deployment:** PyInstaller (for EXE builds), Docker (future scope)

---

## 📊 Results

### ✅ CLI Mode

* Successfully detects anomalies in system logs.
* Provides **real-time explanations** of detected threats.
* Executes corresponding security actions automatically.

### ✅ Flask Web App

* User-friendly dashboard with:

  * Threat detection visualization (charts, logs, alerts).
  * Real-time anomaly explanations.
  * Action logs showing applied mitigations.

### ✅ Self-Healing Capability

* Planned and executed corrective actions for detected anomalies.
* Showcased ability to **automatically block malicious IPs, kill rogue processes, and restore stability**.

---

## 📥 Installation & Usage

### 🔽 Clone Repository

```bash
git clone https://github.com/Nikileshwar-V/CyberSentinel.git
cd CyberSentinel
```

### ▶️ Run in CLI Mode

```bash
python cli.py
```

### 🌐 Run Flask Web App

```bash
python app.py
```

Then open `http://127.0.0.1:5000/` in your browser.

### 📦 Build Executable (Optional)

```bash
pyinstaller --name CyberSentinel --onefile --add-data "templates;templates" --add-data "web;web" --add-data "logs;logs" --add-data "ml;ml" --add-data "agent;agent" --hidden-import flask app.py
```

---

## 📚 Future Enhancements

* 🔗 **Integration with SIEM platforms** (Splunk, ELK).
* 🌍 **Multi-platform log monitoring** (Linux, MacOS).
* 🤖 **Enhanced LLM-powered explanations** using fine-tuned transformers.
* 🛡️ **Advanced deception techniques** (honeypots, decoys).
* ☁️ **Cloud-native deployment** with Docker & Kubernetes.

---

## 🧑‍💻 Author

**Nikileshwar V**
MCA Student | AI/ML Enthusiast | Open to Internships, Job roles & Collaboration in real time projects
[GitHub](https://github.com/Nikileshwar-V) | [LinkedIn](https://linkedin.com/in/nikileshwar-v)

# CyberSentinel : An Autonomous AI Agent for Real-Time Threat Hunting and Self-Healing Networks

CyberSentinel/
│
├── agent/                 # AI agent logic
│   ├── planner.py
│   ├── executor.py
│   └── memory.py
│
├── ml/                    # ML models
│   ├── anomaly_model.py
│   └── preprocess.py
│
├── logs/                  # Log files (input)
│   └── sample_log.json
│
├── web/                   # Flask frontend
│   ├── app.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       └── style.css
│
├── docs/                  # Reports and documentation
│   └── abstract.pdf
│
├── .env                   # API keys and configs
└── README.md

Abstract:
This project introduces CyberSentinel — a real-time cybersecurity system powered by AI and LLMs. It autonomously analyzes system logs, detects threats using machine learning, and uses a Large Language Model to investigate and explain anomalies in natural language. CyberSentinel is agentic, meaning it not only detects threats but can also take actions like blocking IPs, restarting services, or isolating processes. A dashboard interface provides insights and alerts, enabling proactive and autonomous cyber defense. This system demonstrates how GenAI and autonomous agents can modernize threat hunting and response in a scalable, explainable, and hands-free way.

#MCA student building an agentic AI-based cyberdefense system using LLMs and ML

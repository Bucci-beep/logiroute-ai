# LogiRoute-AI: Automated Freight Intake & Multi-Agent Dispatch Gateway

LogiRoute-AI is a production-grade, asynchronous backend framework built with **FastAPI** and **Pydantic** that automates the transition from messy, unstructured broker communications (emails, phone transcripts) into rigorous, validated logistics manifests. 

Rather than relying on fragile, raw LLM prompt responses, this system implements a deterministic validation pattern paired with a multi-agent orchestration workflow using high-speed **Groq LLM inference** and native tool-calling capabilities.

---

## 🏗️ 3-Step Execution Architecture

The system treats LLM integration as an engineering pipeline rather than an experimental script, operating across three distinct layers:

[ Unstructured Text ]
          │
          ▼
┌──────────────────────┐
│ 1. INTAKE LAYER      │ ──► [ Pydantic Schema Validation ]
└──────────────────────┘                 │
│                             ├─► [FAIL] ──► [ /manual_review Queue ]
▼ [PASS]                      │
┌──────────────────────┐                 ▼
│ 2. DISPATCH AGENT    │ ──► [ Loop 1: Query Fleet DB Tool ]
└──────────────────────┘ ──► [ Loop 2: Call Calendar/Scheduling API ]
│
▼
┌──────────────────────┐
│ 3. FASTAPI GATEWAY   │ ──► [ Asynchronous Production Endpoints ]
└──────────────────────┘

### 1. Strict Schema Validation (The Intake Layer)
Guards the database and core application domain using a strict `Pydantic` schema to parse raw payloads. It enforces rigid, real-world physical and temporal logistics boundaries before data routes downstream:
* **Temporal Guards:** Ensures pickup dates cannot be backdated or scheduled in the past.
* **Regulatory Formatting:** Enforces strict US Department of Transportation (`USDOT`) identification rules via optimized regex patterns.
* **Physical Safety Ceilings:** Rejects any physical payloads exceeding real-world weight constraints (e.g., maximum legal ceiling of 45,000 lbs for standard semi-truck freight).

### 2. Multi-Agent Orchestration & Tool Routing
Leverages an isolated tool-calling routing loop running on two specialized functional units:
* **The Intake Agent:** Translates unstructured broker text strings or phone transcripts into structured entities via Groq's JSON tool-calling capabilities.
* **The Dispatch Agent:** Receives validated objects, queries a simulated `Truck Fleet Database` to lock down available drivers, and commits a final payload lease transaction through a `Calendar/Scheduling API`.

### 3. FastAPI Production Routing Gateway
An enterprise-ready, asynchronous web interface driving two core processing pipelines:
* `POST /dispatch/intake`: Entrypoint for unstructured raw inputs.
* `POST /dispatch/assign`: Executes the multi-agentic matching and booking loop.
* **Deterministic Fallback Handler:** If validation fails at the Intake Layer, an interceptor safely reroutes the broken payload directly to a `/manual_review` queue database bucket rather than allowing a 500 system crash.

---

## 📂 Repository Structure

The layout follows industry-standard conventions for clean separation of concerns:

```text
logiroute-ai/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Kernel API gateway entrypoint
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── intake_agent.py     # Schema extraction & parsing
│   │   └── dispatch_agent.py   # Tool-routing execution loop
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py        # /intake and /assign route handlers
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py           # Secure environment configurations
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py          # Strict Pydantic logistics constraints
│   └── services/
│       ├── __init__.py
│       └── fleet_db.py         # Mock Fleet DB and Scheduling API tools
├── .env                        # Local environment secrets
├── .gitignore                  # Production file exclusions
├── requirements.txt            # Pinned system dependencies
└── README.md                   # System architectural documentation

Quickstart & Local Verification
1. Environment Set Up
Clone the project, set up an isolated Python virtual environment, and refresh permissions to bypass macOS Anaconda environment lockouts:
Bash
# Force clear broken shell caches
cd ~/Desktop/Self-Learning/Agents/logiroute-ai

# Reset directory permissions safely
chmod -R 755 .

# Instantiate virtual environment
python3 -m venv .venv
source .venv/bin/activate
2. Dependency Installation
Install production packages into your isolated environment:
Bash
pip install -r requirements.txt
3. Configure Credentials
Create a .env file in the root folder and add your high-speed Groq API credentials:
Code snippet
GROQ_API_KEY=gsk_your_secret_key_here
4. Boot Up the API Dev Engine
Spin up the local asynchronous web server via Uvicorn:
Bash
uvicorn app.main:app --reload
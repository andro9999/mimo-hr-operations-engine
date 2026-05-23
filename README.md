# MiMo HR Operations Engine

An AI-powered HR operations platform built on MiMo LLM with an agent-based architecture for automating the full employee lifecycle.

```
+------------------------------------------------------------------+
|                    MiMo HR Operations Engine                      |
+------------------------------------------------------------------+
|                                                                   |
|   +-----------+      +----------------------------+               |
|   |  FastAPI  |----->|       AgentKernel          |               |
|   |  Server   |      |  +----------------------+  |               |
|   +-----------+      |  |     Event Bus        |  |               |
|        |             |  +----------------------+  |               |
|        v             |                            |               |
|   +-----------+      |  +----------+----------+  |               |
|   | Dashboard |      |  | Onboard | Policy   |  |               |
|   |  (HTML)   |      |  +----------+----------+  |               |
|   +-----------+      |  | Perform | Learning |  |               |
|                      |  +----------+----------+  |               |
|                      |  | Engage  | Payroll  |  |               |
|                      |  +----------+----------+  |               |
|                      |  | Offboard           |  |               |
|                      |  +--------------------+  |               |
|                      +----------------------------+               |
+------------------------------------------------------------------+
```

## File Structure

```
mimo-hr-operations-engine/
|-- README.md
|-- requirements.txt
|-- Dockerfile
|-- docker-compose.yml
|-- .github/
|   `-- workflows/
|       `-- ci.yml
|-- config/
|   `-- settings.py
|-- dashboard/
|   `-- index.html
`-- app/
    |-- main.py
    |-- kernel/
    |   |-- __init__.py
    |   `-- agent_kernel.py
    |-- agents/
    |   |-- __init__.py
    |   |-- onboarding_agent.py
    |   |-- policy_agent.py
    |   |-- performance_agent.py
    |   |-- learning_agent.py
    |   |-- engagement_agent.py
    |   |-- payroll_agent.py
    |   `-- offboarding_agent.py
    `-- routers/
        |-- __init__.py
        `-- hr.py
```

## Tech Stack

- **Python 3.11+**
- **FastAPI** - Async web framework with automatic OpenAPI docs
- **MiMo LLM** - Nous Research language model for HR intelligence
- **Pydantic** - Data validation and settings management
- **Docker** - Containerized deployment
- **Uvicorn** - ASGI server

## Agents

| Agent | Description |
|---|---|
| **Onboarding** | Manages paperwork generation, IT setup coordination, training schedule assignment, and buddy pairing for new hires. |
| **Policy** | Handles HR policy Q&A, interprets policy documents for specific scenarios, and flags compliance issues. |
| **Performance** | Tracks goal progress, collects 360-degree feedback summaries, and drafts performance reviews. |
| **Learning** | Identifies skill gaps, recommends courses and training paths, and tracks certification status. |
| **Engagement** | Designs pulse surveys, analyzes employee sentiment from feedback, and flags retention risk. |
| **Payroll** | Validates overtime calculations, summarizes benefits elections, and checks tax compliance by jurisdiction. |
| **Offboarding** | Conducts exit interview analysis, coordinates knowledge transfer plans, and manages access revocation checklists. |

## API Endpoints

- `GET /health` - Health check
- `GET /api/v1/kernel/status` - Kernel and agent status
- `POST /api/v1/kernel/pipeline` - Execute a multi-agent pipeline
- `POST /api/v1/hr/onboarding` - Onboarding agent
- `POST /api/v1/hr/policy` - Policy agent
- `POST /api/v1/hr/performance` - Performance agent
- `POST /api/v1/hr/learning` - Learning agent
- `POST /api/v1/hr/engagement` - Engagement agent
- `POST /api/v1/hr/payroll` - Payroll agent
- `POST /api/v1/hr/offboarding` - Offboarding agent

## How to Run

### Local

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Docker

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`. Dashboard at `http://localhost:8000/dashboard`. OpenAPI docs at `http://localhost:8000/docs`.

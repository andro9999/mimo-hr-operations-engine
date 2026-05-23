"""MiMo HR Operations Engine - FastAPI Application."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from config.settings import settings
from app.kernel.agent_kernel import AgentKernel
from app.agents.onboarding_agent import OnboardingAgent
from app.agents.policy_agent import PolicyAgent
from app.agents.performance_agent import PerformanceAgent
from app.agents.learning_agent import LearningAgent
from app.agents.engagement_agent import EngagementAgent
from app.agents.payroll_agent import PayrollAgent
from app.agents.offboarding_agent import OffboardingAgent
from app.routers.hr import router as hr_router

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

kernel: AgentKernel | None = None


def _init_kernel() -> AgentKernel:
    k = AgentKernel()
    k.register_agent("onboarding", OnboardingAgent(k))
    k.register_agent("policy", PolicyAgent(k))
    k.register_agent("performance", PerformanceAgent(k))
    k.register_agent("learning", LearningAgent(k))
    k.register_agent("engagement", EngagementAgent(k))
    k.register_agent("payroll", PayrollAgent(k))
    k.register_agent("offboarding", OffboardingAgent(k))
    return k


@asynccontextmanager
async def lifespan(app: FastAPI):
    global kernel
    kernel = _init_kernel()
    logger.info("AgentKernel initialized with %d agents", len(kernel.list_agents()))
    yield
    logger.info("Shutting down")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hr_router, prefix="/api/v1/hr")


@app.get("/health")
async def health():
    return {"status": "healthy", "service": settings.app_name, "version": settings.app_version}


@app.get("/api/v1/kernel/status")
async def kernel_status():
    if kernel is None:
        return {"status": "not_initialized"}
    return kernel.get_status()


@app.post("/api/v1/kernel/pipeline")
async def run_pipeline(body: dict):
    if kernel is None:
        return {"error": "Kernel not initialized"}
    steps = body.get("steps", [])
    result = await kernel.execute_pipeline(steps)
    return {
        "pipeline_id": result.pipeline_id,
        "status": result.status,
        "total_duration_ms": result.total_duration_ms,
        "steps": result.steps,
    }


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    import os
    dashboard_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dashboard", "index.html")
    with open(dashboard_path) as f:
        return HTMLResponse(content=f.read())

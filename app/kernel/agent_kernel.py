"""AgentKernel: central orchestrator for HR agent pipeline execution."""

import asyncio
import logging
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable

logger = logging.getLogger(__name__)


@dataclass
class AgentRecord:
    name: str
    agent: Any
    registered_at: float = field(default_factory=time.time)
    executions: int = 0
    last_status: str = "idle"


@dataclass
class PipelineResult:
    pipeline_id: str
    steps: list[dict]
    total_duration_ms: float
    status: str


class EventBus:
    """Simple in-process pub/sub event bus."""

    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable]] = defaultdict(list)

    def subscribe(self, event_type: str, handler: Callable) -> None:
        self._subscribers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler: Callable) -> None:
        if handler in self._subscribers[event_type]:
            self._subscribers[event_type].remove(handler)

    async def publish(self, event_type: str, data: dict) -> None:
        for handler in self._subscribers.get(event_type, []):
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(data)
                else:
                    handler(data)
            except Exception:
                logger.exception("Event handler error for %s", event_type)

    @property
    def subscriptions(self) -> dict[str, int]:
        return {k: len(v) for k, v in self._subscribers.items()}


class AgentKernel:
    """Central kernel that registers agents, routes tasks, and orchestrates pipelines."""

    def __init__(self) -> None:
        self.event_bus = EventBus()
        self._agents: dict[str, AgentRecord] = {}
        self._started_at: float | None = None
        logger.info("AgentKernel initialized")

    def register_agent(self, name: str, agent: Any) -> None:
        if name in self._agents:
            raise ValueError(f"Agent '{name}' is already registered")
        self._agents[name] = AgentRecord(name=name, agent=agent)
        logger.info("Registered agent: %s", name)

    def get_agent(self, name: str) -> Any:
        rec = self._agents.get(name)
        if rec is None:
            raise KeyError(f"Agent '{name}' not found")
        return rec.agent

    def list_agents(self) -> list[str]:
        return list(self._agents.keys())

    async def execute_agent(self, agent_name: str, task: dict) -> dict:
        rec = self._agents.get(agent_name)
        if rec is None:
            return {"error": f"Agent '{agent_name}' not found"}
        rec.last_status = "running"
        await self.event_bus.publish("agent.start", {"agent": agent_name, "task": task})
        start = time.time()
        try:
            result = await rec.agent.execute(task)
            rec.executions += 1
            rec.last_status = "success"
            duration = (time.time() - start) * 1000
            await self.event_bus.publish("agent.complete", {
                "agent": agent_name,
                "duration_ms": round(duration, 2),
            })
            return {"status": "success", "agent": agent_name, "duration_ms": round(duration, 2), "result": result}
        except Exception as exc:
            rec.last_status = "error"
            await self.event_bus.publish("agent.error", {"agent": agent_name, "error": str(exc)})
            return {"status": "error", "agent": agent_name, "error": str(exc)}

    async def execute_pipeline(self, steps: list[dict]) -> PipelineResult:
        """Execute a sequence of agent tasks.

        Each step: {"agent": "<name>", "task": {...}}
        Later steps can reference earlier results via context accumulation.
        """
        pipeline_id = uuid.uuid4().hex[:12]
        await self.event_bus.publish("pipeline.start", {"pipeline_id": pipeline_id, "steps": len(steps)})
        results: list[dict] = []
        start = time.time()
        overall_status = "success"

        for i, step in enumerate(steps):
            agent_name = step["agent"]
            task = step.get("task", {})
            task["pipeline_context"] = [r for r in results]
            task["step_index"] = i
            result = await self.execute_agent(agent_name, task)
            results.append(result)
            if result.get("status") == "error":
                overall_status = "partial"
                break

        duration = (time.time() - start) * 1000
        pipeline_result = PipelineResult(
            pipeline_id=pipeline_id,
            steps=results,
            total_duration_ms=round(duration, 2),
            status=overall_status,
        )
        await self.event_bus.publish("pipeline.complete", {
            "pipeline_id": pipeline_id,
            "status": overall_status,
            "duration_ms": round(duration, 2),
        })
        return pipeline_result

    def get_status(self) -> dict:
        return {
            "kernel": "running",
            "agent_count": len(self._agents),
            "agents": {
                name: {
                    "executions": rec.executions,
                    "last_status": rec.last_status,
                    "registered_at": rec.registered_at,
                }
                for name, rec in self._agents.items()
            },
            "event_bus_subscriptions": self.event_bus.subscriptions,
        }

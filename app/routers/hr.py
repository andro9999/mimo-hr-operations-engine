"""HR API Router - routes for all 7 agents."""

from fastapi import APIRouter, Request

router = APIRouter()


def _get_kernel(request: Request):
    from app.main import kernel
    return kernel


@router.post("/onboarding")
async def onboarding(body: dict, request: Request):
    kernel = _get_kernel(request)
    if kernel is None:
        return {"error": "Kernel not initialized"}
    return await kernel.execute_agent("onboarding", body)


@router.post("/policy")
async def policy(body: dict, request: Request):
    kernel = _get_kernel(request)
    if kernel is None:
        return {"error": "Kernel not initialized"}
    return await kernel.execute_agent("policy", body)


@router.post("/performance")
async def performance(body: dict, request: Request):
    kernel = _get_kernel(request)
    if kernel is None:
        return {"error": "Kernel not initialized"}
    return await kernel.execute_agent("performance", body)


@router.post("/learning")
async def learning(body: dict, request: Request):
    kernel = _get_kernel(request)
    if kernel is None:
        return {"error": "Kernel not initialized"}
    return await kernel.execute_agent("learning", body)


@router.post("/engagement")
async def engagement(body: dict, request: Request):
    kernel = _get_kernel(request)
    if kernel is None:
        return {"error": "Kernel not initialized"}
    return await kernel.execute_agent("engagement", body)


@router.post("/payroll")
async def payroll(body: dict, request: Request):
    kernel = _get_kernel(request)
    if kernel is None:
        return {"error": "Kernel not initialized"}
    return await kernel.execute_agent("payroll", body)


@router.post("/offboarding")
async def offboarding(body: dict, request: Request):
    kernel = _get_kernel(request)
    if kernel is None:
        return {"error": "Kernel not initialized"}
    return await kernel.execute_agent("offboarding", body)

from fastapi import APIRouter, HTTPException, Query, Request

router = APIRouter()

@router.get("/metrics/latest")
def get_latest_metrics(request: Request):
    repository = request.app.state.snapshot_repository

    snapshot = repository.get_latest_snapshot()

    if snapshot is None:
        raise HTTPException(
            status_code = 404,
            detail = "No metrics snapshot available",
            )
    return snapshot

@router.get("/metrics/history")
def get_metrics_history(
    request: Request,
    limit: int = Query(default=10, ge=1, le=100)
    ):
    repository = request.app.state.snapshot_repository

    return repository.get_recent_snapshots(limit=limit)

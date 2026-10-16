from fastapi import APIRouter, Query, Request

router = APIRouter()

@router.get("/errors")
def get_recent_errors(
    request: Request,
    limit: int = Query(default=10, ge=1, le=100),
    ):
    repository = request.app.state.error_repository
    return repository.get_recent_errors(limit=limit)

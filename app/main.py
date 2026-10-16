import logging
import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.init_db import create_tables
from app.collector.system_collector import SystemCollector
from app.core.config import settings
from app.repository.sql_snapshot_repository import SQLSnapshotRepository
from app.scheduler.scheduler import MonitoringScheduler
from app.services.metrics_service import MetricsService
from app.services.monitoring_service import MonitoringService
from app.repository.sql_error_repository import SQLErrorRepository

from app.api.routes.health import router as health_router
from app.api.routes.metrics import router as metrics_router
from app.api.routes.errors import router as errors_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_repositories():
    return SQLSnapshotRepository(), SQLErrorRepository()



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure database tables exist before monitoring starts.
    create_tables()
    #create shared application dependencies
    collector = SystemCollector()
    metrics_service = MetricsService()
    snapshot_repository, error_repository = app.state.repository_factory()

    monitoring_service = MonitoringService(
        collector = collector,
        metrics_service=metrics_service,
        snapshot_repository =  snapshot_repository, error_repository =  error_repository,
        )

    scheduler = MonitoringScheduler(
        monitoring_service = monitoring_service,
        interval_seconds = settings.monitoring_interval_seconds,
        )

    scheduler_thread = threading.Thread(
        target = scheduler.run_forever,
        name = "monitoring-scheduler",
        daemon = True,
        )

    #Make dependencies available to API routes
    app.state.collector = collector
    app.state.metrics_service = metrics_service
    app.state.snapshot_repository = snapshot_repository
    app.state.monitoring_service = monitoring_service
    app.state.scheduler = scheduler
    app.state.error_repository = error_repository

    scheduler_thread.start()
    logger.info("Monitoring scheduler started")

    try:
        yield
    finally:
        scheduler.stop()
        scheduler_thread.join(timeout=5)
        logger.info("Monitoring scheduler shutdown requested")

app = FastAPI(
    title = "System Monitoring API",
    lifespan = lifespan,
    )
app.state.repository_factory = create_repositories
app.include_router(health_router)
app.include_router(metrics_router)
app.include_router(errors_router)

@app.get("/")
def root():
    return {"message": "System Monitoring API is running"}



import logging
import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.collector.system_collector import SystemCollector
from app.core.config import settings
from app.repository.snapshot_repository import SnapshotRepository
from app.scheduler.scheduler import MonitoringScheduler
from app.services.metrics_service import MetricsService
from app.services.monitoring_service import MonitoringService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    #create shared application dependencies
    collector = SystemCollector()
    metrics_service = MetricsService()
    snapshot_repository = SnapshotRepository()

    monitoring_service = MonitoringService(
        collector = collector,
        metrics_service=metrics_service,
        snapshot_repository=snapshot_repository,
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

    scheduler_thread.start()
    logger.info("Monitoring scheduler started")

    try:
        yield
    finally:
        scheduler.stop()
        scheduler_thread.join(timeout=5)
        logger.info("Monitoring scheduler shutdown requested")

app = FastAPI(
    title = "Job Processing & System Monitoring API",
    lifespan = lifespan,
    )

@app.get("/")
def root():
    return {"message": "System Monitoring API is running"}



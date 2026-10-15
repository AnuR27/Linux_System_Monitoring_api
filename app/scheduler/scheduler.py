import logging
import threading
import time

from app.services.monitoring_service import MonitoringService

logger = logging.getLogger(__name__)

class MonitoringScheduler:
    def __init__(
        self,
        monitoring_service: MonitoringService,
        interval_seconds: float = 30.0,
        ):
        if interval_seconds <=0:
            raise ValueError("interval seconds must be greater than 0")

        self.monitoring_service = monitoring_service
        self.interval_seconds = interval_seconds
        self.stop_event = threading.Event()

    def run_forever(self) -> None:
        while not self.stop_event.is_set():
            try:
                snapshot, errors = self.monitoring_service.run_cycle()

                logger.info(
                    "Monitoring cycle completed: cycle_id=%s,"
                    "status=%s, severity=%s, errors=%s",
                    snapshot.cycle_id,
                    snapshot.status,
                    snapshot.severity,
                    len(errors),
                    )
            except Exception:
                logger.exception("Monitoring cycle failed unexpectedly")

            if self.stop_event.wait(self.interval_seconds):
                break

    def stop(self) -> None:
        self.stop_event.set()

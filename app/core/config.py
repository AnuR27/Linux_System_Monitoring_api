import os

class Settings:
    def __init__(self):
        self.monitoring_interval_seconds = float(
            os.getenv("MONITORING_INTERVAL_SECONDS", "30")
            )


settings = Settings()

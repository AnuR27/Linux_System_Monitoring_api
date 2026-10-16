import os

class Settings:
    def __init__(self):
        self.monitoring_interval_seconds = float(
            os.getenv("MONITORING_INTERVAL_SECONDS", "30")
            )

        self.database_url = os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg://monitoring:monitoring_dev_password@localhost:5432/monitoring",
            )


settings = Settings()

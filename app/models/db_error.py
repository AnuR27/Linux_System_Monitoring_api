from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

class ErrorDB(Base):
    __tablename__ = "monitoring_errors"

    error_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )
    cycle_id: Mapped[int] = mapped_column(
        ForeignKey("metric_snapshots.cycle_id"),
        nullable=False,
        index=True,
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    error_code: Mapped[str] = mapped_column(String(100), nullable=False)
    message: Mapped[str] = mapped_column(String(1000), nullable=False)

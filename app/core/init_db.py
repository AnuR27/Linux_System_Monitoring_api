from app.core.database import Base, engine
from app.models.db_snapshot import SnapshotDB
from app.models.db_error import ErrorDB

def create_tables() -> None:
    Base.metadata.create_all(bind=engine)

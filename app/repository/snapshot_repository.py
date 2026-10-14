from app.models.snapshot import Snapshot, SnapshotDraft

class SnapshotRepository:
    def __init__(self):
        self.snapshots_by_cycle: dict[int, Snapshot] = {}
        self.cycle_order: list[int] = []
        self._next_cycle_id: int = 1


    def save_snapshot(self, snapshot: SnapshotDraft) -> Snapshot:
        cycle_id = self._next_cycle_id
        self._next_cycle_id += 1

        saved_snapshot = Snapshot(
            cycle_id=cycle_id,
            **snapshot.model_dump(),
        )

        self.snapshots_by_cycle[cycle_id] = saved_snapshot
        self.cycle_order.append(cycle_id)

        return saved_snapshot


    def get_latest_snapshot(self) -> Snapshot | None:
        if not self.cycle_order:
            return None

        latest_cycle_id = self.cycle_order[-1]
        return self.snapshots_by_cycle[latest_cycle_id]

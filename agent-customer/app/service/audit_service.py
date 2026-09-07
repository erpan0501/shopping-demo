import sqlite3
from contextlib import closing
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path


@dataclass(frozen=True)
class ChatAuditEvent:
    event_id: int
    session_id: str
    user_id: int | None
    source: str
    outcome: str
    status_code: int
    elapsed_ms: float
    error_code: str | None
    created_at: str


@dataclass(frozen=True)
class ChatOperationsSummary:
    window_minutes: int
    total_requests: int
    completed_requests: int
    failed_requests: int
    rate_limited_requests: int
    average_elapsed_ms: float
    max_elapsed_ms: float
    source_counts: dict[str, int]
    error_counts: dict[str, int]


class AuditService:
    """仅记录排障所需元数据，不保存问题、回复、订单号或手机号。"""

    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        self._initialize_database()

    def record_chat(
        self,
        *,
        session_id: str,
        user_id: int | None,
        source: str,
        outcome: str,
        status_code: int,
        elapsed_ms: float,
        error_code: str | None = None,
    ) -> None:
        created_at = datetime.now().astimezone().isoformat(timespec="seconds")
        with closing(self._connect()) as connection, connection:
            connection.execute(
                """
                INSERT INTO chat_audit_event (
                    session_id, user_id, source, outcome, status_code,
                    elapsed_ms, error_code, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session_id,
                    user_id,
                    source,
                    outcome,
                    status_code,
                    elapsed_ms,
                    error_code,
                    created_at,
                ),
            )

    def list_events(self, *, limit: int) -> list[ChatAuditEvent]:
        with closing(self._connect()) as connection:
            rows = connection.execute(
                "SELECT * FROM chat_audit_event ORDER BY event_id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [self._to_event(row) for row in rows]

    def get_operations_summary(self, *, window_minutes: int) -> ChatOperationsSummary:
        cutoff = (
            datetime.now().astimezone() - timedelta(minutes=window_minutes)
        ).isoformat(timespec="seconds")
        with closing(self._connect()) as connection:
            totals = connection.execute(
                """
                SELECT
                    COUNT(*) AS total_requests,
                    SUM(CASE WHEN outcome = 'completed' THEN 1 ELSE 0 END) AS completed_requests,
                    SUM(CASE WHEN outcome = 'failed' THEN 1 ELSE 0 END) AS failed_requests,
                    SUM(CASE WHEN source = 'rate_limit' THEN 1 ELSE 0 END) AS rate_limited_requests,
                    COALESCE(AVG(elapsed_ms), 0) AS average_elapsed_ms,
                    COALESCE(MAX(elapsed_ms), 0) AS max_elapsed_ms
                FROM chat_audit_event
                WHERE created_at >= ?
                """,
                (cutoff,),
            ).fetchone()
            source_rows = connection.execute(
                """
                SELECT source, COUNT(*) AS count
                FROM chat_audit_event
                WHERE created_at >= ?
                GROUP BY source
                """,
                (cutoff,),
            ).fetchall()
            error_rows = connection.execute(
                """
                SELECT error_code, COUNT(*) AS count
                FROM chat_audit_event
                WHERE created_at >= ? AND error_code IS NOT NULL
                GROUP BY error_code
                ORDER BY count DESC, error_code ASC
                LIMIT 20
                """,
                (cutoff,),
            ).fetchall()

        return ChatOperationsSummary(
            window_minutes=window_minutes,
            total_requests=totals["total_requests"],
            completed_requests=totals["completed_requests"] or 0,
            failed_requests=totals["failed_requests"] or 0,
            rate_limited_requests=totals["rate_limited_requests"] or 0,
            average_elapsed_ms=round(totals["average_elapsed_ms"], 2),
            max_elapsed_ms=round(totals["max_elapsed_ms"], 2),
            source_counts={row["source"]: row["count"] for row in source_rows},
            error_counts={row["error_code"]: row["count"] for row in error_rows},
        )

    def _initialize_database(self) -> None:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        with closing(self._connect()) as connection, connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_audit_event (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    user_id INTEGER,
                    source TEXT NOT NULL,
                    outcome TEXT NOT NULL,
                    status_code INTEGER NOT NULL,
                    elapsed_ms REAL NOT NULL,
                    error_code TEXT,
                    created_at TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_chat_audit_event_created_at
                ON chat_audit_event (created_at DESC)
                """
            )

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    @staticmethod
    def _to_event(row: sqlite3.Row) -> ChatAuditEvent:
        return ChatAuditEvent(
            event_id=row["event_id"],
            session_id=row["session_id"],
            user_id=row["user_id"],
            source=row["source"],
            outcome=row["outcome"],
            status_code=row["status_code"],
            elapsed_ms=row["elapsed_ms"],
            error_code=row["error_code"],
            created_at=row["created_at"],
        )

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from uuid import uuid4


@dataclass(frozen=True)
class HandoffTicket:
    ticket_id: str
    created_at: str


@dataclass(frozen=True)
class HandoffTicketRecord:
    ticket_id: str
    session_id: str
    user_id: int | None
    question: str
    conversation: list[tuple[str, str]]
    status: str
    created_at: str
    updated_at: str
    handled_by: str | None


class HandoffService:
    """人工客服工单的本地持久化实现。

    真实部署时可用 CRM 或工单系统替换本服务，对 Agent 的调用方式不变。
    """

    def __init__(self, database_path: Path):
        self.database_path = database_path
        self._initialize_database()

    def create_ticket(
        self,
        *,
        session_id: str,
        user_id: int | None,
        question: str,
        history: list[tuple[str, str]],
    ) -> HandoffTicket:
        created_at = datetime.now().astimezone().isoformat(timespec="seconds")
        ticket_id = f"CS-{datetime.now():%Y%m%d}-{uuid4().hex[:8].upper()}"

        with sqlite3.connect(self.database_path) as connection:
            connection.execute(
                """
                INSERT INTO handoff_ticket (
                    ticket_id, session_id, user_id, question,
                    conversation_json, status, created_at
                    , updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    ticket_id,
                    session_id,
                    user_id,
                    question,
                    json.dumps(history, ensure_ascii=False),
                    "waiting_human",
                    created_at,
                    created_at,
                ),
            )

        return HandoffTicket(ticket_id=ticket_id, created_at=created_at)

    def list_tickets(
        self,
        *,
        status: str | None,
        limit: int,
    ) -> list[HandoffTicketRecord]:
        query = "SELECT * FROM handoff_ticket"
        params: list[object] = []
        if status:
            query += " WHERE status = ?"
            params.append(status)
        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)

        with self._connect() as connection:
            rows = connection.execute(query, params).fetchall()
        return [self._to_record(row) for row in rows]

    def get_ticket(self, ticket_id: str) -> HandoffTicketRecord | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM handoff_ticket WHERE ticket_id = ?",
                (ticket_id,),
            ).fetchone()
        return self._to_record(row) if row else None

    def update_ticket_status(
        self,
        *,
        ticket_id: str,
        status: str,
        handled_by: str,
    ) -> HandoffTicketRecord | None:
        updated_at = datetime.now().astimezone().isoformat(timespec="seconds")
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE handoff_ticket
                SET status = ?, handled_by = ?, updated_at = ?
                WHERE ticket_id = ?
                """,
                (status, handled_by, updated_at, ticket_id),
            )
            if cursor.rowcount == 0:
                return None
        return self.get_ticket(ticket_id)

    def _initialize_database(self) -> None:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS handoff_ticket (
                    ticket_id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    user_id INTEGER,
                    question TEXT NOT NULL,
                    conversation_json TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    handled_by TEXT
                )
                """
            )
            columns = {
                row[1]
                for row in connection.execute("PRAGMA table_info(handoff_ticket)")
            }
            if "updated_at" not in columns:
                connection.execute(
                    "ALTER TABLE handoff_ticket ADD COLUMN updated_at TEXT"
                )
                connection.execute(
                    "UPDATE handoff_ticket SET updated_at = created_at"
                )
            if "handled_by" not in columns:
                connection.execute(
                    "ALTER TABLE handoff_ticket ADD COLUMN handled_by TEXT"
                )

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    @staticmethod
    def _to_record(row: sqlite3.Row) -> HandoffTicketRecord:
        conversation = [tuple(message) for message in json.loads(row["conversation_json"])]
        return HandoffTicketRecord(
            ticket_id=row["ticket_id"],
            session_id=row["session_id"],
            user_id=row["user_id"],
            question=row["question"],
            conversation=conversation,
            status=row["status"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            handled_by=row["handled_by"],
        )

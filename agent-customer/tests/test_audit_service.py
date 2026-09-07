import tempfile
import unittest
from pathlib import Path

from app.service.audit_service import AuditService


class AuditServiceTests(unittest.TestCase):
    def test_records_metadata_without_chat_content_columns(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            service = AuditService(Path(temporary_directory) / "audit.db")
            service.record_chat(
                session_id="session-1",
                user_id=1,
                source="order",
                outcome="completed",
                status_code=200,
                elapsed_ms=12.5,
            )

            events = service.list_events(limit=10)

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].session_id, "session-1")
        self.assertEqual(events[0].source, "order")
        self.assertEqual(events[0].status_code, 200)
        self.assertIsNone(events[0].error_code)

    def test_summarizes_operational_metadata_by_window(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            service = AuditService(Path(temporary_directory) / "audit.db")
            service.record_chat(
                session_id="session-1",
                user_id=1,
                source="faq",
                outcome="completed",
                status_code=200,
                elapsed_ms=10,
            )
            service.record_chat(
                session_id="session-2",
                user_id=1,
                source="rate_limit",
                outcome="rejected",
                status_code=429,
                elapsed_ms=2,
                error_code="RATE_LIMITED",
            )
            service.record_chat(
                session_id="session-3",
                user_id=1,
                source="java",
                outcome="failed",
                status_code=503,
                elapsed_ms=20,
                error_code="JAVA_CIRCUIT_OPEN",
            )

            summary = service.get_operations_summary(window_minutes=60)

        self.assertEqual(summary.total_requests, 3)
        self.assertEqual(summary.completed_requests, 1)
        self.assertEqual(summary.failed_requests, 1)
        self.assertEqual(summary.rate_limited_requests, 1)
        self.assertEqual(summary.source_counts, {"faq": 1, "java": 1, "rate_limit": 1})
        self.assertEqual(summary.error_counts["RATE_LIMITED"], 1)


if __name__ == "__main__":
    unittest.main()

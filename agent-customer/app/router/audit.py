from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, ConfigDict, Field

from ..service.audit_service import ChatAuditEvent, ChatOperationsSummary
from .faq import audit_service
from .staff import require_staff_access


router = APIRouter(prefix="/internal/audit-events", tags=["内部审计"])
class AuditEventResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    event_id: int = Field(alias="eventId")
    session_id: str = Field(alias="sessionId")
    user_id: int | None = Field(alias="userId")
    source: str
    outcome: str
    status_code: int = Field(alias="statusCode")
    elapsed_ms: float = Field(alias="elapsedMs")
    error_code: str | None = Field(alias="errorCode")
    created_at: str = Field(alias="createdAt")


class OperationsSummaryResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    window_minutes: int = Field(alias="windowMinutes")
    total_requests: int = Field(alias="totalRequests")
    completed_requests: int = Field(alias="completedRequests")
    failed_requests: int = Field(alias="failedRequests")
    rate_limited_requests: int = Field(alias="rateLimitedRequests")
    average_elapsed_ms: float = Field(alias="averageElapsedMs")
    max_elapsed_ms: float = Field(alias="maxElapsedMs")
    source_counts: dict[str, int] = Field(alias="sourceCounts")
    error_counts: dict[str, int] = Field(alias="errorCounts")


@router.get("", response_model=list[AuditEventResponse], dependencies=[Depends(require_staff_access)])
def list_audit_events(
    limit: int = Query(default=50, ge=1, le=200),
) -> list[AuditEventResponse]:
    return [_to_response(event) for event in audit_service.list_events(limit=limit)]


@router.get(
    "/summary",
    response_model=OperationsSummaryResponse,
    dependencies=[Depends(require_staff_access)],
)
def get_operations_summary(
    minutes: int = Query(default=60, ge=1, le=1440),
) -> OperationsSummaryResponse:
    return _to_summary_response(
        audit_service.get_operations_summary(window_minutes=minutes),
    )


def _to_response(event: ChatAuditEvent) -> AuditEventResponse:
    return AuditEventResponse(
        eventId=event.event_id,
        sessionId=event.session_id,
        userId=event.user_id,
        source=event.source,
        outcome=event.outcome,
        statusCode=event.status_code,
        elapsedMs=event.elapsed_ms,
        errorCode=event.error_code,
        createdAt=event.created_at,
    )


def _to_summary_response(summary: ChatOperationsSummary) -> OperationsSummaryResponse:
    return OperationsSummaryResponse(
        windowMinutes=summary.window_minutes,
        totalRequests=summary.total_requests,
        completedRequests=summary.completed_requests,
        failedRequests=summary.failed_requests,
        rateLimitedRequests=summary.rate_limited_requests,
        averageElapsedMs=summary.average_elapsed_ms,
        maxElapsedMs=summary.max_elapsed_ms,
        sourceCounts=summary.source_counts,
        errorCounts=summary.error_counts,
    )

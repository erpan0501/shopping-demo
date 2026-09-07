import hmac
from typing import Literal

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from pydantic import BaseModel, Field

from ..config import Settings, get_settings
from ..service.handoff_service import HandoffService, HandoffTicketRecord

router = APIRouter(prefix="/internal/tickets", tags=["内部客服工单"])
settings = get_settings()
handoff_service = HandoffService(settings.handoff_db_path)


class ConversationMessage(BaseModel):
    role: str
    content: str


class TicketSummary(BaseModel):
    ticket_id: str = Field(alias="ticketId")
    user_id: int | None = Field(alias="userId")
    question: str
    status: str
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")
    handled_by: str | None = Field(alias="handledBy")


class TicketDetail(TicketSummary):
    session_id: str = Field(alias="sessionId")
    conversation: list[ConversationMessage]


class TicketStatusUpdate(BaseModel):
    status: Literal["processing", "resolved"]
    handled_by: str = Field(min_length=1, max_length=50, alias="handledBy")


def require_staff_access(
    x_staff_key: str | None = Header(default=None),
) -> None:
    if not settings.staff_api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="内部客服接口尚未配置 STAFF_API_KEY。",
        )
    if not x_staff_key or not hmac.compare_digest(x_staff_key, settings.staff_api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="内部客服访问密钥无效。",
        )


@router.get("", response_model=list[TicketSummary], dependencies=[Depends(require_staff_access)])
def list_tickets(
    ticket_status: Literal["waiting_human", "processing", "resolved"] | None = Query(
        default=None,
        alias="status",
    ),
    limit: int = Query(default=20, ge=1, le=100),
) -> list[TicketSummary]:
    return [_to_summary(ticket) for ticket in handoff_service.list_tickets(status=ticket_status, limit=limit)]


@router.get("/{ticket_id}", response_model=TicketDetail, dependencies=[Depends(require_staff_access)])
def get_ticket(ticket_id: str) -> TicketDetail:
    ticket = handoff_service.get_ticket(ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="工单不存在。")
    return _to_detail(ticket)


@router.patch("/{ticket_id}", response_model=TicketDetail, dependencies=[Depends(require_staff_access)])
def update_ticket(ticket_id: str, request: TicketStatusUpdate) -> TicketDetail:
    ticket = handoff_service.update_ticket_status(
        ticket_id=ticket_id,
        status=request.status,
        handled_by=request.handled_by,
    )
    if ticket is None:
        raise HTTPException(status_code=404, detail="工单不存在。")
    return _to_detail(ticket)


def _to_summary(ticket: HandoffTicketRecord) -> TicketSummary:
    return TicketSummary(
        ticketId=ticket.ticket_id,
        userId=ticket.user_id,
        question=ticket.question,
        status=ticket.status,
        createdAt=ticket.created_at,
        updatedAt=ticket.updated_at,
        handledBy=ticket.handled_by,
    )


def _to_detail(ticket: HandoffTicketRecord) -> TicketDetail:
    return TicketDetail(
        **_to_summary(ticket).model_dump(by_alias=True),
        sessionId=ticket.session_id,
        conversation=[
            ConversationMessage(role=role, content=content)
            for role, content in ticket.conversation
        ],
    )

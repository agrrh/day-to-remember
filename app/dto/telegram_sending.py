from pydantic import BaseModel, Field

from app.dto.abstract_message import AbstractMessageDTO


class TelegramSendingDTO(BaseModel):
    """Pack of abstract messages and an address to send those to."""

    chat_id: int
    messages: list[AbstractMessageDTO] = Field(default_factory=list)

from pydantic import BaseModel, Field

from app.dto.abstract_message import AbstractMessageDTO


class TelegramSendingDTO(BaseModel):
    chat_id: int
    messages: list[AbstractMessageDTO] = Field(default_factory=list)

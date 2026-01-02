from pydantic import BaseModel, Field

from app.dto.abstract_message import AbstractMessage


class TelegramShipment(BaseModel):
    user_id: int
    messages: list[AbstractMessage] = Field(default_factory=list)

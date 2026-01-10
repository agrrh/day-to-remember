from typing import Any, override

from pydantic import BaseModel, ConfigDict
from telebot.types import CallbackQuery as TgCallbackQuery


class TelegramCallbackDTO(BaseModel):
    """Telegram Callback container, with a little bit knowledge about entities, stored in "data" field."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    raw_callback: TgCallbackQuery

    data: str | None = None

    @override
    def model_post_init(self, context: Any) -> None:
        self.data = self.raw_callback.data

    def get_data_parts(self) -> tuple[str, str]:
        """Get Button data field, possibly prefixed with some string."""
        if self.data is None:
            # TODO: Produce explicit error
            raise ValueError

        prefix, value = self.data.split("_")

        return (prefix, value)

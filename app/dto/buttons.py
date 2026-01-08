from itertools import batched
from typing import List

from pydantic import BaseModel
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.domain.fact import Fact


class ButtonDTO(BaseModel):
    """Single option, later to be rendered as Button."""

    data: str
    label: str

    def load_from_fact(self, fact: Fact):
        """Load domain Fact as a Button."""

        self.data = fact.uuid
        self.label = "{text}".format(**fact.model_dump())

    def get_data_maybe_prefixed(self, prefix: str | None = None) -> str:
        """Get Button data field, possibly prefixed with some string."""
        return self.data if prefix is None else "_".join((prefix, self.data))


class ButtonsDTO(BaseModel):
    """Stores options group, later to be rendered as buttons."""

    buttons: List[ButtonDTO]

    # Telegram stuff

    # Makes buttons "data" field to be prepended with "{prefix}_" to ease callback handling
    tg_prefix: str | None = None
    # Buttons per row
    tg_width: int = 3

    def to_telegram_markup(self) -> InlineKeyboardMarkup:
        """Produce Telegram keyboard."""
        markup = InlineKeyboardMarkup()
        markup.row_width = self.tg_width

        for row in batched(self.buttons, self.tg_width):
            buttons_row = []
            for button in row:
                data = button.get_data_maybe_prefixed(self.tg_prefix)

                tg_button = InlineKeyboardButton(button.label, callback_data=data)
                buttons_row.append(tg_button)

            markup.add(*buttons_row)

        return markup

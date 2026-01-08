from pydantic import BaseModel


class AbstractMessageDTO(BaseModel):
    """Container for Message, abstract from channel type to be sent on (messenger, email, whatever)."""

    text: str | None = None
    media_url: str | None = None
    reaction_emoji: str | None = None

    def to_telegram_args(self) -> dict:
        """Convert to dict with args capable with `telebot.send_message`."""
        tg_message = {}

        if self.media_url:
            tg_message["photo"] = self.media_url
            tg_message["caption"] = self.text
        elif self.reaction_emoji:
            tg_message["reaction_emoji"] = self.reaction_emoji
        else:
            tg_message["text"] = self.text

        return tg_message

    def measure_read_time(self) -> float:
        """Roughly measure time needed to read corresponding text."""
        if self.text is None:
            return 1

        words = self.text.split()
        words = filter(None, words)

        # Real world reading speed is about 3 words per second
        base = len(list(words)) / 3

        # Add few moments to take a look at image, if attached
        extra = 5 if self.media_url else 0

        return base + extra

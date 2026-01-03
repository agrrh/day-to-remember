from pydantic import BaseModel


class AbstractMessage(BaseModel):
    text: str
    media_url: str = ""

    def to_telegram_args(self) -> dict:
        """Convert to dict with args capable with `telebot.send_message`."""
        tg_message = {}

        if self.media_url:
            tg_message["photo"] = self.media_url
            tg_message["caption"] = self.text
        else:
            tg_message["text"] = self.text

        return tg_message

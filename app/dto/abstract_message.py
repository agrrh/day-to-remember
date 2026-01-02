from pydantic import BaseModel


class AbstractMessage(BaseModel):
    text: str
    media_url: str = ""

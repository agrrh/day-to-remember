class BaseError(Exception):
    """Base application error."""

    def __init__(self, *, message: str | None = None, **context) -> None:
        self.message = self.__doc__ or message
        self.context = context

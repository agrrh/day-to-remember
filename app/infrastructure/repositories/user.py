import copy

from telebot.types import Message as TgMessage

from app.domain.user import User
from app.infrastructure.utils.errors import BaseError
from app.infrastructure.external.grist_adapter import GristAdapter


class ErrorUserNotFound(BaseError):
    """User not found in storage."""


class ErrorMultipleUsersFound(BaseError):
    """Multiple users found by same field, which supposed to be unique."""


class UserRepository:
    def __init__(self, grist: GristAdapter):
        self.adapter = copy.copy(grist)
        self.adapter.table_id = "Users"

    def create_from_telegram_message(self, message: TgMessage) -> bool:
        name = (
            " ".join(
                filter(
                    None,
                    [
                        message.from_user.first_name,
                        message.from_user.last_name,
                    ],
                )
            )
            or ""
        )

        user = User(
            telegram_id=message.from_user.id,
            name=name,
        )

        self.adapter.create_record(user.dict())

    def get_by_telegram_message(self, message: TgMessage) -> User:
        users_found = self.adapter.get_records(
            filters={
                "telegram_id": message.from_user.id,
            }
        )

        match len(users_found):
            case 0:
                raise ErrorUserNotFound
            case 1:
                _u = (users_found[0])._asdict()
                user = User(**_u)
            case _:
                raise ErrorMultipleUsersFound

        return user

    def get_active_users(self) -> list[User]:
        users_found = self.adapter.get_records(filters={})

        return [u._asdict() for u in users_found]

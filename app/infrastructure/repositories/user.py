import copy

from telebot.types import Message as TgMessage

from app.domain.user import User
from app.infrastructure.external.grist_adapter import GristAdapter
from app.infrastructure.utils.errors import BaseError


class ErrorUserNotFound(BaseError):
    """User not found in storage."""


class ErrorMultipleUsersFound(BaseError):
    """Multiple users found by same field, which supposed to be unique."""


class UserRepository:
    """Interface for Users storage."""

    def __init__(self, grist: GristAdapter):
        self.adapter = copy.copy(grist)
        self.adapter.table_id = "Users"

    def create_from_telegram_message(self, message: TgMessage) -> bool:
        """Create User from incoming Telegram message."""

        # TODO: Add specific error for missing from_user information
        if not message.from_user:
            raise ValueError("Telegram message does not contain from_user information.")

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

        record_id = self.adapter.create_record(user.model_dump())

        return bool(record_id)

    def get_by_telegram_message(self, message: TgMessage) -> User:
        """Get User from database by given Telegram message."""

        # TODO: Add specific error for missing from_user information
        if not message.from_user:
            raise ValueError("Telegram message does not contain from_user information.")

        users_found = self.adapter.get_records(
            filters={
                "telegram_id": message.from_user.id,
            }
        )

        match len(users_found):
            case 0:
                raise ErrorUserNotFound
            case 1:
                _u = users_found[0]
                user = User(**_u)
            case _:
                raise ErrorMultipleUsersFound

        return user

    def get_active_users(self) -> list[User]:
        """List active Users."""

        # TODO: Add filter to select non-blocked Users only (also add "blocked" attribute)
        users_found = self.adapter.get_records(filters={})

        return [User(**_u) for _u in users_found]

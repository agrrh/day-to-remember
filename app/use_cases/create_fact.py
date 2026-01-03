from datetime import datetime

from telebot.types import Message as TgMessage

from app.domain.fact import Fact
from app.dto.abstract_message import AbstractMessage
from app.infrastructure.repositories.fact import FactRepository
from app.infrastructure.repositories.user import ErrorUserNotFound, UserRepository


class CreateFactUseCase:
    def __init__(
        self, user_repository: UserRepository, fact_repository: FactRepository
    ):
        self.fact_repository = fact_repository
        self.user_repository = user_repository

    def __call__(self, message: TgMessage) -> list[AbstractMessage]:
        # TODO: Move those to some DTO validation?
        if not message.text:
            raise ValueError("Message text could not be empty while creating Fact.")

        if not message.reply_to_message:
            raise ValueError("Message should be a reply while creating Fact.")

        try:
            user = self.user_repository.get_by_telegram_message(message)
        except ErrorUserNotFound:
            messages = [
                AbstractMessage(
                    text="Ой, я вас не узнаю! Повторите запуск бота через `/start`, пожалуйста."
                ),
            ]
            return messages
        except Exception:
            messages = [
                AbstractMessage(
                    text="Ой, что-то сломалось! Пожалуйста, попробуйте позже."
                ),
            ]
            return messages

        date_unix = message.reply_to_message.date

        fact = Fact(
            user_uuid=user.uuid,
            text=message.text,
            date=datetime.fromtimestamp(date_unix).date(),
        )

        try:
            self.fact_repository.save(fact)
        except Exception as e:
            print(e)
            messages = [
                AbstractMessage(
                    text="Ой, не могу сохранить событие! Пожалуйста, попробуйте позже."
                ),
            ]
            return messages

        # TODO: Make it possible to update older messages with some acks (e.g. add "Saved N facts :ok:")
        return []

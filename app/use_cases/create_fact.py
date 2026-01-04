from datetime import datetime

from telebot.types import Message as TgMessage

from app.domain.fact import Fact
from app.dto.abstract_message import AbstractMessageDTO
from app.dto.telegram_sending import TelegramSendingDTO
from app.infrastructure.repositories.fact import FactRepository
from app.infrastructure.repositories.user import ErrorUserNotFound, UserRepository


class CreateFactUseCase:
    def __init__(
        self, user_repository: UserRepository, fact_repository: FactRepository
    ):
        self.fact_repository = fact_repository
        self.user_repository = user_repository

    def __call__(self, message: TgMessage) -> TelegramSendingDTO:
        # TODO: Move those to some DTO validation?
        if message.text is None:
            raise ValueError("Message text could not be empty while creating Fact.")

        if message.reply_to_message is None:
            raise ValueError("Message should be a reply while creating Fact.")

        if message.from_user is None:
            raise ValueError("Message should have sender id.")

        sending = TelegramSendingDTO(chat_id=message.from_user.id)

        try:
            user = self.user_repository.get_by_telegram_message(message)
        except ErrorUserNotFound:
            sending.messages = [
                AbstractMessageDTO(
                    text="Ой, я вас не узнаю! Повторите запуск бота через `/start`, пожалуйста."
                ),
            ]
            return sending
        except Exception:
            sending.messages = [
                AbstractMessageDTO(
                    text="Ой, что-то сломалось! Пожалуйста, попробуйте позже."
                ),
            ]
            return sending

        date_unix = message.reply_to_message.date

        fact = Fact(
            user_uuid=user.uuid,
            text=message.text,
            date=datetime.fromtimestamp(date_unix).date(),
        )

        try:
            self.fact_repository.save(fact)
        except Exception:
            # TODO: Log error
            sending.messages = [
                AbstractMessageDTO(
                    text="Ой, не могу сохранить событие! Пожалуйста, попробуйте позже."
                ),
            ]
            return sending

        # TODO: Determine text emotion and select appropriate emoji from list of possible reactions
        #   https://core.telegram.org/bots/api#reactiontypeemoji
        sending.messages = [AbstractMessageDTO(reaction_emoji="✍")]

        return sending

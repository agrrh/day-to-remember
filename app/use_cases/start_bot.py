from telebot.types import Message

from app.dto.abstract_message import AbstractMessageDTO
from app.dto.telegram_sending import TelegramSendingDTO
from app.infrastructure.repositories.user import ErrorUserNotFound, UserRepository


class StartBotUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def __call__(self, message: Message) -> TelegramSendingDTO:
        if message.from_user is None:
            raise ValueError("Message should have sender id.")

        sending = TelegramSendingDTO(chat_id=message.from_user.id)

        try:
            _ = self.user_repository.get_by_telegram_message(message)

            # Return link to article for returning user
            sending.messages = [
                AbstractMessageDTO(text="Повторное: (link)"),
            ]
        except ErrorUserNotFound:
            _ = self.user_repository.create_from_telegram_message(message)

            # Return full intro
            # TODO: Add i18n
            sending.messages = [
                AbstractMessageDTO(
                    text="Привет!"
                    "\n\n"
                    "Я постараюсь в несколько сообщений объяснить, что это за бот."
                ),
                AbstractMessageDTO(
                    text="Бот будет периодически присылать тебе сообщения."
                    "\n\n"
                    "Просто рассказывай ему о том, что важного происходит в твоей жизни.",
                    media_url="AgACAgIAAxkBAAMraVaEYx2ERtY1VwOiTrd-t0CISwMAAjYRaxvmv7FKMCAzBLscrT0BAAMCAAN4AAM4BA",
                ),
                AbstractMessageDTO(
                    text="Также, по мере накопления записей, он будет предлагать выбрать самое важное событие."
                    "\n\n"
                    "Например, за неделю.",
                    media_url="AgACAgIAAxkBAAMsaVaEtcmKd7DUxsDDYBjr66tEUdkAAjgRaxvmv7FK587mFcn825gBAAMCAAN5AAM4BA",
                ),
                AbstractMessageDTO(
                    text="Потом за месяц, квартал, год ...",
                    media_url="AgACAgIAAxkBAAMtaVaFBDEu9JIOwMv21XFREg3e5RsAAj0Raxvmv7FKsKFnv0utS7UBAAMCAAN5AAM4BA",
                ),
                AbstractMessageDTO(
                    text="Что, в итоге, позволит отметить, в какие успехи было вложено твоё время!",
                    media_url="AgACAgIAAxkBAAM6aVaGOUoIXY_hPq1pT4JNandygykAAkcRaxvmv7FKlDVBFZwAAborAQADAgADeQADOAQ",
                ),
                AbstractMessageDTO(text="Удачного использования!"),
            ]

        return sending

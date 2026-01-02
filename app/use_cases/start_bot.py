from telebot.types import Message

from app.dto.abstract_message import AbstractMessage
from app.infrastructure.repositories.user import UserRepository, ErrorUserNotFound


class StartBotUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def __call__(self, message: Message) -> list[AbstractMessage]:
        try:
            _ = self.user_repository.get_by_telegram_message(message)

            # Return link to article for returning user
            messages = [
                AbstractMessage(text="Повторное: (link)"),
            ]
        except ErrorUserNotFound:
            _ = self.user_repository.create_from_telegram_message(message)

            # Return full intro
            # TODO: Add i18n
            messages = [
                AbstractMessage(text="Привет!" "\n\n" "Я постараюсь в несколько сообщений объяснить, что это за бот."),
                AbstractMessage(
                    text="Бот будет периодически присылать тебе сообщения."
                    "\n\n"
                    "Просто рассказывай ему о том, что важного происходит в твоей жизни.",
                    media_url="AgACAgIAAxkBAAMraVaEYx2ERtY1VwOiTrd-t0CISwMAAjYRaxvmv7FKMCAzBLscrT0BAAMCAAN4AAM4BA",
                ),
                AbstractMessage(
                    text="Также, по мере накопления записей, он будет предлагать выбрать самое важное событие."
                    "\n\n"
                    "Например, за неделю.",
                    media_url="AgACAgIAAxkBAAMsaVaEtcmKd7DUxsDDYBjr66tEUdkAAjgRaxvmv7FK587mFcn825gBAAMCAAN5AAM4BA",
                ),
                AbstractMessage(
                    text="Потом за месяц, квартал, год ...",
                    media_url="AgACAgIAAxkBAAMtaVaFBDEu9JIOwMv21XFREg3e5RsAAj0Raxvmv7FKsKFnv0utS7UBAAMCAAN5AAM4BA",
                ),
                AbstractMessage(
                    text="Что, в итоге, позволит отметить, в какие успехи было вложено твоё время!",
                    media_url="AgACAgIAAxkBAAM6aVaGOUoIXY_hPq1pT4JNandygykAAkcRaxvmv7FKlDVBFZwAAborAQADAgADeQADOAQ",
                ),
                AbstractMessage(text="Удачного использования!"),
            ]

        return messages

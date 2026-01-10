import datetime
import locale

from app.dto.abstract_message import AbstractMessageDTO
from app.dto.telegram_sending import TelegramSendingDTO
from app.infrastructure.env import DEV_RUN, DEV_USER_UUID_LIST
from app.infrastructure.repositories.user import UserRepository


class AskForFactsUseCase:
    """Send notification to Users, asking them to add today's Facts."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def __call__(self) -> list[TelegramSendingDTO]:
        """Entrypoint for this use case."""

        sendings = []

        # TODO: Add i18n
        locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")
        today = datetime.date.today().strftime("%d %B")

        # TODO: Add day name, e.g. was it monday, sunday, ..?
        # TODO: Add holidays, based on language
        # TODO: Take location into account to determine holdiays
        text = (
            f"📆 {today} #day"
            "\n\n"
            "📖 Пришли мне одно или несколько сообщений с самыми важными событиями за день, они буду записаны."
            "\n\n"
            "⚠️ Чтобы я правильно понял, какое событие к какой дате относится "
            '- обязательно отвечай через "Ответить".'
        )

        users = self.user_repository.get_active_users()

        if DEV_RUN:
            users = filter(lambda u: u.uuid in DEV_USER_UUID_LIST, users)

        for user in users:
            sending = TelegramSendingDTO(
                chat_id=user.telegram_id,
                messages=[AbstractMessageDTO(text=text)],
            )
            sendings.append(sending)

        return sendings

import datetime
import locale

from app.dto.abstract_message import AbstractMessage
from app.dto.telegram_shipment import TelegramShipment
from app.infrastructure.repositories.user import UserRepository


class AskForFactsUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def __call__(self) -> list[TelegramShipment]:
        shipments = []

        # TODO: Add i18n
        locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")
        today = datetime.date.today().strftime("%d %B")

        text = (
            f"📆 {today} #day"
            "\n\n"
            "📖 Пришли мне одно или несколько сообщений с самыми важными событиями за день, они буду записаны."
            "\n\n"
            "⚠️ Чтобы я правильно понял, какое событие к какой дате относится "
            '- обязательно отвечай через "Ответить".'
        )

        users = self.user_repository.get_active_users()

        for user in users:
            shipment = TelegramShipment(
                user_id=user.get("telegram_id", 0),
                messages=[AbstractMessage(text=text)],
            )
            shipments.append(shipment)

        return shipments

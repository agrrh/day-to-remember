import json
import time

from telebot.types import CallbackQuery as TgCallbackQuery

from app.domain.review_period import ReviewPeriodWeek
from app.dto.abstract_message import AbstractMessageDTO
from app.dto.telegram_callback import TelegramCallbackDTO
from app.dto.telegram_sending import TelegramSendingDTO
from app.infrastructure.repositories.fact import FactRepository
from app.infrastructure.repositories.review_session import ReviewSessionRepository
from app.infrastructure.repositories.user import UserRepository


class SetWeeklyFavUseCase:
    """User has sent a Message, store it as a Fact."""

    def __init__(
        self,
        fact_repository: FactRepository,
        user_repository: UserRepository,
        rs_repository: ReviewSessionRepository,
    ):
        self.fact_repository = fact_repository
        self.user_repository = user_repository
        self.rs_repository = rs_repository

    def __call__(self, callback: TgCallbackQuery) -> TelegramSendingDTO:
        """Entrypoint for this use case."""

        tg_callback = TelegramCallbackDTO(raw_callback=callback)

        _, fact_uuid = tg_callback.get_data_parts()

        fact = self.fact_repository.get_by_uuid(fact_uuid)
        user = self.user_repository.get_by_uuid(fact.user_uuid)
        period = ReviewPeriodWeek(date=fact.date)
        rss = self.rs_repository.get_by_user_and_period(user, period)

        # FIXME: date is not JSON serializable, we need DTO or custom serialization
        rss.date_start = time.mktime(period.start.timetuple())  # ty: ignore[possibly-missing-attribute]
        rss.date_end = time.mktime(period.end.timetuple())  # ty: ignore[possibly-missing-attribute]

        # FIXME: List[uuid] <-> json string
        rss.fact_uuids = json.dumps(rss.fact_uuids)  # ty: ignore[invalid-assignment]

        # TODO: Check that Fact is present in Facts list
        self.rs_repository.promote_fact(rss, fact)

        # FIXME: date is not JSON serializable, we need DTO or custom serialization
        fact.date = time.mktime(fact.date.timetuple())  # ty: ignore[invalid-assignment]
        self.fact_repository.set_selected_for_scope(fact, period.scope)

        message = AbstractMessageDTO(
            text=f"Выбран факт: {fact.text}",
        )

        # TODO: Also update buttons with some COMPLETED state?

        sending = TelegramSendingDTO(
            chat_id=callback.message.chat.id,
            messages=[
                message,
            ],
        )

        return sending

import datetime

from app.domain.review_period import ReviewPeriodWeek
from app.dto.abstract_message import AbstractMessageDTO
from app.dto.buttons import ButtonDTO, ButtonsDTO
from app.dto.telegram_sending import TelegramSendingDTO
from app.infrastructure.env import DEV_RUN, DEV_USER_UUID_LIST
from app.infrastructure.repositories.fact import FactRepository
from app.infrastructure.repositories.review_session import ReviewSessionRepository
from app.infrastructure.repositories.user import UserRepository


class SendWeeklyDigestUseCase:
    """Ask user to choose most important Fact out of given weekly list."""

    def __init__(
        self,
        user_repository: UserRepository,
        fact_repository: FactRepository,
        rs_repository: ReviewSessionRepository,
    ):
        self.user_repository = user_repository
        self.fact_repository = fact_repository
        self.rs_repository = rs_repository

    def __call__(self) -> list[TelegramSendingDTO]:
        """Entrypoint for this use case."""

        sendings = []

        today = datetime.date.today()

        period = ReviewPeriodWeek(date=today)

        users = self.user_repository.get_active_users()

        if DEV_RUN:
            users = filter(lambda u: u.uuid in DEV_USER_UUID_LIST, users)

        # TODO: Add i18n
        text = (
            "📆 Настало время выбрать самое важное событие за период!\n"
            f"{period.start} - {period.end}"
        )

        for user in users:
            # FIXME: Filter only non-finished ReviewSessions for desired Scope!
            rs = self.rs_repository.get_by_user_and_period(user=user, period=period)

            # TODO: Update RS status as "notified"

            facts = [self.fact_repository.get_by_uuid(uuid=u) for u in rs.fact_uuids]

            buttons_group = ButtonsDTO(buttons=[], tg_width=1, tg_prefix="weekly")
            for fact in facts:
                button = ButtonDTO(data="tmp", label="placeholder")
                button.load_from_fact(fact)

                buttons_group.buttons.append(button)

            message = AbstractMessageDTO(
                text=text,
                buttons=buttons_group,
            )

            sending = TelegramSendingDTO(
                chat_id=user.telegram_id,
                messages=[message],
            )
            sendings.append(sending)

        return sendings

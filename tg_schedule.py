import sys
import time

import schedule
import telebot

from app.infrastructure.env import (
    DEV_RUN,
    GRIST_DOC_ID,
    GRIST_TOKEN,
    GRIST_URL,
    TG_TOKEN,
)
from app.infrastructure.external.grist_adapter import GristAdapter
from app.infrastructure.external.telegram_adapter import TelegramAdapter
from app.infrastructure.repositories.fact import FactRepository
from app.infrastructure.repositories.review_session import ReviewSessionRepository
from app.infrastructure.repositories.user import UserRepository
from app.use_cases.ask_for_facts import AskForFactsUseCase
from app.use_cases.plan_review_sessions import PlanReviewSessionsUseCase
from app.use_cases.send_weekly_digest import SendWeeklyDigestUseCase

bot = telebot.TeleBot(TG_TOKEN)

grist_adapter = GristAdapter(
    url=GRIST_URL,
    document_id=GRIST_DOC_ID,
    api_key=GRIST_TOKEN,
)
user_repository = UserRepository(grist=grist_adapter)
fact_repository = FactRepository(grist=grist_adapter)
rs_repository = ReviewSessionRepository(grist=grist_adapter)

telegram_adapter = TelegramAdapter(handler=bot)


def job_ask_for_facts():
    """Ask User to write today's Fact."""

    ask_for_facts = AskForFactsUseCase(
        user_repository=user_repository,
    )
    sendings_list = ask_for_facts()
    for sending in sendings_list:
        telegram_adapter.process_sending(sending)


def job_plan_review_sessions():
    """Form ReviewSessions for Users to later recieve as digests."""
    plan_review_sessions = PlanReviewSessionsUseCase(
        user_repository=user_repository,
        fact_repository=fact_repository,
        rs_repository=rs_repository,
    )

    plan_review_sessions()


def job_send_weekly_digest():
    """Ask User to choose most important Fact out of a weekly list."""

    send_weekly = SendWeeklyDigestUseCase(
        user_repository=user_repository,
        fact_repository=fact_repository,
        rs_repository=rs_repository,
    )

    sendings_list = send_weekly()
    for sending in sendings_list:
        telegram_adapter.process_sending(sending)


if __name__ == "__main__":
    print("Initializing ...")

    if DEV_RUN:
        # job_ask_for_facts()
        # job_plan_review_sessions()
        job_send_weekly_digest()
        sys.exit()

    # TODO: Parametrize time for each user
    # TODO: Send further notices after user interacted with first one
    schedule.every().hour.do(job_plan_review_sessions)
    schedule.every().day.at("20:00").do(job_ask_for_facts)
    schedule.every().monday.at("20:05").do(job_send_weekly_digest)

    print("Starting ...")
    while True:
        schedule.run_pending()
        time.sleep(30)

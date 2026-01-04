import os
import time

import schedule
import telebot

from app.infrastructure.external.grist_adapter import GristAdapter
from app.infrastructure.external.telegram_adapter import TelegramAdapter
from app.infrastructure.repositories.user import UserRepository
from app.use_cases.ask_for_facts import AskForFactsUseCase

TG_TOKEN = os.environ.get("TG_TOKEN", "")

GRIST_URL = os.environ.get("GRIST_URL", "")
GRIST_DOC_ID = os.environ.get("GRIST_DOC_ID", "")
GRIST_TOKEN = os.environ.get("GRIST_TOKEN", "")

bot = telebot.TeleBot(TG_TOKEN)

grist_adapter = GristAdapter(
    url=GRIST_URL,
    document_id=GRIST_DOC_ID,
    api_key=GRIST_TOKEN,
)
user_repository = UserRepository(grist=grist_adapter)

telegram_adapter = TelegramAdapter(handler=bot)


def job_ask_for_facts():
    ask_for_facts = AskForFactsUseCase(
        user_repository=user_repository,
    )
    sendings_list = ask_for_facts()
    for sending in sendings_list:
        telegram_adapter.process_sending(sending)


if __name__ == "__main__":
    print("Initializing ...")

    # TODO: Parametrize time for each user
    schedule.every().day.at("20:00").do(job_ask_for_facts)

    print("Starting ...")
    while True:
        schedule.run_pending()
        time.sleep(5)

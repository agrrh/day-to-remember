import os

import telebot

from app.infrastructure.external.grist_adapter import GristAdapter
from app.infrastructure.external.telegram_adapter import TelegramAdapter
from app.infrastructure.repositories.fact import FactRepository
from app.infrastructure.repositories.user import UserRepository
from app.use_cases.create_fact import CreateFactUseCase
from app.use_cases.start_bot import StartBotUseCase

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
# NOTE: Copies are used cause
user_repository = UserRepository(grist=grist_adapter)
fact_repository = FactRepository(grist=grist_adapter)

telegram_adapter = TelegramAdapter(handler=bot)


@bot.message_handler(commands=["start"])
def handle_start(message):
    handler = StartBotUseCase(
        user_repository=user_repository,
    )
    sending = handler(message)
    telegram_adapter.process_sending(sending)


@bot.message_handler(
    func=lambda message: message.reply_to_message.from_user.is_bot
    and "#day" in message.reply_to_message.text
)
# @bot.message_handler(func=lambda message: True)
def handle_fact(message):
    handler = CreateFactUseCase(
        user_repository=user_repository,
        fact_repository=fact_repository,
    )
    sending = handler(message)
    telegram_adapter.process_sending(sending)


if __name__ == "__main__":
    print("Starting ...")
    bot.infinity_polling()

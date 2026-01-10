import telebot
from telebot.types import CallbackQuery as TgCallbackQuery
from telebot.types import Message as TgMessage

from app.infrastructure.env import (
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

# Use cases
from app.use_cases.create_fact import CreateFactUseCase
from app.use_cases.set_weekly_fav import SetWeeklyFavUseCase
from app.use_cases.start_bot import StartBotUseCase

bot = telebot.TeleBot(TG_TOKEN)

grist_adapter = GristAdapter(
    url=GRIST_URL,
    document_id=GRIST_DOC_ID,
    api_key=GRIST_TOKEN,
)
fact_repository = FactRepository(grist=grist_adapter)
user_repository = UserRepository(grist=grist_adapter)
rs_repository = ReviewSessionRepository(grist=grist_adapter)

telegram_adapter = TelegramAdapter(handler=bot)


@bot.message_handler(commands=["start"])
def handle_start(message):
    """Process "/start" command."""
    handler = StartBotUseCase(
        user_repository=user_repository,
    )
    sending = handler(message)
    telegram_adapter.process_sending(sending=sending)


# TODO: Any better way to determine daily messages?
@bot.message_handler(
    func=lambda message: message.reply_to_message.from_user.is_bot
    and "#day" in message.reply_to_message.text
)
# @bot.message_handler(func=lambda message: True)
def handle_fact(message: TgMessage):
    """Process replies to daily scheduled messages."""
    handler = CreateFactUseCase(
        user_repository=user_repository,
        fact_repository=fact_repository,
    )
    sending = handler(message)
    telegram_adapter.process_sending(sending=sending, message_to_reply=message)


@bot.callback_query_handler(func=lambda call: call.data.startswith("weekly_"))
def handle_weekly_choice(callback: TgCallbackQuery):
    """Process choice of most important event (weekly)."""

    handler = SetWeeklyFavUseCase(
        fact_repository=fact_repository,
        user_repository=user_repository,
        rs_repository=rs_repository,
    )
    sending = handler(callback)
    telegram_adapter.process_sending(sending=sending)


if __name__ == "__main__":
    print("Starting ...")
    bot.infinity_polling()

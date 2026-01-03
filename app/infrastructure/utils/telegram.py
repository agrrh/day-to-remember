# TODO: Move out of utils!
#   Some specific class maybe? Domain service?

import time

from telebot import TeleBot
from telebot.types import Message

from app.dto.abstract_message import AbstractMessage
from app.infrastructure.utils.humans import text_to_seconds


def process_replies(bot: TeleBot, message: Message, replies: list[AbstractMessage]):
    """Given a Telebot instance, incoming message and number of replies, process those replies."""

    for i, reply in enumerate(replies):
        reply_message = reply.to_telegram_args()

        if reply_message.get("text"):
            bot.reply_to(message, **reply_message)
        elif reply_message.get("photo"):
            bot.send_photo(
                chat_id=message.chat.id,
                reply_to_message_id=message.id,
                **reply_message,
            )
        else:
            # TODO: Send error to logs, not to customer
            bot.reply_to(message, text="Error, please contact service owner!")

        if i < len(replies):
            time.sleep(text_to_seconds(reply.text, bool(reply.media_url)))


def send_messages(bot: TeleBot, user_id: int, messages: list[AbstractMessage]):
    """Given a Telebot instance, user ID and number of messages, send those messages."""

    for i, message in enumerate(messages):
        tg_message = message.to_telegram_args()

        if tg_message.get("text"):
            bot.send_message(chat_id=user_id, **tg_message)
        elif tg_message.get("photo"):
            bot.send_photo(
                chat_id=user_id,
                **tg_message,
            )
        else:
            # TODO: Send error to logs, not to customer
            bot.send_message(
                chat_id=user_id, text="Error, please contact service owner!"
            )

        if i < len(messages):
            time.sleep(text_to_seconds(message.text, bool(message.media_url)))

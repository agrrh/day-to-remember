import time

from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, ReactionTypeEmoji
from telebot.types import Message as TgMessage

from app.dto.abstract_message import AbstractMessageDTO
from app.dto.telegram_sending import TelegramSendingDTO


class TelegramAdapter:
    """Interact with Telegram API - send messages."""

    def __init__(self, handler: TeleBot):
        self.handler = handler

    def process_sending(
        self,
        sending: TelegramSendingDTO,
        message_to_reply: TgMessage | None = None,
    ) -> bool:
        """Given a Telebot instance, user ID and number of messages, send those messages, possibly as replies."""

        for i, message in enumerate(sending.messages):
            # TODO: Check if sent successful
            self.__send_message(
                chat_id=sending.chat_id,
                message=message,
                message_to_reply=message_to_reply,
            )

            if i < len(sending.messages):
                time.sleep(message.measure_read_time())

        return True

    def __send_message(
        self,
        chat_id: int,
        message: AbstractMessageDTO,
        message_to_reply: TgMessage | None = None,
    ) -> None:
        """Send abstract message, further sends text, media or reactions."""
        if message.media_url:
            self.__send_photo(
                chat_id=chat_id,
                message=message,
                message_to_reply=message_to_reply,
            )
        elif message.text:
            if message.buttons is not None:
                buttons_markup = message.buttons.to_telegram_markup()

                self.__send_text(
                    chat_id=chat_id,
                    message=message,
                    message_to_reply=message_to_reply,
                    reply_markup=buttons_markup,
                )
            else:
                self.__send_text(
                    chat_id=chat_id,
                    message=message,
                    message_to_reply=message_to_reply,
                )
        elif message.reaction_emoji is not None:
            if message_to_reply is not None:
                self.__send_reaction(
                    chat_id=chat_id,
                    message_to_react=message_to_reply,
                    reaction=message.reaction_emoji,
                )
            else:
                self.handler.send_message(
                    chat_id=chat_id,
                    text="Can't react to non-existent message!",
                )
        else:
            # TODO: Send error to logs, not to customer
            self.handler.send_message(
                chat_id=chat_id, text="Error, please contact service owner!"
            )

        # TODO: Return success/failure
        return None

    def __send_text(
        self,
        chat_id: int,
        message: AbstractMessageDTO,
        message_to_reply: TgMessage | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> bool:
        tg_args = message.to_telegram_args()

        if reply_markup is not None:
            tg_args["reply_markup"] = reply_markup

        if message_to_reply is not None:
            message_sent = self.handler.reply_to(message=message_to_reply, **tg_args)
        else:
            message_sent = self.handler.send_message(chat_id=chat_id, **tg_args)

        return bool(message_sent)

    def __send_photo(
        self,
        chat_id: int,
        message: AbstractMessageDTO,
        message_to_reply: TgMessage | None = None,
    ) -> bool:
        tg_args = message.to_telegram_args()

        if message_to_reply is not None:
            message_sent = self.handler.send_photo(
                chat_id=chat_id, reply_to_message_id=message_to_reply.id, **tg_args
            )
        else:
            message_sent = self.handler.send_photo(chat_id=chat_id, **tg_args)

        return bool(message_sent)

    def __send_reaction(
        self, chat_id: int, message_to_react: TgMessage, reaction: str
    ) -> bool:
        reactions = [ReactionTypeEmoji(type="emoji", emoji=reaction)]

        success = self.handler.set_message_reaction(
            chat_id=chat_id,
            message_id=message_to_react.id,
            reaction=reactions,
            is_big=False,
        )
        return success

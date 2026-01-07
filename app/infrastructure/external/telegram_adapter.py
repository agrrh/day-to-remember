import time

from telebot import TeleBot
from telebot.types import Message as TgMessage
from telebot.types import ReactionTypeEmoji

from app.dto.abstract_message import AbstractMessageDTO
from app.dto.telegram_sending import TelegramSendingDTO


class TelegramAdapter:
    def __init__(self, handler: TeleBot):
        self.handler = handler

    def process_sending(
        self,
        sending: TelegramSendingDTO,
        message_to_reply: TgMessage | None = None,
    ) -> bool:
        """Given a Telebot instance, user ID and number of messages, send those messages, possibly as replies."""

        # TODO: Check if sent successful
        for i, message in enumerate(sending.messages):
            if message.media_url:
                self.__send_photo(
                    chat_id=sending.chat_id,
                    message=message,
                    message_to_reply=message_to_reply,
                )
            elif message.text:
                self.__send_text(
                    chat_id=sending.chat_id,
                    message=message,
                    message_to_reply=message_to_reply,
                )
            elif message.reaction_emoji is not None:
                if message_to_reply is not None:
                    self.__send_reaction(
                        chat_id=sending.chat_id,
                        message_to_react=message_to_reply,
                        reaction=message.reaction_emoji,
                    )
                else:
                    self.handler.send_message(
                        chat_id=sending.chat_id,
                        text="Can't react to non-existent message!",
                    )
            else:
                # TODO: Send error to logs, not to customer
                self.handler.send_message(
                    chat_id=sending.chat_id, text="Error, please contact service owner!"
                )

            if i < len(sending.messages):
                time.sleep(message.measure_read_time())

        return True

    def __send_text(
        self,
        chat_id: int,
        message: AbstractMessageDTO,
        message_to_reply: TgMessage | None = None,
    ) -> bool:
        tg_message = message.to_telegram_args()

        if message_to_reply is not None:
            message_sent = self.handler.reply_to(message=message_to_reply, **tg_message)
        else:
            message_sent = self.handler.send_message(chat_id=chat_id, **tg_message)

        return bool(message_sent)

    def __send_photo(
        self,
        chat_id: int,
        message: AbstractMessageDTO,
        message_to_reply: TgMessage | None = None,
    ) -> bool:
        tg_message = message.to_telegram_args()

        if message_to_reply is not None:
            message_sent = self.handler.send_photo(
                chat_id=chat_id, reply_to_message_id=message_to_reply.id, **tg_message
            )
        else:
            message_sent = self.handler.send_photo(chat_id=chat_id, **tg_message)

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

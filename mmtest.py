import logging

from telethon.errors.rpcerrorlist import BotMethodInvalidError, FloodWaitError, MessageNotModifiedError
from telethon.tl.types import Message

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class MusicMod(loader.Module):
    strings = {
        "name": "Music",
        "no_query": "<emoji document_id=5337117114392127164>🤷‍♂</emoji> <b>Provide a search query.</b>",
        "not_found": "<emoji document_id=5843952899184398024>🚫</emoji> <b>Track not found</b>",
        "usage": "<b>Usage:</b> <code>.music [track name]</code>",
        "error": "<emoji document_id=5843952899184398024>🚫</emoji> <b>Error: {}</b>",
        "flood_wait": "<emoji document_id=5462295343642956603>⏳</emoji> <b>Wait {}s (Telegram limits).</b>",
        "bot_error": "<emoji document_id=5228947933545635555>🤖</emoji> <b>Bot error: {}</b>",
    }

    def __init__(self):
        self.bot = "@eliteSCbot"

    @loader.command()
    async def m(self, message: Message):
        args = utils.get_args(message)
        query = ""

        if args:
            query = " ".join(args)
        elif reply := await message.get_reply_message():
            query = reply.raw_text.strip()

        if not query:
            await utils.answer(message, self.strings("usage"))
            return

        try:
            results = await message.client.inline_query(self.bot, query)

            if not results:
                await utils.answer(message, self.strings("not_found"))
                return

            await results[0].click(
                entity=message.chat_id,
                hide_via=True,
                reply_to=message.reply_to_msg_id or None
            )
            await message.delete()

        except FloodWaitError as e:
            await utils.answer(message, self.strings("flood_wait").format(e.seconds))
        except BotMethodInvalidError as e:
            await utils.answer(message, self.strings("bot_error").format(str(e)))
        except MessageNotModifiedError:
            pass
        except Exception as e:
            logger.exception("Search error:")
            await utils.answer(message, self.strings("error").format(str(e)))

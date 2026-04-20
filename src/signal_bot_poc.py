#secrets im file, file im .gitignore
#läuft in nem docker auf fpg
#poe

import logging
import os
from dotenv import load_dotenv
from faster_whisper import WhisperModel

from signalbot import (
    Command,
    Config,
    Context,
    SignalBot,
    enable_console_logging,
    triggered,
)


class PingCommand(Command):
    @triggered("Ping")
    async def handle(self, context: Context) -> None:
        await context.react("👍")

class PigCommand(Command):
    async def handle(self, context: Context) -> None:
        logging.info("Pig Command am Stizzle")
        model = WhisperModel("large-v3-turbo", device="cpu")
        logging.info(f"debug ausgabe {context.message.text} und {context.message.attachments_local_filenames}")
        if context.message.text is None and context.message.attachments_local_filenames is not None:
            for item in context.message.attachments_local_filenames:
                segments, info = model.transcribe(item, language="de")
                for segment in segments:
                    await context.send(segment.text)


#https://deepwiki.com/signalbot-org/signalbot/3.2-commands

if __name__ == "__main__":
    enable_console_logging(logging.INFO)

    load_dotenv()

    bot = SignalBot(
        Config(
            signal_service=os.environ["SIGNAL_SERVICE"],
            phone_number=os.environ["PHONE_NUMBER"],
        )
    )
    bot.register(PingCommand())  # Run the command for all contacts and groups
    bot.register(PigCommand())
    bot.start()
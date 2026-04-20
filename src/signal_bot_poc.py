#secrets im file, file im .gitignore
#läuft in nem docker auf fpg
#poe

import logging
import os
from dotenv import load_dotenv

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
        await context.send("Pong")


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
    bot.start()
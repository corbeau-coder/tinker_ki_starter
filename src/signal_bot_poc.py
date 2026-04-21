#secrets im file, file im .gitignore
#läuft in nem docker auf fpg
#poe

import logging
import os
from dotenv import load_dotenv
from faster_whisper import WhisperModel
from ollama import AsyncClient

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
    def __init__(self):
        self.model = WhisperModel("large-v3-turbo", device="cpu")
        self.asyclient = AsyncClient()

    async def handle(self, context: Context) -> None:

        # You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
        if context.message.text is None and context.message.attachments_local_filenames is not None:
            for item in context.message.attachments_local_filenames:
                path = os.environ["ATTACHMENT_PATH"]
                path = path if path.endswith("/") else path + "/"
                segments, info = self.model.transcribe(path + item, language="de")
                transcript = ""
                for segment in segments:
                    transcript = transcript + segment.text
                    await context.send(segment.text)

                message = [{"role": "user", "content": transcript}]
                await self.bot.start_typing(context.message.recipient())
                try:
                    response = await self.asyclient.chat(model="assi1", messages=message, stream=False)
                    response_str = response.message.content
                    while response_str.length > 255:
                        await context.send(response_str[:255])
                        response_str = response_str[:255]
                finally:
                    await self.bot.stop_typing(context.message.recipient())



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
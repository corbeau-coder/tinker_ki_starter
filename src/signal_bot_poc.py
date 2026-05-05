#secrets im file, file im .gitignore
#läuft in nem docker auf fpg
#poe

from loguru import logger
import logging
import os
import datetime as dt

from dotenv import load_dotenv
from faster_whisper import WhisperModel
from ollama import AsyncClient
from ddgs import DDGS
from pathlib import Path

from opentelemetry.trace import get_tracer, Status, StatusCode
from modules.otel_init import init_telemetry

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
        self.asynclient = AsyncClient()
        self.tracer = get_tracer("tinker_one")

    async def handle(self, context: Context) -> None:
        tools = {
            "web_search": self.web_search
        }

        # You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
        if context.message.text is None and context.message.attachments_local_filenames is not None:
            with self.tracer.start_as_current_span("INCOMING_MESSAGE") as span:
                for item in context.message.attachments_local_filenames:
                    logger.debug(f"taking {item} from stack start working on")
                    await self.bot.start_typing(context.message.recipient())
                    path = os.environ["ATTACHMENT_PATH"]
                    path = path if path.endswith("/") else path + "/"
                    logger.debug(f"opening {path}")
                    with self.tracer.start_as_current_span("CREATE_TRANSCRIPT") as span:
                        span.set_attribute("audio.file_path", path)
                        try:
                            segments, info = self.model.transcribe(path + item, language="de")
                        except IOError as e:
                            logger.error(f"error openening {path}, got exception {e}")
                            span.set_status(Status(StatusCode.ERROR, str(e)))
                            span.record_exception(e)
                            raise
                        logger.debug(f"info {info}")
                        transcript = ""
                        for segment in segments:
                            transcript = transcript + segment.text
                        logger.info(f"transcripted command is {transcript}")
                        await context.send(transcript)

                    with self.tracer.start_as_current_span("LLM_OPERATIONS") as span:

                        message = [{"role": "system", "content": f"Das heutige Datum ist {dt.date.today().strftime('%d.%m.%Y')}"},{"role": "user", "content": transcript}]
                        try:
                            logger.debug(f"starting llm with following prompt message: {message}")
                            response = await self.asynclient.chat(model="assi1", messages=message, stream=False, tools=list(tools.values()))
                            logger.debug(f"LLM response: {response.message.content}")
                            while response.message.tool_calls is not None:
                                logger.debug(f"tools called: {response.message.tool_calls[0].function.name} {response.message.tool_calls[0].function.arguments}")
                                call = response.message.tool_calls[0]
                                tool_fn = tools[call.function.name]
                                result = tool_fn(**call.function.arguments)
                                logger.debug(f"tool call result: {result}")
                                message.append(response.message)
                                message.append({"role": "tool", "content": str(result)})
                                logger.debug(f"starting llm with following prompt message including tool response: {message}")
                                response = await self.asynclient.chat(model="assi1", messages=message, stream=False,
                                                                      tools=[self.web_search])
                                logger.debug(f"LLM response: {response.message.content} amount of tool call requests: {len(response.message.tool_calls) if response.message.tool_calls else 0}")

                            response_str = response.message.content
                            await context.send(response_str)
                        except Exception as e:
                            span.set_status(Status(StatusCode.ERROR, str(e)))
                            span.record_exception(e)
                            raise
                        finally:
                            await self.bot.stop_typing(context.message.recipient())

    @staticmethod
    def web_search(query: str) -> str:
        """Sucht nach aktuellen Informationen im Web mit DuckDuckGo
        Nutze dieses Tool, wenn du unsicher bist oder der Nutzer
        nach Informationen fragst, die du nicht sicher kennst.
        Sei dir den klassischen Problemen mit Suchmaschinen-APIs bewusst, insbesondere
        wie sie klassisch filtern - du bekommst nur 5 Ergebnisse zurück und solltest mithilfe der
        Suchanfrage eingrenzen, was du sehen willst.
        Args:
            query: Die Suchanfrage als String

        Returns:
            List of ditionaries with search results
        """
        result = DDGS().text(query, region="de-de", max_results=5)

        return "\n\n".join(
            f"Titel: {r['title']}\nURL: {r['href']}\nInhalt: {r['body']} "
            for r in result
        )

#https://deepwiki.com/signalbot-org/signalbot/3.2-commands

if __name__ == "__main__":
    enable_console_logging(logging.INFO)


    load_dotenv(Path(__file__).parent.parent / ".env")
    init_telemetry("tinker_one")

    bot = SignalBot(
        Config(
            signal_service=os.environ["SIGNAL_SERVICE"],
            phone_number=os.environ["PHONE_NUMBER"],
        )
    )
    bot.register(PingCommand())  # Run the command for all contacts and groups
    bot.register(PigCommand())
    bot.start()
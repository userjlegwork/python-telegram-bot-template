"""Entry point for the application."""
import logging
import os

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

import commands
from db.connection import DBHandler

load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Do this on every module that you want to use
logger = logging.getLogger(__name__)

# Logs telegram api errors
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""

    app = ApplicationBuilder().token(os.getenv("TOKEN")).build()

    DBHandler().connect_pool()

    app.add_error_handler(error)

    app.add_handlers(
        [
            CommandHandler(command, eval(f"commands.{command}"))
            for command in commands.get_all_commands()
        ]
    )

    app.add_handler(MessageHandler(filters.COMMAND, commands.unknown))
    app.run_polling()


if __name__ == "__main__":
    main()

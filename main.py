"""Entry point for the application."""
import html
import json
import logging
import os
import traceback

from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

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
async def error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log Errors caused by Updates."""

    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb_string = "".join(tb_list)

    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    await context.bot.send_message(
        chat_id=os.getenv("DEVELOPER_CHAT_ID"), text=message, parse_mode=ParseMode.HTML
    )


def main():
    """Start the bot."""

    app = ApplicationBuilder().token(os.getenv("TOKEN")).build()

    DBHandler().connect_pool()

    app.add_handlers(
        [
            CommandHandler(command, getattr(commands, command))
            for command in commands.get_all_commands()
        ]
    )

    app.add_handler(MessageHandler(filters.COMMAND, commands.unknown))
    app.add_error_handler(error)
    app.run_polling()


if __name__ == "__main__":
    main()

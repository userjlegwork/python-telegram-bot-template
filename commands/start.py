"""All activity related to the /start command."""
import logging

from telegram import Update
from telegram.ext import ContextTypes

from common.utils import get_user_first_name

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""

    if update == None:
        return

    logger.info("/start command called")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Welcome {get_user_first_name(update)}!",  # 1 Handle translate
    )
    logger.info("/start command executed successfully")

if __name__ == "__main__":
    start()

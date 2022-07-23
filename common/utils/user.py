"""User related commands."""


def get_user_id(update):
    """Get the user id from the update."""
    return update.message.from_user.id


def get_user_name(update):
    """Get the user name from the update."""
    return update.message.from_user.username


def get_user_first_name(update):
    """Get the user first name from the update."""
    return update.message.from_user.first_name


def get_user_last_name(update):
    """Get the user last name from the update."""
    return update.message.from_user.last_name


def get_user_full_name(update):
    """Get the user full name from the update."""
    return update.message.from_user.full_name


def get_language_code(update):
    """Get the language code from the update."""
    return update.message.from_user.language_code


def get_user(update):
    """Get the user from the update."""
    return update.message.from_user


def ban_user(update):
    """Ban the user from the update."""
    update.message.bot.kick_chat_member(
        update.message.chat_id, update.message.from_user.id
    )

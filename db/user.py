"""Database user handlers"""
import logging

from db.connection import DBHandler

logger = logging.getLogger(__name__)


def create_users_table():
    """Create the users table."""

    # Create the users table
    DBHandler().execute(
        """CREATE TABLE IF NOT EXISTS users (id BIGINT PRIMARY KEY, first_name VARCHAR(255),
        last_name VARCHAR(255), username VARCHAR(255), language_code VARCHAR(255))"""
    )
    logger.info("Users table created")


def save_user(user):
    """Save the user to the database."""

    # Check if the user is already in the database
    if (
        DBHandler().execute("SELECT * FROM users WHERE id = %s", (user.id,)).fetchone()
        is not None
    ):
        logger.info("User already in database")
        return

        # Save the user to the database
    DBHandler().execute(
        """INSERT INTO users (id, first_name, last_name, username, language_code)
        VALUES (%s, %s, %s, %s, %s)""",
        (
            user.id,
            user.first_name,
            user.last_name,
            user.username,
            user.language_code,
        ),
    )


def delete_user(user):
    """Delete the user from the database."""

    # Delete the user from the database
    DBHandler().execute("DELETE FROM users WHERE id = %s", (user.id,))

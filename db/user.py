"""Database user handlers"""
from db.connection import DBHandler


def save_user(user):
    """Save the user to the database."""

    # Check if the user is already in the database
    if (
        DBHandler().execute("SELECT * FROM users WHERE id = %s", (user.id,)).fetchone()
        is not None
    ):
        return

        # Save the user to the database
    DBHandler().execute(
        "INSERT INTO users (id, first_name, last_name, username, language_code) VALUES (%s, %s, %s, %s, %s)",
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

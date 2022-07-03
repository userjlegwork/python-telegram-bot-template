"""Handle postgresql connection."""
import logging
import os
from typing import List, Tuple

import psycopg2
from psycopg2.pool import ThreadedConnectionPool

logger = logging.getLogger(__name__)


class DBHandler:
    """Handle postgresql connection."""

    conn = None

    @classmethod
    def connect_pool(cls) -> None:
        """Connect to the database."""

        logger.info("Connecting to the PostgreSQL database... (pool)")
        try:
            cls.conn = ThreadedConnectionPool(
                5,
                50,
                host=os.getenv("POSTGRES_HOST", "localhost"),
                database=os.getenv("POSTGRES_DB", "testbot"),
                user=os.getenv("POSTGRES_USER", "postgres"),
                password=os.getenv("POSTGRES_PASSWORD", "postgres"),
            ).getconn()

            logger.info("PostgreSQL database connected (pool)")
            with cls.conn.cursor() as cur:
                cur.execute("SELECT version();")
                logger.info(
                    "Connected to PostgreSQL database version: %s", cur.fetchone()
                )
        except (psycopg2.DatabaseError) as error:
            logger.error(error)

        finally:
            if not cur.closed:
                cur.close()

    @classmethod
    def connect(cls) -> None:
        """Connect to the database."""

        logger.info("Connecting to the PostgreSQL database...")
        try:
            cls.conn = psycopg2.connect(
                host=os.getenv("POSTGRES_HOST", "localhost"),
                database=os.getenv("POSTGRES_DB", "testbot"),
                user=os.getenv("POSTGRES_USER", "postgres"),
                password=os.getenv("POSTGRES_PASSWORD", "postgres"),
            )

            logger.info("PostgreSQL database connected")
            with cls.conn.cursor() as cur:
                cur.execute("SELECT version();")
                logger.info(
                    "Connected to PostgreSQL database version: %s", cur.fetchone()
                )
        except (psycopg2.DatabaseError) as error:
            logger.error(error)

        finally:
            if not cur.closed:
                cur.close()

    @classmethod
    def execute(cls, query: str, params: Tuple = None) -> List:
        """Execute a query."""
        result = []
        if cls.conn is None:
            cls.connect()

        with cls.conn.cursor() as cur:
            try:
                cur.execute(query, params)
                cls.conn.commit()
                if cur.rowcount > 0:
                    result = cur.fetchall()
            except (psycopg2.DatabaseError) as error:
                logger.error(error)
            finally:
                if not cur.closed:
                    cur.close()
                cls.close_connection()
        return result

    @classmethod
    def close_connection(cls) -> None:
        """Close the connection."""

        if cls.conn is not None:
            cls.conn.close()
            logger.info("PostgreSQL connection closed")

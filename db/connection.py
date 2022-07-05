"""Handle postgresql connection."""
import logging
import os
from typing import List, Tuple

import psycopg2
from psycopg2.pool import ThreadedConnectionPool

logger = logging.getLogger(__name__)


class DBHandler:
    """Handle postgresql connection."""

    pool = None

    @classmethod
    def connect_pool(cls) -> None:
        """Connect to the database."""

        logger.info("Connecting to the PostgreSQL database... (pool)")
        try:
            cls.pool = ThreadedConnectionPool(
                5,
                50,
                host=os.getenv("POSTGRES_HOST", "localhost"),
                database=os.getenv("POSTGRES_DB", "testbot"),
                user=os.getenv("POSTGRES_USER", "postgres"),
                password=os.getenv("POSTGRES_PASSWORD", "postgres"),
            )

            conn = cls.pool.getconn()

            logger.info("PostgreSQL database connected (pool)")
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                logger.info(
                    "Connected to PostgreSQL database version: %s", cur.fetchone()
                )
        except (psycopg2.DatabaseError) as error:
            logger.error(error)

        finally:
            if not cur.closed:
                cur.close()

            if conn:
                cls.pool.putconn(conn)

    @classmethod
    def execute(cls, query: str, params: Tuple = None) -> List:
        """Execute a query."""
        result = []
        if cls.pool is None:
            cls.connect_pool()

        with cls.pool.getconn() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                result = cur.fetchall()

            cls.pool.putconn(conn)
        return result

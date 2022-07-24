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

        logger.info("Creating connection pool...")
        try:
            cls.pool = ThreadedConnectionPool(
                5,
                50,
                host=os.getenv("POSTGRES_HOST"),
                database=os.getenv("POSTGRES_DB"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
            )
            if cls.pool:
                logger.info("Connection pool created successfully")

            conn = cls.pool.getconn()
            if conn:
                logger.info("Successfully recived connection from connection pool")

            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                logger.info(
                    "Connected to PostgreSQL database version: %s", cur.fetchone()
                )
        except (psycopg2.DatabaseError) as error:
            logger.error(error)

        else:
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
            if conn:
                logger.info("Successfully recived connection from connection pool")
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    result = cur.fetchall()
                    logger.info("Query executed successfully")
                cls.pool.putconn(conn)
        return result

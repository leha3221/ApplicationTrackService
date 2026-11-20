"""SQLite connection and named SQL-query helpers."""

from functools import lru_cache
from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "application_track.sqlite"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"
QUERIES_PATH = BASE_DIR / "sql" / "queries.sql"


def _casefold(value: str | None) -> str:
    return value.casefold() if value is not None else ""


def get_connection(db_path: Path | str = DB_PATH) -> sqlite3.Connection:
    """Open the project database with row access and foreign keys enabled."""
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.create_function("casefold", 1, _casefold, deterministic=True)
    return connection


def initialize_database(db_path: Path | str = DB_PATH) -> None:
    """Create the database tables and indexes if they do not exist yet."""
    connection = get_connection(db_path)
    try:
        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        connection.executescript(schema)
        connection.commit()
    finally:
        connection.close()


@lru_cache(maxsize=1)
def _named_queries() -> dict[str, str]:
    """Load SQL statements marked with ``-- name: query_name``."""
    contents = QUERIES_PATH.read_text(encoding="utf-8")
    queries: dict[str, str] = {}
    for section in contents.split("-- name:")[1:]:
        name, statement = section.split("\n", maxsplit=1)
        queries[name.strip()] = statement.strip().rstrip(";")
    return queries


def query_all(
    name: str,
    parameters: tuple = (),
    db_path: Path | str = DB_PATH,
) -> list[sqlite3.Row]:
    """Run a named query with bound parameters and return all rows."""
    connection = get_connection(db_path)
    try:
        cursor = connection.execute(_named_queries()[name], parameters)
        return cursor.fetchall()
    finally:
        connection.close()


def query_one(
    name: str,
    parameters: tuple = (),
    db_path: Path | str = DB_PATH,
) -> sqlite3.Row | None:
    """Run a named query with bound parameters and return its first row."""
    connection = get_connection(db_path)
    try:
        cursor = connection.execute(_named_queries()[name], parameters)
        return cursor.fetchone()
    finally:
        connection.close()

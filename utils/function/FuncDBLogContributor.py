# Library
import sqlite3
import logging

# ? Utils
from utils.constant import (
    DB_FILEPATH,
    DB_NAME_CONTRIBUTOR,
    DB_NAME_REPO,
)
from utils.function.FuncDB import db_retry_lock
from utils.model.Sgithub import (
    TGitHubContributorJoinLog,
    TGitHubContributorLog,
    TGitHubContributorBatchLog,
)


def init_table() -> bool:
    """Initialize the log database"""

    try:
        with sqlite3.connect(DB_FILEPATH) as connection:
            cursor = connection.cursor()
            # Create tables if not exists

            cursor.execute(
                f"""
            CREATE TABLE IF NOT EXISTS {DB_NAME_CONTRIBUTOR} (
                id INTEGER PRIMARY KEY,
                url TEXT NOT NULL UNIQUE,
                repo_url TEXT NOT NULL,
                repo_name TEXT,
                error TEXT,
                status TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
            )

            # Add indexes for performance
            cursor.execute(
                f"CREATE INDEX IF NOT EXISTS idx_contributor_url ON {DB_NAME_CONTRIBUTOR}(url)"
            )

            connection.commit()
            print(f'🗃️ DB "{DB_NAME_CONTRIBUTOR}" INIT SUCCESSFULLY')
            return True

    except sqlite3.Error as err:
        logging.error(f'❌ ERROR_DB in "init_table()": {err}')
        return False


def drop_table() -> bool:
    try:
        with sqlite3.connect(DB_FILEPATH) as connection:
            cursor = connection.cursor()

            # Drop existing tables
            cursor.execute(f"DROP TABLE IF EXISTS {DB_NAME_CONTRIBUTOR}")

            return True

    except sqlite3.Error as err:
        logging.error(f'❌ ERROR_DB in "drop_table()": {err}')
        return False


@db_retry_lock
def insert_batch(arr: list[TGitHubContributorLog], status: str) -> int:
    try:
        with sqlite3.connect(DB_FILEPATH) as connection:
            cursor = connection.cursor()
            data = [(item.url, item.repo_url, item.repo_name, status) for item in arr]
            cursor.executemany(
                f"""
                INSERT INTO {DB_NAME_CONTRIBUTOR} (url, repo_url, repo_name, status) 
                VALUES (?, ?, ?, ?)
                ON CONFLICT(url) DO NOTHING
                """,
                data,
            )
            connection.commit()
            return cursor.rowcount

    except sqlite3.Error as err:
        logging.error(f'❌ ERROR_DB in "insert_batch()": {err}')
        return 0


@db_retry_lock
def upsert(props: TGitHubContributorLog) -> bool:

    url = props.url
    # Ensure non-Null values for database columns
    repo_url = props.repo_url or ""  # Ensure non-Null
    repo_name = props.repo_name or ""  # Ensure non-Null
    error = props.error
    status = props.status

    try:
        with sqlite3.connect(DB_FILEPATH) as connection:
            cursor = connection.cursor()

            """
            Upsert operation : INSERT and UPDATE operations in the SQL query.
            
            COALESCE will use the first non SQL `NULL` value
            If a value already exists in the DB, it won't be overwritten with 
            SQL `NULL` value
            """
            cursor.execute(
                f"""
            INSERT INTO {DB_NAME_CONTRIBUTOR} (url, repo_url, repo_name, error, status) 
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(url) DO UPDATE SET 
                repo_url = CASE 
                    WHEN repo_url = '' THEN {DB_NAME_CONTRIBUTOR}.repo_url
                    ELSE repo_url
                END,
                repo_name = CASE 
                    WHEN repo_name = '' THEN {DB_NAME_CONTRIBUTOR}.repo_name
                    ELSE repo_name
                END,
                error = ?,
                status = ?,  
                timestamp = CURRENT_TIMESTAMP
            """,
                (url, repo_url, repo_name, error, status, error, status),
            )
            connection.commit()

            # Return True only if a row was actually inserted
            return cursor.rowcount > 0

    except sqlite3.Error as err:
        logging.error(f'❌ ERROR_DB in "upsert()": {err}')
        return False


@db_retry_lock
def load(
    status: list[str],
    repo_url: str | None = None,
) -> list[TGitHubContributorJoinLog]:

    data: list[TGitHubContributorJoinLog] = []

    try:
        with sqlite3.connect(DB_FILEPATH) as connection:
            cursor = connection.cursor()

            # Create placeholders for each status in the list
            # Generates ?, ? Dynamically
            placeholders = ", ".join("?" for _ in status)

            if repo_url:
                params = (repo_url,) + tuple(status)
                cursor.execute(
                    f"""
                SELECT
                    a.id, a.url, a.repo_url, a.repo_name, a.error, a.status, a.timestamp, b.output AS repo_output 
                FROM {DB_NAME_CONTRIBUTOR} a
                LEFT JOIN {DB_NAME_REPO} b 
                    ON a.repo_url = b.url
                WHERE repo_url = ? AND a.status IN ({placeholders})
                """,
                    params,
                )
            else:
                cursor.execute(
                    f"""
                SELECT 
                    a.id, a.url, a.repo_url, a.repo_name, a.error, a.status, a.timestamp, b.output AS repo_output 
                FROM {DB_NAME_CONTRIBUTOR} a
                LEFT JOIN {DB_NAME_REPO} b 
                    ON a.repo_url = b.url
                WHERE a.status IN ({placeholders})
                """,
                    tuple(status),
                )

            for row in cursor.fetchall():
                data.append(
                    TGitHubContributorJoinLog(
                        id=row[0],
                        url=row[1],
                        repo_url=row[2],
                        repo_name=row[3],
                        error=row[4],
                        status=row[5],
                        timestamp=row[6],
                        output=row[7],
                    )
                )

    except sqlite3.Error as err:
        logging.error(f'❌ ERROR_DB in "contributor.load()": {err}')

    return data


@db_retry_lock
def load_batch(status: list[str]) -> list[TGitHubContributorBatchLog]:

    data: list[TGitHubContributorBatchLog] = []

    try:
        with sqlite3.connect(DB_FILEPATH) as connection:
            cursor = connection.cursor()

            placeholders = ", ".join("?" for _ in status)

            cursor.execute(
                f"""
            SELECT a.repo_url, a.repo_name, MAX(b.output) AS repo_output 
            FROM {DB_NAME_CONTRIBUTOR} a
            LEFT JOIN {DB_NAME_REPO} b 
                ON a.repo_url = b.url
            WHERE a.status IN ({placeholders})
            GROUP BY a.repo_url
            """,
                tuple(status),  # Pass statuses as separate parameters
            )

            for row in cursor.fetchall():
                data.append(
                    TGitHubContributorBatchLog(
                        repo_url=row[0], repo_name=row[1], repo_output=row[2]
                    )
                )

    except sqlite3.Error as err:
        logging.error(f'❌ ERROR_DB in "load_batch()": {err}')

    return data

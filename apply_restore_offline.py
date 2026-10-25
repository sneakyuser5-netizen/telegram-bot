import os
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path

LIVE_DB = Path("database.db")
RESTORE_DB = Path("database_restored.db")
REPLACEMENT_DB = Path("database.db.replacement")

REQUIRED_COLUMNS = {
    "users": {
        "user_id", "referrals", "referred_by",
        "reward_unlocked", "joined_at",
    },
    "downloads": {"category", "count"},
    "files": {"id", "category", "size", "file_id", "created_at"},
}


def validate_database(path):
    if not path.is_file() or path.stat().st_size == 0:
        return False, "Database file is missing or empty."

    conn = None
    try:
        uri = path.resolve().as_uri() + "?mode=ro"
        conn = sqlite3.connect(uri, uri=True)

        result = conn.execute("PRAGMA integrity_check").fetchone()
        if not result or result[0] != "ok":
            return False, "SQLite integrity check failed."

        tables = {
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }

        for table, required in REQUIRED_COLUMNS.items():
            if table not in tables:
                return False, f"Missing table: {table}"

            columns = {
                row[1]
                for row in conn.execute(
                    f'PRAGMA table_info("{table}")'
                )
            }

            if not required.issubset(columns):
                return False, f"Required columns missing in {table}."

        return True, "Database is valid."

    except (sqlite3.Error, OSError, ValueError):
        return False, "Could not read or validate the database."
    finally:
        if conn is not None:
            conn.close()

def main():
    if not RESTORE_DB.is_file():
        raise SystemExit(
            "STOP: database_restored.db is missing. "
            "Use /restoredb to upload and validate a backup first."
        )

    if not LIVE_DB.is_file():
        raise SystemExit(
            "STOP: database.db is missing. "
            "Do not proceed without reviewing the recovery situation."
        )

    for sidecar in (
        Path("database.db-wal"),
        Path("database.db-shm"),
    ):
        if sidecar.exists():
            raise SystemExit(
                f"STOP: {sidecar} exists. Ensure the bot is fully stopped "
                "and investigate the SQLite sidecar before restoring. "
                "Do not delete the sidecar manually."
            )

    print("This operation will replace the live database.")
    print("The current database will be backed up first.")
    print("Ensure the Telegram bot and every other database user are stopped.")

    if input('Type STOPPED to confirm the bot is fully stopped: ').strip() != "STOPPED":
        raise SystemExit("Cancelled. No database changes made.")

    valid, reason = validate_database(RESTORE_DB)
    if not valid:
        raise SystemExit(f"STOP: staged database rejected: {reason}")

    valid, reason = validate_database(LIVE_DB)
    if not valid:
        raise SystemExit(
            f"STOP: current database failed validation: {reason}. "
            "The original has not been replaced."
        )

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = Path(f"database.db.pre-restore-{stamp}")

    if REPLACEMENT_DB.exists():
        raise SystemExit(
            f"STOP: {REPLACEMENT_DB} already exists. "
            "Inspect it before retrying."
        )

    try:
        # Preserve the current database before preparing the replacement.
        shutil.copy2(LIVE_DB, backup)

        valid, reason = validate_database(backup)
        if not valid:
            raise RuntimeError(
                f"Current database backup failed validation: {reason}"
            )

        # Prepare and validate the replacement on the same filesystem.
        shutil.copy2(RESTORE_DB, REPLACEMENT_DB)

        valid, reason = validate_database(REPLACEMENT_DB)
        if not valid:
            raise RuntimeError(
                f"Replacement failed validation: {reason}"
            )

        os.replace(REPLACEMENT_DB, LIVE_DB)

        print("SUCCESS: restored database installed.")
        print(f"Previous database backup: {backup}")
        print("The staged restore file was retained.")
        print("Restart the bot only after reviewing this result.")

    except Exception as exc:
        if REPLACEMENT_DB.exists():
            REPLACEMENT_DB.unlink()

        raise SystemExit(
            f"Restore did not complete normally ({type(exc).__name__}). "
            f"Check {backup} and the live database before retrying."
        )


if __name__ == "__main__":
    main()

"""Import the existing JSON data into the SQLite project database."""

from pathlib import Path

from db.database import DB_PATH, get_connection, initialize_database
from storage import load_json


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def import_json_data() -> None:
    """Replace SQLite rows with the current JSON data."""
    employees = load_json(DATA_DIR / "employees.json", [])
    requests = load_json(DATA_DIR / "requests.json", [])
    categories = load_json(DATA_DIR / "categories.json", [])
    statuses = load_json(DATA_DIR / "statuses.json", [])

    category_codes = {item["name"]: item["code"] for item in categories}
    status_codes = {item["name"]: item["code"] for item in statuses}

    request_rows = []
    for item in requests:
        if item["type"] not in category_codes:
            raise ValueError(f"Unknown request category: {item['type']}")
        if item["status"] not in status_codes:
            raise ValueError(f"Unknown request status: {item['status']}")
        request_rows.append(
            (
                item["id"],
                item["employee_id"],
                category_codes[item["type"]],
                status_codes[item["status"]],
                item["date"],
            )
        )

    initialize_database(DB_PATH)
    connection = get_connection(DB_PATH)
    try:
        connection.execute("DELETE FROM requests")
        connection.execute("DELETE FROM employees")
        connection.execute("DELETE FROM categories")
        connection.execute("DELETE FROM statuses")
        connection.executemany(
            "INSERT INTO employees (id, fio, department, age) "
            "VALUES (?, ?, ?, ?)",
            [
                (
                    item["id"],
                    item["fio"],
                    item["department"],
                    item["age"],
                )
                for item in employees
            ],
        )
        connection.executemany(
            "INSERT INTO categories (code, name) VALUES (?, ?)",
            [(item["code"], item["name"]) for item in categories],
        )
        connection.executemany(
            "INSERT INTO statuses (code, name) VALUES (?, ?)",
            [(item["code"], item["name"]) for item in statuses],
        )
        connection.executemany(
            """INSERT INTO requests
               (id, employee_id, category_code, status_code, date)
               VALUES (?, ?, ?, ?, ?)""",
            request_rows,
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    print(f"Database created: {DB_PATH}")
    print(
        "Imported: "
        f"{len(employees)} employees, {len(requests)} requests, "
        f"{len(categories)} categories, {len(statuses)} statuses."
    )


if __name__ == "__main__":
    import_json_data()

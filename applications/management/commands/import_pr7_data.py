import sqlite3
from datetime import date
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from applications.models import Category, Request, Status
from employees_web.models import Employee


class Command(BaseCommand):
    help = (
        "Copy records from the PR7 SQLite database "
        "into the Django ORM database."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--source",
            default=str(
                Path(settings.BASE_DIR) / "data" / "application_track.sqlite"
            ),
            help="Path to the untouched SQLite database created in PR7.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        source = Path(options["source"]).resolve()
        if not source.is_file():
            raise CommandError(f"Source database not found: {source}")

        try:
            connection = sqlite3.connect(
                f"file:{source.as_posix()}?mode=ro", uri=True
            )
            connection.row_factory = sqlite3.Row
            with connection:
                source_employees = connection.execute(
                    "SELECT id, fio, department, age "
                    "FROM employees ORDER BY id"
                ).fetchall()
                source_categories = connection.execute(
                    "SELECT code, name FROM categories ORDER BY code"
                ).fetchall()
                source_statuses = connection.execute(
                    "SELECT code, name FROM statuses ORDER BY code"
                ).fetchall()
                source_requests = connection.execute(
                    "SELECT id, employee_id, category_code, status_code, date "
                    "FROM requests ORDER BY id"
                ).fetchall()
                foreign_key_errors = connection.execute(
                    "PRAGMA foreign_key_check"
                ).fetchall()
            connection.close()
        except sqlite3.Error as error:
            raise CommandError(
                f"Cannot read source database: {error}"
            ) from error

        if foreign_key_errors:
            raise CommandError(
                "Source database contains invalid foreign-key references."
            )

        for row in source_categories:
            Category.objects.update_or_create(
                code=row["code"], defaults={"name": row["name"]}
            )
        for row in source_statuses:
            Status.objects.update_or_create(
                code=row["code"], defaults={"name": row["name"]}
            )
        for row in source_employees:
            Employee.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "fio": row["fio"],
                    "department": row["department"],
                    "age": row["age"],
                },
            )
        for row in source_requests:
            try:
                request_date = date.fromisoformat(row["date"])
            except ValueError as error:
                raise CommandError(
                    "Invalid date in source request "
                    f"{row['id']}: {row['date']}"
                ) from error
            Request.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "employee_id": row["employee_id"],
                    "category_id": row["category_code"],
                    "status_id": row["status_code"],
                    "date": request_date,
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Imported "
                f"{Employee.objects.count()} employees, "
                f"{Category.objects.count()} categories, "
                f"{Status.objects.count()} statuses and "
                f"{Request.objects.count()} requests."
            )
        )

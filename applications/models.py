from django.db import models

from employees_web.models import Employee


class RequestQuerySet(models.QuerySet):
    def active(self):
        """Requests still being processed, including additional review."""
        return self.exclude(status_id__in=("5", Status.WITHDRAWN_CODE))

    def rejected(self):
        return self.filter(status_id="5")

    def withdrawn(self):
        return self.filter(status_id=Status.WITHDRAWN_CODE)


class Category(models.Model):
    code = models.CharField(
        max_length=12, primary_key=True, verbose_name="Код"
    )
    name = models.CharField(
        max_length=120, unique=True, verbose_name="Название"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Категория заявления"
        verbose_name_plural = "Категории заявлений"

    def __str__(self) -> str:
        return self.name


class Status(models.Model):
    WITHDRAWN_CODE = "7"

    code = models.CharField(
        max_length=12, primary_key=True, verbose_name="Код"
    )
    name = models.CharField(
        max_length=200, unique=True, verbose_name="Название"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Статус заявления"
        verbose_name_plural = "Статусы заявлений"

    def __str__(self) -> str:
        return self.name


class Request(models.Model):
    objects = RequestQuerySet.as_manager()

    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="requests",
        verbose_name="Сотрудник",
    )
    category = models.ForeignKey(
        Category,
        to_field="code",
        db_column="category_code",
        on_delete=models.PROTECT,
        related_name="requests",
        verbose_name="Тип заявления",
    )
    status = models.ForeignKey(
        Status,
        to_field="code",
        db_column="status_code",
        on_delete=models.PROTECT,
        related_name="requests",
        verbose_name="Статус",
    )
    date = models.DateField(verbose_name="Дата подачи")

    class Meta:
        ordering = ["-date", "-pk"]
        verbose_name = "Кадровое заявление"
        verbose_name_plural = "Кадровые заявления"

    def __str__(self) -> str:
        return f"Заявление №{self.pk} — {self.category} ({self.employee})"

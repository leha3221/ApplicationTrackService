from django.db import models

from employees_web.models import Employee


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

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Employee(models.Model):
    fio = models.CharField(max_length=200, verbose_name="ФИО")
    department = models.CharField(max_length=120, verbose_name="Подразделение")
    age = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(120)],
        verbose_name="Возраст",
    )

    class Meta:
        ordering = ["fio", "pk"]
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(age__gte=1, age__lte=120),
                name="employee_age_between_1_and_120",
            )
        ]

    def __str__(self) -> str:
        return self.fio

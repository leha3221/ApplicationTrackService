from django import forms
from django.utils import timezone

from employees_web.models import Employee

from .models import Category, Request, Status


class RequestFilterForm(forms.Form):
    SORT_CHOICES = (
        ("-date", "Сначала новые"),
        ("date", "Сначала старые"),
        ("employee", "Сотрудник А–Я"),
        ("-employee", "Сотрудник Я–А"),
        ("category", "Тип А–Я"),
        ("-category", "Тип Я–А"),
    )

    q = forms.CharField(
        label="Поиск",
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "ФИО, тип или статус",
            }
        ),
    )
    category = forms.ModelChoiceField(
        label="Тип заявления",
        queryset=Category.objects.order_by("name"),
        required=False,
        empty_label="Все типы",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    status = forms.ModelChoiceField(
        label="Статус",
        queryset=Status.objects.order_by("name"),
        required=False,
        empty_label="Все статусы",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    employee = forms.ModelChoiceField(
        label="Сотрудник",
        queryset=Employee.objects.order_by("fio"),
        required=False,
        empty_label="Все сотрудники",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    date = forms.DateField(
        label="Дата заявления",
        required=False,
        input_formats=("%Y-%m-%d",),
        widget=forms.DateInput(
            attrs={"class": "form-control", "type": "date"},
            format="%Y-%m-%d",
        ),
    )
    exclude_rejected = forms.BooleanField(
        label="Исключить отклонённые",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    sort = forms.ChoiceField(
        label="Сортировка",
        choices=SORT_CHOICES,
        required=False,
        initial="-date",
        widget=forms.Select(attrs={"class": "form-select"}),
    )


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ("employee", "category", "date")
        labels = {
            "employee": "Сотрудник",
            "category": "Тип заявления",
            "date": "Дата подачи",
        }
        widgets = {
            "employee": forms.Select(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"},
                format="%Y-%m-%d",
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"].initial = timezone.localdate()

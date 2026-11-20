from datetime import date

from django.contrib import admin
from django.test import Client, TestCase
from django.urls import reverse

from employees_web.models import Employee

from .forms import RequestFilterForm
from .models import Category, Request, Status


class RequestFormsAndViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.employee = Employee.objects.create(
            fio="Тестовый Сотрудник", department="Кадры", age=30
        )
        cls.minor = Employee.objects.create(
            fio="Несовершеннолетний Сотрудник", department="Стажёры", age=17
        )
        cls.category = Category.objects.create(code="1", name="Отпуск")
        cls.second_category = Category.objects.create(code="2", name="Перевод")
        cls.status = Status.objects.create(
            code="1", name="На согласовании у руководителя"
        )
        cls.second_status = Status.objects.create(
            code="2", name="На согласовании у HR"
        )
        cls.rejected = Status.objects.create(
            code="5", name="Отклонено: сотрудник младше 18 лет"
        )
        Status.objects.create(
            code="6", name="Требуется дополнительная проверка (возраст > 70)"
        )
        cls.withdrawn, _ = Status.objects.get_or_create(
            code=Status.WITHDRAWN_CODE,
            defaults={"name": "Отозвано сотрудником"},
        )

    def test_filter_form_rejects_invalid_date_and_object_ids(self):
        form = RequestFilterForm({"date": "не-дата", "employee": "999"})

        self.assertFalse(form.is_valid())
        self.assertIn("date", form.errors)
        self.assertIn("employee", form.errors)

    def test_request_list_displays_form_errors_without_crashing(self):
        response = self.client.get(
            reverse("applications:list"),
            {"date": "не-дата", "employee": "нет"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["filter_form"].errors)

    def test_create_request_uses_age_and_category_rules(self):
        response = self.client.post(
            reverse("applications:create"),
            {
                "employee": self.employee.pk,
                "category": self.category.pk,
                "date": "2026-11-20",
            },
        )

        self.assertEqual(response.status_code, 302)
        item = Request.objects.get(employee=self.employee)
        self.assertEqual(item.status, self.status)
        self.assertEqual(item.date, date(2026, 11, 20))

        self.client.post(
            reverse("applications:create"),
            {
                "employee": self.minor.pk,
                "category": self.category.pk,
                "date": "2026-11-20",
            },
        )
        minor_request = Request.objects.get(employee=self.minor)
        self.assertEqual(minor_request.status, self.rejected)

    def test_edit_preserves_current_status(self):
        item = Request.objects.create(
            employee=self.employee,
            category=self.category,
            status=self.second_status,
            date=date(2026, 11, 1),
        )

        response = self.client.post(
            reverse("applications:update", args=(item.pk,)),
            {
                "employee": self.employee.pk,
                "category": self.second_category.pk,
                "date": "2026-11-02",
            },
        )

        self.assertEqual(response.status_code, 302)
        item.refresh_from_db()
        self.assertEqual(item.category, self.second_category)
        self.assertEqual(item.status, self.second_status)
        self.assertEqual(item.date, date(2026, 11, 2))

    def test_withdrawal_requires_post_and_updates_status(self):
        item = Request.objects.create(
            employee=self.employee,
            category=self.category,
            status=self.status,
            date=date(2026, 11, 1),
        )
        url = reverse("applications:withdraw", args=(item.pk,))

        self.assertEqual(self.client.get(url).status_code, 405)
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        item.refresh_from_db()
        self.assertEqual(item.status, self.withdrawn)

    def test_withdrawal_post_requires_csrf_token(self):
        item = Request.objects.create(
            employee=self.employee,
            category=self.category,
            status=self.status,
            date=date(2026, 11, 1),
        )
        client = Client(enforce_csrf_checks=True)
        url = reverse("applications:withdraw", args=(item.pk,))
        page = client.get(reverse("applications:detail", args=(item.pk,)))

        self.assertEqual(client.post(url).status_code, 403)
        token = page.cookies["csrftoken"].value
        self.assertEqual(
            client.post(url, {"csrfmiddlewaretoken": token}).status_code, 302
        )

    def test_request_manager_partitions_working_and_withdrawn_requests(self):
        active = Request.objects.create(
            employee=self.employee,
            category=self.category,
            status=self.status,
            date=date(2026, 11, 1),
        )
        Request.objects.create(
            employee=self.minor,
            category=self.category,
            status=self.rejected,
            date=date(2026, 11, 2),
        )
        withdrawn = Request.objects.create(
            employee=self.minor,
            category=self.category,
            status=self.withdrawn,
            date=date(2026, 11, 3),
        )

        self.assertQuerySetEqual(Request.objects.active(), [active])
        self.assertQuerySetEqual(Request.objects.rejected(), [
            Request.objects.get(status=self.rejected)
        ])
        self.assertQuerySetEqual(Request.objects.withdrawn(), [withdrawn])

    def test_all_domain_models_are_registered_in_admin(self):
        self.assertTrue(admin.site.is_registered(Employee))
        self.assertTrue(admin.site.is_registered(Category))
        self.assertTrue(admin.site.is_registered(Status))
        self.assertTrue(admin.site.is_registered(Request))

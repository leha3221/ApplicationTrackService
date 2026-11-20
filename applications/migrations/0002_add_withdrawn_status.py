from django.db import migrations


def add_withdrawn_status(apps, schema_editor):
    Status = apps.get_model("applications", "Status")
    Status.objects.using(schema_editor.connection.alias).get_or_create(
        code="7", defaults={"name": "Отозвано сотрудником"}
    )


class Migration(migrations.Migration):
    dependencies = [("applications", "0001_initial")]

    operations = [
        migrations.RunPython(add_withdrawn_status, migrations.RunPython.noop)
    ]

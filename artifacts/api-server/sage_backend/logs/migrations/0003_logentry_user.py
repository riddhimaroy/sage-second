from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def assign_entry_users_from_daily_log(apps, schema_editor):
    LogEntry = apps.get_model("logs", "LogEntry")

    for entry in LogEntry.objects.select_related("daily_log__user").all():
        if entry.daily_log_id and entry.daily_log.user_id and entry.user_id != entry.daily_log.user_id:
            # FIXED
            entry.user_id = entry.daily_log.user_id
            entry.save(update_fields=["user"])


class Migration(migrations.Migration):

    dependencies = [
        ("logs", "0002_dailylog_user_unique"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="logentry",
            name="user",
            field=models.ForeignKey(
                # ADDED
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="log_entries",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(assign_entry_users_from_daily_log, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="logentry",
            name="user",
            field=models.ForeignKey(
                # FIXED
                on_delete=django.db.models.deletion.CASCADE,
                related_name="log_entries",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def assign_existing_logs_to_first_user(apps, schema_editor):
    DailyLog = apps.get_model("logs", "DailyLog")
    User = apps.get_model("auth", "User")

    first_user = User.objects.order_by("id").first()
    if not first_user:
        return

    # FIXED: attach pre-existing shared logs to one existing user so migration can complete
    DailyLog.objects.filter(user__isnull=True).update(user=first_user)


class Migration(migrations.Migration):

    dependencies = [
        ("logs", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="dailylog",
            name="user",
            field=models.ForeignKey(
                # ADDED
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="daily_logs",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(assign_existing_logs_to_first_user, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="dailylog",
            name="user",
            field=models.ForeignKey(
                # FIXED
                on_delete=django.db.models.deletion.CASCADE,
                related_name="daily_logs",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="dailylog",
            name="date",
            field=models.CharField(
                # FIXED
                help_text="Date in YYYY-MM-DD format",
                max_length=10,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="dailylog",
            # ADDED
            unique_together={("user", "date")},
        ),
    ]

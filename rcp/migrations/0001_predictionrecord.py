from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PredictionRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("model_key", models.CharField(max_length=32)),
                ("inputs", models.JSONField()),
                ("predicted_class", models.PositiveSmallIntegerField()),
                ("predicted_severity", models.CharField(max_length=16)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]

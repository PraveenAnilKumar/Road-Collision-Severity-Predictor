from django.db import models


class PredictionRecord(models.Model):
    """A submitted collision scenario and the severity predicted for it."""

    created_at = models.DateTimeField(auto_now_add=True)
    model_key = models.CharField(max_length=32)
    inputs = models.JSONField()
    predicted_class = models.PositiveSmallIntegerField()
    predicted_severity = models.CharField(max_length=16)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.predicted_severity} prediction ({self.created_at:%Y-%m-%d %H:%M})"

# Create your models here.

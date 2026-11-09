from django.contrib import admin

from .models import PredictionRecord


@admin.register(PredictionRecord)
class PredictionRecordAdmin(admin.ModelAdmin):
    list_display = ("created_at", "predicted_severity", "model_key")
    list_filter = ("predicted_severity", "model_key", "created_at")
    search_fields = ("predicted_severity", "model_key")
    readonly_fields = ("created_at", "model_key", "inputs", "predicted_class", "predicted_severity")

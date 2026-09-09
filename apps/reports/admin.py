"""Reports Django Admin."""
from django.contrib import admin
from apps.reports.models import GeneratedReportRecord

@admin.register(GeneratedReportRecord)
class GeneratedReportRecordAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_type', 'format', 'generated_by', 'created_at')
    list_filter = ('report_type', 'format', 'created_at')
    readonly_fields = ('title', 'report_type', 'format', 'generated_by', 'created_at')

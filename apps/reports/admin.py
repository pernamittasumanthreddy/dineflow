from django.contrib import admin

from .models import ReportDefinition, ReportExecution, ReportExport, ReportSchedule


class ReportExportInline(admin.TabularInline):
    model = ReportExport
    extra = 0


@admin.register(ReportDefinition)
class ReportDefinitionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'report_category', 'is_active']
    list_filter = ['report_category', 'is_active']


@admin.register(ReportExecution)
class ReportExecutionAdmin(admin.ModelAdmin):
    list_display = ['report_definition', 'branch', 'status', 'execution_duration_seconds', 'created_at']
    list_filter = ['status', 'branch', 'created_at']
    inlines = [ReportExportInline]


@admin.register(ReportSchedule)
class ReportScheduleAdmin(admin.ModelAdmin):
    list_display = ['report_definition', 'branch', 'frequency', 'next_run_at', 'is_active']
    list_filter = ['frequency', 'is_active']

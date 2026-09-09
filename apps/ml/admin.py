from django.contrib import admin
from .models import (
    MLDataset, MLFeature, MLModel,
    MLModelVersion, MLTrainingRun, MLPrediction
)


class MLFeatureInline(admin.TabularInline):
    model = MLFeature
    extra = 0


@admin.register(MLDataset)
class MLDatasetAdmin(admin.ModelAdmin):
    list_display = ['name', 'dataset_type', 'row_count', 'created_at']
    list_filter = ['dataset_type']
    inlines = [MLFeatureInline]


class MLModelVersionInline(admin.TabularInline):
    model = MLModelVersion
    extra = 0


@admin.register(MLModel)
class MLModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'model_type', 'is_active']
    inlines = [MLModelVersionInline]


@admin.register(MLModelVersion)
class MLModelVersionAdmin(admin.ModelAdmin):
    list_display = ['model', 'version_tag', 'algorithm', 'is_deployed', 'created_at']
    list_filter = ['is_deployed', 'algorithm']


@admin.register(MLTrainingRun)
class MLTrainingRunAdmin(admin.ModelAdmin):
    list_display = ['model_version', 'dataset', 'status', 'evaluation_score', 'start_time']
    list_filter = ['status', 'start_time']


@admin.register(MLPrediction)
class MLPredictionAdmin(admin.ModelAdmin):
    list_display = ['model_version', 'confidence_score', 'created_at']
    list_filter = ['model_version']

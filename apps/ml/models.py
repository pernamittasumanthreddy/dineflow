from django.db import models
from django.utils import timezone

from apps.core.models import BaseModel


class MLDataset(BaseModel):
    DATASET_TYPES = [
        ('SALES_DEMAND', 'Sales Demand Forecasting'),
        ('CHURN_PREDICTION', 'Customer Churn'),
        ('WASTE_ESTIMATION', 'Kitchen Waste Estimation'),
    ]

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    dataset_type = models.CharField(max_length=30, choices=DATASET_TYPES)
    row_count = models.PositiveIntegerField(default=0)
    feature_schema = models.JSONField(default=dict)
    source_reference = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'df_ml_datasets'
        verbose_name = 'ML Dataset'
        verbose_name_plural = 'ML Datasets'

    def __str__(self):
        return f"{self.name} ({self.row_count} rows)"


class MLFeature(BaseModel):
    FEATURE_TYPES = [
        ('FLOAT', 'Float'),
        ('INT', 'Integer'),
        ('CATEGORICAL', 'Categorical'),
        ('BOOLEAN', 'Boolean'),
        ('DATETIME', 'Datetime'),
    ]

    dataset = models.ForeignKey(MLDataset, on_delete=models.CASCADE, related_name='features')
    name = models.CharField(max_length=100)
    data_type = models.CharField(max_length=50, choices=FEATURE_TYPES, default='FLOAT')
    is_target = models.BooleanField(default=False)
    importance_score = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)

    class Meta:
        db_table = 'df_ml_features'
        verbose_name = 'ML Feature'
        verbose_name_plural = 'ML Features'
        constraints = [
            models.UniqueConstraint(fields=['dataset', 'name'], name='unique_dataset_feature_name')
        ]

    def __str__(self):
        target = " [TARGET]" if self.is_target else ""
        return f"{self.name} ({self.data_type}){target}"


class MLModel(BaseModel):
    MODEL_TYPES = [
        ('REGRESSION', 'Regression'),
        ('CLASSIFICATION', 'Classification'),
        ('TIME_SERIES', 'Time Series Forecaster'),
        ('CLUSTERING', 'Clustering'),
    ]

    name = models.CharField(max_length=150, unique=True)
    model_type = models.CharField(max_length=50, choices=MODEL_TYPES, default='TIME_SERIES')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'df_ml_models'
        verbose_name = 'ML Model'
        verbose_name_plural = 'ML Models'

    def __str__(self):
        return f"{self.name} ({self.model_type})"


class MLModelVersion(BaseModel):
    model = models.ForeignKey(MLModel, on_delete=models.CASCADE, related_name='versions')
    version_tag = models.CharField(max_length=50)  # e.g., v1.0.0
    algorithm = models.CharField(max_length=100)  # e.g., RandomForestRegressor, XGBoost
    hyperparameters = models.JSONField(default=dict, blank=True)
    metrics = models.JSONField(default=dict, blank=True)
    weights_storage_path = models.CharField(max_length=255, blank=True)
    is_deployed = models.BooleanField(default=False)

    class Meta:
        db_table = 'df_ml_model_versions'
        verbose_name = 'ML Model Version'
        verbose_name_plural = 'ML Model Versions'
        constraints = [
            models.UniqueConstraint(fields=['model', 'version_tag'], name='unique_model_version_tag')
        ]

    def __str__(self):
        status = " [DEPLOYED]" if self.is_deployed else ""
        return f"{self.model.name} {self.version_tag} ({self.algorithm}){status}"


class MLTrainingRun(BaseModel):
    STATUS_CHOICES = [
        ('RUNNING', 'Running'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    model_version = models.ForeignKey(MLModelVersion, on_delete=models.CASCADE, related_name='training_runs')
    dataset = models.ForeignKey(MLDataset, on_delete=models.PROTECT, related_name='training_runs')
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='COMPLETED')
    training_logs = models.TextField(blank=True)
    evaluation_score = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)

    class Meta:
        db_table = 'df_ml_training_runs'
        verbose_name = 'ML Training Run'
        verbose_name_plural = 'ML Training Runs'

    def __str__(self):
        return f"Run for {self.model_version.model.name} {self.model_version.version_tag} [{self.status}]"


class MLPrediction(BaseModel):
    model_version = models.ForeignKey(MLModelVersion, on_delete=models.CASCADE, related_name='predictions')
    input_features = models.JSONField(default=dict)
    prediction_result = models.JSONField(default=dict)
    confidence_score = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    actual_outcome = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'df_ml_predictions'
        verbose_name = 'ML Prediction'
        verbose_name_plural = 'ML Predictions'
        indexes = [
            models.Index(fields=['model_version', 'created_at']),
        ]

    def __str__(self):
        return f"Prediction by {self.model_version.model.name} at {self.created_at}"

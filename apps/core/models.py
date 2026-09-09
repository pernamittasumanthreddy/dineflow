"""Core Abstract Models and Utilities."""
import uuid
from decimal import Decimal
from django.db import models

class TimeStampedModel(models.Model):
    """Abstract base model that provides self-updating created_at and updated_at fields."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

class UUIDModel(models.Model):
    """Abstract base model providing a UUID primary key."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

class ActiveManager(models.Manager):
    """Manager returning only active records."""
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class SoftDeleteModel(models.Model):
    """Abstract model enabling soft-deletion."""
    is_active = models.BooleanField(default=True, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()
    active_objects = ActiveManager()

    class Meta:
        abstract = True

    def soft_delete(self):
        from django.utils import timezone
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_active', 'deleted_at'])

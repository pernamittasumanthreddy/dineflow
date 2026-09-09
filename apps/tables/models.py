"""Restaurant Floor Plan and Dining Table Models."""
from django.db import models
from apps.core.models import TimeStampedModel, SoftDeleteModel

class TableStatus(models.TextChoices):
    AVAILABLE = 'AVAILABLE', 'Available'
    OCCUPIED = 'OCCUPIED', 'Occupied'
    RESERVED = 'RESERVED', 'Reserved'
    CLEANING = 'CLEANING', 'Cleaning'
    MAINTENANCE = 'MAINTENANCE', 'Maintenance'

class FloorSection(TimeStampedModel, SoftDeleteModel):
    """Dining areas / zones (Main AC Hall, Rooftop Garden, Family Courtyard, Banquet)."""
    branch = models.ForeignKey(
        'branches.Branch',
        on_delete=models.CASCADE,
        related_name='floor_sections'
    )
    name = models.CharField('Section Name', max_length=100)
    floor_number = models.IntegerField('Floor Level', default=0)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Floor Section'
        verbose_name_plural = 'Floor Sections'
        ordering = ['floor_number', 'name']

    def __str__(self):
        return f"{self.name} (Floor {self.floor_number}) - {self.branch.name}"

class RestaurantTable(TimeStampedModel, SoftDeleteModel):
    """Individual dining table entity with live occupancy status."""
    branch = models.ForeignKey(
        'branches.Branch',
        on_delete=models.CASCADE,
        related_name='tables'
    )
    section = models.ForeignKey(
        FloorSection,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tables'
    )
    table_number = models.CharField('Table #', max_length=30)
    seating_capacity = models.PositiveIntegerField('Capacity', default=4)
    status = models.CharField(
        'Occupancy Status',
        max_length=20,
        choices=TableStatus.choices,
        default=TableStatus.AVAILABLE,
        db_index=True
    )
    current_order = models.ForeignKey(
        'orders.Order',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='occupied_table'
    )
    pos_x = models.IntegerField('Grid X Position', default=0)
    pos_y = models.IntegerField('Grid Y Position', default=0)

    class Meta:
        verbose_name = 'Restaurant Table'
        verbose_name_plural = 'Restaurant Tables'
        ordering = ['table_number']
        unique_together = ('branch', 'table_number')

    def __str__(self):
        return f"Table {self.table_number} ({self.seating_capacity} seats) - [{self.get_status_display()}]"

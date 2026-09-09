"""Kitchen Display System (KDS), Station Routing, and Prep SLA Analytics Models."""
from django.db import models
from django.utils import timezone
from apps.core.models import TimeStampedModel

class KitchenStation(models.TextChoices):
    ALL = 'ALL', 'Main Kitchen / All Stations'
    BIRYANI_CURRY = 'BIRYANI_CURRY', 'Biryani & Curry Section'
    TANDOOR_GRILL = 'TANDOOR_GRILL', 'Tandoor & Starters Station'
    DOSA_SOUTH = 'DOSA_SOUTH', 'South Indian & Tiffin Station'
    BEVERAGES = 'BEVERAGES', 'Beverages & Mocktails'
    DESSERT = 'DESSERT', 'Dessert Station'

class TicketStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending Cook'
    PREPARING = 'PREPARING', 'Cooking / In Progress'
    READY = 'READY', 'Ready for Expeditor'
    BUMPED = 'BUMPED', 'Served / Cleared'

class KitchenTicket(TimeStampedModel):
    """KDS digital order ticket tracking station prep SLAs and bump actions."""
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='kitchen_tickets')
    ticket_number = models.CharField('KOT #', max_length=50)
    station = models.CharField(max_length=30, choices=KitchenStation.choices, default=KitchenStation.ALL)
    status = models.CharField(
        max_length=20,
        choices=TicketStatus.choices,
        default=TicketStatus.PENDING,
        db_index=True
    )
    
    # SLA metrics
    expected_prep_minutes = models.PositiveIntegerField('Expected SLA (Mins)', default=15)
    started_cooking_at = models.DateTimeField(null=True, blank=True)
    completed_cooking_at = models.DateTimeField(null=True, blank=True)
    bumped_at = models.DateTimeField(null=True, blank=True)
    bumped_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bumped_tickets'
    )

    class Meta:
        verbose_name = 'Kitchen Ticket (KOT)'
        verbose_name_plural = 'Kitchen Tickets (KOTs)'
        ordering = ['created_at']

    def __str__(self):
        return f"KOT #{self.ticket_number} for Order #{self.order.order_number} [{self.status}]"

    @property
    def elapsed_minutes(self):
        """Calculate elapsed prep duration from ticket creation."""
        end_time = self.completed_cooking_at or timezone.now()
        start_time = self.started_cooking_at or self.created_at
        diff = end_time - start_time
        return max(0, int(diff.total_seconds() / 60))

    @property
    def is_delayed(self):
        """Returns True if the ticket has breached its expected preparation SLA."""
        if self.status in [TicketStatus.READY, TicketStatus.BUMPED]:
            return False
        return self.elapsed_minutes > self.expected_prep_minutes

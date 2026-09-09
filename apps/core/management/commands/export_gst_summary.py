"""Statutory Indian GST Audit & Summary Export Command."""
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db.models import Sum, Count
from django.utils import timezone
from apps.billing.models import Invoice

class Command(BaseCommand):
    help = 'Aggregates and prints statutory Indian GST SAC 9963 tax summary for a given month/year.'

    def add_arguments(self, parser):
        parser.add_argument('--month', type=int, default=timezone.localdate().month, help='Month (1-12)')
        parser.add_argument('--year', type=int, default=timezone.localdate().year, help='Year (e.g. 2026)')

    def handle(self, *args, **options):
        month = options['month']
        year = options['year']

        self.stdout.write(self.style.NOTICE(f"=== STATUTORY INDIAN GST RETURN SUMMARY: {month:02d}/{year} ==="))

        invoices = Invoice.objects.filter(
            created_at__year=year,
            created_at__month=month,
            is_paid=True
        )

        agg = invoices.aggregate(
            inv_count=Count('id'),
            tot_taxable=Sum('taxable_subtotal'),
            tot_cgst=Sum('cgst_amount'),
            tot_sgst=Sum('sgst_amount'),
            tot_igst=Sum('igst_amount'),
            tot_tax=Sum('total_tax_amount'),
            tot_grand=Sum('grand_total')
        )

        inv_count = agg['inv_count'] or 0
        tot_taxable = agg['tot_taxable'] or Decimal('0.00')
        tot_cgst = agg['tot_cgst'] or Decimal('0.00')
        tot_sgst = agg['tot_sgst'] or Decimal('0.00')
        tot_igst = agg['tot_igst'] or Decimal('0.00')
        tot_tax = agg['tot_tax'] or Decimal('0.00')
        tot_grand = agg['tot_grand'] or Decimal('0.00')

        self.stdout.write(f"Total Settled Tax Invoices   : {inv_count}")
        self.stdout.write(f"Aggregate Taxable Value (INR): {tot_taxable:,.2f}")
        self.stdout.write(f"Central GST (CGST 2.5%) (INR): {tot_cgst:,.2f}")
        self.stdout.write(f"State GST   (SGST 2.5%) (INR): {tot_sgst:,.2f}")
        self.stdout.write(f"Integrated  (IGST 5.0%) (INR): {tot_igst:,.2f}")
        self.stdout.write(f"Total GST Collected     (INR): {tot_tax:,.2f}")
        self.stdout.write(f"Invoice Gross Billed    (INR): {tot_grand:,.2f}")
        self.stdout.write(self.style.SUCCESS("=== END OF STATUTORY GST SUMMARY ==="))

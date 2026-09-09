"""Thermal Receipt Text & ESC/POS Generation Utility for POS Printers (80mm & 58mm)."""
from decimal import Decimal
from django.utils import timezone
from apps.core.utils import format_inr

ESC = b'\x1b'
GS = b'\x1d'

def generate_thermal_receipt_text(invoice, width_chars=48):
    """
    Generates a clean, precisely aligned plain-text receipt suitable for 80mm (48 chars)
    or 58mm (32 chars) thermal POS printers.
    """
    lines = []
    div = "=" * width_chars
    sdiv = "-" * width_chars

    # Center-aligned header
    lines.append(invoice.restaurant_name.center(width_chars))
    if invoice.branch_address:
        lines.append(invoice.branch_address[:width_chars].center(width_chars))
    lines.append(f"GSTIN: {invoice.restaurant_gstin}".center(width_chars))
    lines.append(f"FSSAI Lic: {invoice.fssai_number}".center(width_chars))
    lines.append(div)
    
    # Bill metadata
    lines.append(f"Invoice #: {invoice.invoice_number}")
    dt_str = timezone.localtime(invoice.created_at).strftime('%d/%m/%Y %I:%M %p')
    lines.append(f"Date/Time: {dt_str}")
    if invoice.order and invoice.order.table:
        lines.append(f"Table: {invoice.order.table.table_number} | Server: {invoice.order.server.first_name if invoice.order.server else 'Counter'}")
    if invoice.customer:
        lines.append(f"Guest: {invoice.customer.name} ({invoice.customer.phone})")
    lines.append(sdiv)

    # Itemized header
    # 48 chars: QTY (4) ITEM (26) PRICE (8) TOTAL (10)
    qty_w = 4
    total_w = 10
    price_w = 8
    item_w = width_chars - qty_w - total_w - price_w - 3

    hdr = f"{'QTY':<{qty_w}} {'ITEM':<{item_w}} {'RATE':>{price_w}} {'TOTAL':>{total_w}}"
    lines.append(hdr)
    lines.append(sdiv)

    for it in invoice.items.all():
        name = it.item_name[:item_w]
        rate_str = f"{it.unit_rate:.2f}"
        tot_str = f"{it.item_total:.2f}"
        lines.append(f"{it.quantity:<{qty_w}} {name:<{item_w}} {rate_str:>{price_w}} {tot_str:>{total_w}}")

    lines.append(sdiv)

    # Financial totals
    def align_row(label, val):
        val_str = f"{val:.2f}"
        space = width_chars - len(label) - len(val_str)
        return f"{label}{' ' * max(1, space)}{val_str}"

    lines.append(align_row("Subtotal (Taxable):", invoice.taxable_subtotal))
    if invoice.discount_amount > Decimal('0.00'):
        lines.append(align_row("Discount Applied:", -invoice.discount_amount))
    if invoice.cgst_amount > Decimal('0.00'):
        lines.append(align_row("CGST (2.5%):", invoice.cgst_amount))
    if invoice.sgst_amount > Decimal('0.00'):
        lines.append(align_row("SGST (2.5%):", invoice.sgst_amount))
    if invoice.igst_amount > Decimal('0.00'):
        lines.append(align_row("IGST (5.0%):", invoice.igst_amount))
    
    lines.append(div)
    grand_str = f"GRAND TOTAL: {format_inr(invoice.grand_total)}"
    lines.append(grand_str.center(width_chars))
    lines.append(f"Payment Method: {invoice.payment_method}".center(width_chars))
    lines.append(div)

    # Footer note
    lines.append("Thank you for dining with us!".center(width_chars))
    lines.append("Have a wonderful day!".center(width_chars))
    lines.append("\n\n")

    return "\n".join(lines)

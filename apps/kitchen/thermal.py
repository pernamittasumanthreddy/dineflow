"""Kitchen Order Ticket (KOT) Thermal Slip Generation for KDS & Kitchen Printers."""
from django.utils import timezone

def generate_kot_slip_text(ticket, width_chars=40):
    """
    Formats a Kitchen Order Ticket slip for station printers.
    """
    lines = []
    div = "=" * width_chars
    sdiv = "-" * width_chars

    lines.append("KITCHEN ORDER TICKET (KOT)".center(width_chars))
    lines.append(div)
    lines.append(f"KOT #: {ticket.ticket_number}")
    lines.append(f"Order #: {ticket.order.order_number}")
    if ticket.order.table:
        lines.append(f"TABLE: {ticket.order.table.table_number}")
    lines.append(f"Station: {ticket.get_station_display()}")
    dt_str = timezone.localtime(ticket.created_at).strftime('%H:%M:%S')
    lines.append(f"Time Fired: {dt_str} | SLA: {ticket.expected_prep_minutes} mins")
    lines.append(sdiv)

    # Line items
    qty_w = 4
    item_w = width_chars - qty_w - 1
    lines.append(f"{'QTY':<{qty_w}} {'DISH / SPECIAL NOTES':<{item_w}}")
    lines.append(sdiv)

    for item in ticket.order.items.all():
        lines.append(f"{item.quantity:<{qty_w}} {item.menu_item.name:<{item_w}}")
        if item.kitchen_notes:
            lines.append(f"     * NOTE: {item.kitchen_notes}")

    lines.append(div)
    if ticket.order.special_instructions:
        lines.append(f"INSTRUCTIONS: {ticket.order.special_instructions}")
        lines.append(div)
        
    lines.append("\n\n")
    return "\n".join(lines)

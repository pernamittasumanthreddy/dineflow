"""Enterprise PDF (ReportLab) and Excel (OpenPyXL) Regulatory Report Services."""
import io
from decimal import Decimal
from django.utils import timezone
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from apps.orders.models import Order, OrderStatus
from apps.billing.models import Invoice
from apps.inventory.models import Ingredient
from apps.payroll.models import Payroll
from apps.restaurants.models import Restaurant
from apps.core.utils import format_inr

def generate_sales_pdf(start_date, end_date, branch=None):
    """Generates a boardroom-ready luxury PDF Sales & Revenue report using ReportLab."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0f172a')
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#64748b')
    )
    section_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#b45309')
    )
    
    restaurant = Restaurant.objects.first()
    rest_name = restaurant.name if restaurant else "DineFlow Hospitality"
    gstin = restaurant.gstin if restaurant else "36AAACN1234F1Z9"
    
    # Header
    story.append(Paragraph(rest_name, title_style))
    story.append(Paragraph(f"Statutory Sales & Revenue Audit | GSTIN: {gstin}", subtitle_style))
    story.append(Paragraph(f"Reporting Window: {start_date} to {end_date} | Generated: {timezone.now().strftime('%d-%b-%Y %H:%M')}", subtitle_style))
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#d97706'), spaceAfter=15))
    
    # Financial Query
    orders = Order.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date,
        status=OrderStatus.COMPLETED
    )
    if branch:
        orders = orders.filter(branch=branch)
        
    total_gross = sum(o.subtotal for o in orders)
    total_tax = sum(o.tax_amount for o in orders)
    total_discount = sum(o.discount_amount for o in orders)
    total_net = sum(o.grand_total for o in orders)
    order_count = orders.count()

    # Metric Table
    metric_data = [
        ['Total Completed Orders', str(order_count), 'Taxable Subtotal', format_inr(total_gross)],
        ['Discounts Availed', format_inr(total_discount), 'GST Tax (CGST+SGST)', format_inr(total_tax)],
        ['Net Settled Revenue', format_inr(total_net), 'Average Order Value', format_inr(total_net / order_count if order_count else 0)],
    ]
    t_metrics = Table(metric_data, colWidths=[130, 130, 130, 130])
    t_metrics.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#1e293b')),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
    ]))
    story.append(t_metrics)
    story.append(Spacer(1, 20))

    # Invoices Table
    story.append(Paragraph("Recent Settled Invoices Breakdown", section_style))
    story.append(Spacer(1, 8))
    
    invoices = Invoice.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date,
        is_paid=True
    ).select_related('order', 'customer')[:25]

    inv_headers = ['Invoice #', 'Date', 'Customer', 'Taxable (₹)', 'GST (₹)', 'Grand Total (₹)']
    inv_rows = [inv_headers]
    for inv in invoices:
        cust_name = inv.customer.name if inv.customer else "Walk-in Guest"
        inv_rows.append([
            inv.invoice_number,
            inv.created_at.strftime('%d-%b-%y'),
            cust_name[:18],
            f"₹{inv.taxable_subtotal}",
            f"₹{inv.total_tax_amount}",
            f"₹{inv.grand_total}"
        ])

    t_invoices = Table(inv_rows, colWidths=[100, 70, 130, 75, 65, 80])
    t_invoices.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8.5),
        ('ALIGN', (3,0), (-1,-1), 'RIGHT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('FONTSIZE', (0,1), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_invoices)

    doc.build(story)
    buffer.seek(0)
    return buffer

def generate_gstr1_excel(start_date, end_date, branch=None):
    """Generates statutory Indian GSTR-1 B2C / B2B sales return in Excel format via OpenPyXL."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "GSTR-1 B2CS (Restaurant)"

    # Header styling
    header_fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    data_font = Font(name="Calibri", size=10)
    border = Border(
        left=Side(style='thin', color='CBD5E1'),
        right=Side(style='thin', color='CBD5E1'),
        top=Side(style='thin', color='CBD5E1'),
        bottom=Side(style='thin', color='CBD5E1')
    )

    headers = [
        "Invoice Number", "Invoice Date", "Invoice Value", "Place of Supply",
        "Reverse Charge", "Rate (%)", "Taxable Value (₹)", "CGST (₹)", "SGST (₹)", "IGST (₹)"
    ]
    ws.append(headers)

    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    invoices = Invoice.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date
    ).select_related('order', 'branch')

    if branch:
        invoices = invoices.filter(branch=branch)

    for inv in invoices:
        row = [
            inv.invoice_number,
            inv.created_at.strftime('%Y-%m-%d'),
            float(inv.grand_total),
            inv.branch.state,
            "N",
            5.0,
            float(inv.taxable_subtotal),
            float(inv.cgst_amount),
            float(inv.sgst_amount),
            float(inv.igst_amount)
        ]
        ws.append(row)

    # Column widths
    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = openpyxl.utils.get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer

def generate_inventory_valuation_excel(branch=None):
    """Generates Stock Ledger & Valuation Sheet in Excel via OpenPyXL."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Inventory Valuation"

    header_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")

    headers = ["SKU / Code", "Ingredient Name", "Category", "Current Stock", "Unit", "Reorder Level", "Unit Cost (₹)", "Total Stock Value (₹)", "Status"]
    ws.append(headers)

    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")

    ingredients = Ingredient.objects.filter(is_active=True).select_related('category', 'branch')
    if branch:
        ingredients = ingredients.filter(branch=branch)

    for ing in ingredients:
        status_label = "LOW STOCK" if ing.is_low_stock else "NORMAL"
        row = [
            ing.code or "—",
            ing.name,
            ing.category.name if ing.category else "General",
            float(ing.current_stock),
            ing.unit,
            float(ing.minimum_stock_level),
            float(ing.unit_cost),
            float(ing.stock_value),
            status_label
        ]
        ws.append(row)

    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = openpyxl.utils.get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = max(max_len + 3, 14)

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer

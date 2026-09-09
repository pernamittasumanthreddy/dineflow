"""Report Export Streaming Endpoints (PDF & Excel)."""
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
from django.utils import timezone
from apps.reports.models import GeneratedReportRecord
from apps.reports.services import generate_sales_pdf, generate_gstr1_excel, generate_inventory_valuation_excel
from apps.accounts.decorators import module_permission_required

@login_required
@module_permission_required('reports')
def reports_index_view(request):
    """Reporting Hub with report generation triggers and historical archives."""
    today = timezone.localdate()
    start_of_month = today.replace(day=1)
    
    recent_reports = GeneratedReportRecord.objects.all().select_related('generated_by')[:10]

    return render(request, 'reports/index.html', {
        'recent_reports': recent_reports,
        'default_start': start_of_month,
        'default_end': today,
    })

@login_required
@module_permission_required('reports')
def export_sales_pdf_view(request):
    """Streams statutory sales audit report in PDF format."""
    today = timezone.localdate()
    start_date = request.GET.get('start_date', str(today.replace(day=1)))
    end_date = request.GET.get('end_date', str(today))
    branch = request.user.branch

    pdf_buffer = generate_sales_pdf(start_date=start_date, end_date=end_date, branch=branch)
    
    GeneratedReportRecord.objects.create(
        title=f"Sales Audit Report ({start_date} to {end_date})",
        report_type='SALES_PDF',
        format='PDF',
        generated_by=request.user
    )

    response = HttpResponse(pdf_buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="DineFlow_Sales_Audit_{start_date}_{end_date}.pdf"'
    return response

@login_required
@module_permission_required('reports')
def export_gstr1_excel_view(request):
    """Streams Indian GST GSTR-1 return in Excel format."""
    today = timezone.localdate()
    start_date = request.GET.get('start_date', str(today.replace(day=1)))
    end_date = request.GET.get('end_date', str(today))
    branch = request.user.branch

    excel_buffer = generate_gstr1_excel(start_date=start_date, end_date=end_date, branch=branch)
    
    GeneratedReportRecord.objects.create(
        title=f"GSTR-1 Return ({start_date} to {end_date})",
        report_type='GSTR1_EXCEL',
        format='EXCEL',
        generated_by=request.user
    )

    response = HttpResponse(
        excel_buffer.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="DineFlow_GSTR1_{start_date}_{end_date}.xlsx"'
    return response

@login_required
@module_permission_required('reports')
def export_inventory_excel_view(request):
    """Streams inventory valuation and stock levels in Excel format."""
    branch = request.user.branch
    today = timezone.localdate()

    excel_buffer = generate_inventory_valuation_excel(branch=branch)
    
    GeneratedReportRecord.objects.create(
        title=f"Inventory Stock Valuation ({today})",
        report_type='INVENTORY_EXCEL',
        format='EXCEL',
        generated_by=request.user
    )

    response = HttpResponse(
        excel_buffer.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="DineFlow_Inventory_Valuation_{today}.xlsx"'
    return response

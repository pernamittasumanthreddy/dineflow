from django.shortcuts import render

def business_bi(request):
    """
    Multi-Branch Business Intelligence & Revenue Analytics.
    """
    branch_bi = [
        {'branch': 'Indiranagar Main (Bangalore)', 'gross_sales': 1485000.00, 'cogs': 415800.00, 'food_cost_pct': '28.0%', 'labor_cost': 245000.00, 'operating_profit': 584200.00, 'margin': '39.3%'},
        {'branch': 'Banjara Hills Flagship (Hyderabad)', 'gross_sales': 1240000.00, 'cogs': 359600.00, 'food_cost_pct': '29.0%', 'labor_cost': 210000.00, 'operating_profit': 470400.00, 'margin': '37.9%'},
        {'branch': 'Connaught Place (New Delhi)', 'gross_sales': 890000.00, 'cogs': 267000.00, 'food_cost_pct': '30.0%', 'labor_cost': 165000.00, 'operating_profit': 318000.00, 'margin': '35.7%'},
        {'branch': 'Anna Nagar Central (Chennai)', 'gross_sales': 640000.00, 'cogs': 179200.00, 'food_cost_pct': '28.0%', 'labor_cost': 120000.00, 'operating_profit': 240800.00, 'margin': '37.6%'},
    ]
    context = {
        'page_title': 'Multi-Branch Business Intelligence',
        'branch_bi': branch_bi
    }
    return render(request, 'analytics/business_bi.html', context)

def ml_demand(request):
    """
    AI Machine Learning Demand Forecast & Ingredient Depletion Predictor.
    """
    predictions = [
        {'dish': 'Hyderabadi Chicken Dum Biryani', 'weekday_avg': '65 Handis', 'predicted_weekend': '140 Handis (+115%)', 'raw_meat_req': '35.0 kg Chicken', 'rice_req': '25.2 kg Basmati', 'confidence': '96.4% Accuracy'},
        {'dish': 'Paneer Butter Masala', 'weekday_avg': '42 Portions', 'predicted_weekend': '88 Portions (+109%)', 'raw_meat_req': '17.6 kg Paneer', 'rice_req': '-', 'confidence': '94.8% Accuracy'},
        {'dish': 'Butter Garlic Naan', 'weekday_avg': '110 Pcs', 'predicted_weekend': '280 Pcs (+154%)', 'raw_meat_req': '-', 'rice_req': '18.0 kg Maida / Butter', 'confidence': '98.2% Accuracy'},
        {'dish': 'Special Mutton Handi Biryani', 'weekday_avg': '28 Handis', 'predicted_weekend': '72 Handis (+157%)', 'raw_meat_req': '28.8 kg Mutton', 'rice_req': '13.0 kg Basmati', 'confidence': '92.1% Accuracy'},
    ]
    context = {
        'page_title': 'AI Machine Learning Demand Forecast',
        'predictions': predictions
    }
    return render(request, 'analytics/ml_demand.html', context)

def tax_reports(request):
    """
    GSTR-1 & GSTR-3B Tax Filing Export Summaries.
    """
    gstr_data = [
        {'month': 'August 2026', 'b2c_taxable': 3657142.86, 'cgst_2_5': 91428.57, 'sgst_2_5': 91428.57, 'total_tax_paid': 182857.14, 'invoice_count': 2840, 'filing_status': 'Filed on 11/09/2026 ✓'},
        {'month': 'July 2026', 'b2c_taxable': 3428571.43, 'cgst_2_5': 85714.29, 'sgst_2_5': 85714.29, 'total_tax_paid': 171428.58, 'invoice_count': 2680, 'filing_status': 'Filed on 10/08/2026 ✓'},
        {'month': 'June 2026', 'b2c_taxable': 3142857.14, 'cgst_2_5': 78571.43, 'sgst_2_5': 78571.43, 'total_tax_paid': 157142.86, 'invoice_count': 2450, 'filing_status': 'Filed on 11/07/2026 ✓'},
    ]
    context = {
        'page_title': 'GSTR-1 & GSTR-3B Tax Reports',
        'gstr_data': gstr_data
    }
    return render(request, 'analytics/tax_reports.html', context)

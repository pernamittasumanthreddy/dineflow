from django.shortcuts import render

def index(request):
    """
    Public Landing Page for DineFlow Restaurant ERP.
    """
    testimonials = [
        {
            'name': 'Chef Sanjeev Teja',
            'role': 'Founder & Executive Chef',
            'restaurant': 'Andhra Spice Kitchen (Hyderabad & Bangalore)',
            'quote': 'DineFlow cut our table turnaround time by 32% and completely eliminated KOT errors between our service staff and the tandoor/curry stations.',
            'rating': 5,
            'avatar': 'ST'
        },
        {
            'name': 'Anjali Sharma',
            'role': 'Director of Operations',
            'restaurant': 'Coastal Curry House & Tiffin Chain (Chennai)',
            'quote': 'The built-in Indian GST invoicing with 80mm thermal receipt printing and automated GSTR-1 export saves our accounting team 20+ hours every month.',
            'rating': 5,
            'avatar': 'AS'
        },
        {
            'name': 'Arjun Varma',
            'role': 'Managing Partner',
            'restaurant': 'Bengaluru Brew & Bites (Indiranagar)',
            'quote': 'Managing 4 branches, 120 staff members, and real-time raw material inventory with automatic low-stock WhatsApp alerts has never been this seamless.',
            'rating': 5,
            'avatar': 'AV'
        }
    ]

    pricing_plans = [
        {
            'name': 'Single Outlet Pro',
            'tagline': 'Ideal for independent fine-dining restaurants & standalone cafes',
            'price': '₹2,499',
            'period': 'per month billed annually',
            'featured': False,
            'features': [
                '1 Restaurant Branch (Unlimited Tables)',
                'High-Speed Touch POS & Quick Billing',
                'Live Kitchen Display System (KDS)',
                'Indian GST & FSSAI Compliant Invoicing',
                'Recipe Management & Menu Costing',
                'Daily Day-End Z-Reports',
                '24/7 Dedicated Phone & WhatsApp Support'
            ],
            'button_text': 'Start 14-Day Free Trial',
            'button_class': 'df-btn-outline'
        },
        {
            'name': 'Multi-Chain Enterprise',
            'tagline': 'Engineered for restaurant chains, multi-outlet brands & cloud kitchens',
            'price': '₹5,999',
            'period': 'per branch/month billed annually',
            'featured': True,
            'features': [
                'Unlimited Outlets & Centralized Chain BI',
                'Omnichannel Aggregator Sync (Swiggy / Zomato)',
                'Advanced Raw Material Inventory & Auto-PO',
                'Complete HRMS, Attendance & Indian Payroll',
                'AI/ML Demand & Spoilage Prediction',
                'White-Label Loyalty Points & WhatsApp CRM',
                'Automated GSTR-1 & GSTR-3B Tax Filing Feeds',
                'Dedicated Account Manager & Hardware Onboarding'
            ],
            'button_text': 'Get Started Enterprise 🚀',
            'button_class': 'df-btn-terracotta'
        },
        {
            'name': 'Cloud Kitchen Network',
            'tagline': 'Built for high-velocity multi-brand dark kitchens & food courts',
            'price': '₹4,499',
            'period': 'per kitchen hub/month',
            'featured': False,
            'features': [
                'Multi-Brand Virtual Kitchen Routing',
                'Multi-Station KDS & Bump Bar Support',
                'In-House Delivery Fleet & Rider App',
                'Real-Time Food Costing & Margin Control',
                'Direct Web Ordering & Digital QR Menus',
                'Automated Ingredient Depletion Tracking'
            ],
            'button_text': 'Contact Sales Team',
            'button_class': 'df-btn-outline'
        }
    ]

    modules_showcase = [
        {'num': '01', 'name': 'Multi-Role Auth & RBAC', 'icon': '🔐'},
        {'num': '02', 'name': 'Touch POS Terminal', 'icon': '💻'},
        {'num': '03', 'name': 'Kitchen Display (KDS)', 'icon': '🔥'},
        {'num': '04', 'name': 'Interactive Floor Plan', 'icon': '🪑'},
        {'num': '05', 'name': 'Table Reservations', 'icon': '📅'},
        {'num': '06', 'name': 'Menu & Recipe Costing', 'icon': '📜'},
        {'num': '07', 'name': 'Omnichannel Orders', 'icon': '🛍️'},
        {'num': '08', 'name': 'Raw Material Inventory', 'icon': '📦'},
        {'num': '09', 'name': 'Purchase Orders & GRN', 'icon': '📝'},
        {'num': '10', 'name': 'Suppliers & Vendors', 'icon': '🏭'},
        {'num': '11', 'name': 'GST Invoicing & Billing', 'icon': '🧾'},
        {'num': '12', 'name': 'Staff Directory & HRMS', 'icon': '👥'},
        {'num': '13', 'name': 'Biometric Attendance', 'icon': '⏱️'},
        {'num': '14', 'name': 'Shift Rosters & Leaves', 'icon': '🔄'},
        {'num': '15', 'name': 'Indian Payroll & Slips', 'icon': '💰'},
        {'num': '16', 'name': 'Customer CRM & Visits', 'icon': '🤝'},
        {'num': '17', 'name': 'Loyalty & Reward Club', 'icon': '🎁'},
        {'num': '18', 'name': 'Offers & Promo Codes', 'icon': '🎟️'},
        {'num': '19', 'name': 'Customer Feedback QR', 'icon': '💬'},
        {'num': '20', 'name': 'Delivery Fleet Dispatch', 'icon': '🛵'},
        {'num': '21', 'name': 'Petty Cash & Expenses', 'icon': '💸'},
        {'num': '22', 'name': 'GST Rates & SAC Slabs', 'icon': '⚖️'},
        {'num': '23', 'name': 'Day-End Z-Report', 'icon': '🌙'},
        {'num': '24', 'name': 'Waste & Spoilage Log', 'icon': '🗑️'},
        {'num': '25', 'name': 'Multi-Branch BI Reports', 'icon': '📊'},
        {'num': '26', 'name': 'AI Demand Prediction', 'icon': '🧠'},
        {'num': '27', 'name': 'GSTR-1 / 3B Tax Exports', 'icon': '📑'},
        {'num': '28', 'name': 'Branch Management', 'icon': '🏢'},
        {'num': '29', 'name': 'Audit Logs & Security', 'icon': '🕵️'},
        {'num': '30', 'name': 'Database Backup & Restore', 'icon': '💾'},
        {'num': '31', 'name': 'Kitchen Station Routing', 'icon': '🍳'},
        {'num': '32', 'name': 'Dynamic UPI QR Billing', 'icon': '📱'},
        {'num': '33', 'name': 'Customer Digital Menu', 'icon': '⭐'},
        {'num': '34', 'name': 'Order Cancellation & Void', 'icon': '❌'},
        {'num': '35', 'name': 'System Hardware Settings', 'icon': '⚙️'}
    ]

    context = {
        'testimonials': testimonials,
        'pricing_plans': pricing_plans,
        'modules_showcase': modules_showcase
    }
    return render(request, 'landing/index.html', context)

from django.shortcuts import render


def home(request):
    activities = [
        {"title": "New enterprise account created", "time": "2 minutes ago", "dot_color": "bg-emerald-400"},
        {"title": "Revenue report generated", "time": "14 minutes ago", "dot_color": "bg-brand-400"},
        {"title": "Background sync completed", "time": "31 minutes ago", "dot_color": "bg-amber-400"},
        {"title": "Admin permissions updated", "time": "1 hour ago", "dot_color": "bg-rose-400"},
    ]

    table_rows = [
        {"name": "Acme Inc.", "reference": "INV-1001", "amount": "$2,450.00", "status": "Paid", "status_class": "bg-emerald-500/10 text-emerald-300", "date": "2026-03-18"},
        {"name": "Vertex Labs", "reference": "INV-1002", "amount": "$1,120.00", "status": "Pending", "status_class": "bg-amber-500/10 text-amber-300", "date": "2026-03-17"},
        {"name": "Nova Retail", "reference": "INV-1003", "amount": "$4,980.00", "status": "Overdue", "status_class": "bg-rose-500/10 text-rose-300", "date": "2026-03-16"},
        {"name": "BluePeak", "reference": "INV-1004", "amount": "$890.00", "status": "Processing", "status_class": "bg-cyan-500/10 text-cyan-300", "date": "2026-03-15"},
    ]

    return render(request, 'dashboard/home.html', {
        'activities': activities,
        'table_rows': table_rows,
    })


def analytics(request):
    analytics_activities = [
        {"title": "Audience segments refreshed", "time": "10 minutes ago", "dot_color": "bg-brand-400"},
        {"title": "Attribution model recalculated", "time": "42 minutes ago", "dot_color": "bg-cyan-400"},
        {"title": "Weekly insight digest published", "time": "Today", "dot_color": "bg-emerald-400"},
    ]
    return render(request, 'dashboard/analytics.html', {
        'analytics_activities': analytics_activities,
    })


def reports(request):
    report_activities = [
        {"title": "Q1 executive report exported", "time": "1 hour ago", "dot_color": "bg-emerald-400"},
        {"title": "Operations report scheduled", "time": "Today", "dot_color": "bg-brand-400"},
        {"title": "Retention report shared", "time": "Yesterday", "dot_color": "bg-cyan-400"},
    ]
    report_rows = [
        {"name": "Finance Team", "reference": "RPT-201", "amount": "Weekly", "status": "Active", "status_class": "bg-emerald-500/10 text-emerald-300", "date": "Every Monday"},
        {"name": "Operations", "reference": "RPT-202", "amount": "Daily", "status": "Running", "status_class": "bg-cyan-500/10 text-cyan-300", "date": "08:00 AM"},
        {"name": "Marketing", "reference": "RPT-203", "amount": "Monthly", "status": "Draft", "status_class": "bg-amber-500/10 text-amber-300", "date": "1st day"},
    ]
    return render(request, 'dashboard/reports.html', {
        'report_activities': report_activities,
        'report_rows': report_rows,
    })


def users(request):
    user_rows = [
        {"name": "Sarah Johnson", "reference": "USR-1001", "amount": "Admin", "status": "Active", "status_class": "bg-emerald-500/10 text-emerald-300", "date": "2026-03-20"},
        {"name": "Omar Khalid", "reference": "USR-1002", "amount": "Editor", "status": "Pending", "status_class": "bg-amber-500/10 text-amber-300", "date": "2026-03-19"},
        {"name": "Lina Chen", "reference": "USR-1003", "amount": "Viewer", "status": "Suspended", "status_class": "bg-rose-500/10 text-rose-300", "date": "2026-03-18"},
        {"name": "David Kim", "reference": "USR-1004", "amount": "Manager", "status": "Active", "status_class": "bg-cyan-500/10 text-cyan-300", "date": "2026-03-17"},
    ]
    return render(request, 'dashboard/users.html', {
        'user_rows': user_rows,
    })
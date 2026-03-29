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


from django.shortcuts import render
from urllib.parse import urlencode


def metrics(request):
    active_group = request.GET.get("group", "performance")
    active_period = request.GET.get("period", "FY")
    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")

    period_options = [
        "1D", "7D", "MTD", "TM" , "LM", "YTD", "YTG", "FY", "LY",  "12M", 
    ]

    dashboard_groups = [
        {
            "key": "performance",
            "label": "Performance",
            "cards": [
                {
                    "card_key": "room_revenue",
                    "card_title": "Room Revenue",
                    "icon_svg": "revenue",
                    "options": [
                        {
                            "key": "revenue",
                            "label": "Revenue",
                            "unit": "currency",
                            "total": 12450000,
                            "budget": 16500000,
                            "forecast": 13800000,
                            "same_time_last_year": 13100000,
                            "last_year_actual": 12650000,
                        },
                        {
                            "key": "revpar",
                            "label": "RevPAR",
                            "unit": "currency",
                            "total": 542.75,
                            "budget": 575.20,
                            "forecast": 558.40,
                            "same_time_last_year": 552.80,
                            "last_year_actual": 548.10,
                        },
                    ],
                },
                {
                    "card_key": "business_volume",
                    "card_title": "Business Volume",
                    "icon_svg": "volume",
                    "options": [
                        {
                            "key": "occupancy",
                            "label": "Occupancy",
                            "unit": "percent",
                            "total": 78.40,
                            "budget": 82.50,
                            "forecast": 80.90,
                            "same_time_last_year": 79.60,
                            "last_year_actual": 79.10,
                        },
                        {
                            "key": "nights",
                            "label": "Nights",
                            "unit": "count",
                            "total": 4832,
                            "budget": 5250,
                            "forecast": 5030,
                            "same_time_last_year": 4920,
                            "last_year_actual": 4885,
                        },
                    ],
                },
                {
                    "card_key": "room_rate",
                    "card_title": "Room Rate",
                    "icon_svg": "rate",
                    "options": [
                        {
                            "key": "adr",
                            "label": "Average Rate",
                            "unit": "currency",
                            "total": 692.35,
                            "budget": 715.00,
                            "forecast": 704.20,
                            "same_time_last_year": 698.80,
                            "last_year_actual": 695.40,
                        }
                    ],
                },
            ],
        }
    ]

    chart_data = {
        "categories": [
            "2025-01-01",
            "2025-01-02",
            "2025-01-03",
            "2025-01-04",
            "2025-01-05",
            "2025-01-06",
            "2025-01-07",
            "2025-01-08",
            "2025-01-09",
            "2025-01-10",
            "2025-01-11",
            "2025-01-12",
            "2025-01-13",
            "2025-01-14",
            "2025-01-15",
            "2025-01-16",
            "2025-01-17",
            "2025-01-18",
            "2025-01-19",
            "2025-01-20",
            "2025-01-21",
            "2025-01-22",
            "2025-01-23",
            "2025-01-24",
            "2025-01-25",
            "2025-01-26",
            "2025-01-27",
            "2025-01-28",
            "2025-01-29",
            "2025-01-30",
            "2025-01-31",
        ],
        "series": {
            "occupancy": [
                72, 73, 71, 74, 75, 76, 74,
                73, 75, 77, 78, 76, 74, 75,
                77, 79, 80, 78, 77, 76, 78,
                79, 81, 80, 78, 77, 79, 80,
                82, 81, 83
            ],
            "revenue": [
                9800000, 9950000, 9700000, 10150000, 10300000, 10420000, 10200000,
                10050000, 10380000, 10650000, 10820000, 10540000, 10360000, 10480000,
                10720000, 11050000, 11200000, 10980000, 10850000, 10700000, 10920000,
                11150000, 11400000, 11320000, 11080000, 10960000, 11250000, 11400000,
                11680000, 11590000, 11850000
            ],
            "adr": [
                628.4, 631.2, 625.8, 636.1, 640.8, 645.0, 639.4,
                634.2, 642.7, 651.4, 659.8, 648.5, 643.0, 646.2,
                654.6, 665.1, 672.4, 666.0, 661.8, 657.1, 663.0,
                671.5, 680.2, 676.8, 669.0, 664.7, 673.4, 679.6,
                688.1, 684.9, 692.4
            ],
            "revpar": [
                452.4, 460.8, 444.3, 470.7, 480.6, 490.2, 472.9,
                463.0, 482.0, 501.6, 514.6, 492.9, 475.8, 484.7,
                504.0, 525.4, 537.9, 519.5, 509.6, 499.4, 517.1,
                530.5, 550.9, 541.4, 521.8, 511.8, 532.0, 543.7,
                564.2, 554.8, 574.7
            ],
            "same_time_last_year": [
                69, 70, 68, 70, 71, 72, 71,
                70, 71, 73, 74, 73, 71, 72,
                73, 75, 76, 75, 74, 73, 74,
                75, 77, 76, 75, 74, 75, 76,
                78, 77, 78
            ]
        }
    }

    groups_map = {group["key"]: group for group in dashboard_groups}
    current_group = groups_map.get(active_group, dashboard_groups[0])

    is_custom_range = bool(start_date and end_date)

    current_state = {
        "group": current_group["key"],
        "period": active_period,
        "start_date": start_date,
        "end_date": end_date,
    }

    for card in current_group["cards"]:
        param_name = f"{card['card_key']}_metric"
        default_option_key = card["options"][0]["key"]
        requested_option_key = request.GET.get(param_name, default_option_key)

        selected_option = next(
            (opt for opt in card["options"] if opt["key"] == requested_option_key),
            card["options"][0],
        )

        card["active_option_key"] = selected_option["key"]
        card["active_option"] = selected_option
        current_state[param_name] = selected_option["key"]

    for card in current_group["cards"]:
        param_name = f"{card['card_key']}_metric"
        for option in card["options"]:
            state_for_option = current_state.copy()
            state_for_option[param_name] = option["key"]
            option["querystring"] = urlencode(state_for_option)

    period_links = []
    for period in period_options:
        state_for_period = current_state.copy()
        state_for_period["period"] = period
        state_for_period["start_date"] = ""
        state_for_period["end_date"] = ""

        period_links.append(
            {
                "label": period,
                "querystring": urlencode(state_for_period),
                "is_active": (period == active_period) and not is_custom_range,
            }
        )

    calendar_querystring = urlencode(current_state)

    context = {
        "groups": dashboard_groups,
        "active_group": current_group["key"],
        "current_group": current_group,
        "active_period": active_period,
        "period_links": period_links,
        "calendar_querystring": calendar_querystring,
        "start_date": start_date,
        "end_date": end_date,
        "is_custom_range": is_custom_range,
        "chart_data_json": chart_data,
    }

    return render(request, "dashboard/metrics.html", context)
from __future__ import unicode_literals
from frappe import _

def get_data():

    return [
        {
            "label": _("Transactions"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Sales Plan",
                    "onboard": 1
                },
                {
                    "type": "doctype",
                    "name": "Rejection Entry",
                    "onboard": 1
                },
                {
                    "type": "doctype",
                    "name": "Operator Entry",
                    "onboard": 1
                },
                {
                    "type": "doctype",
                    "name": "Sales Plan Ledger Entry",
                    "onboard": 1
                },
                {
                    "type": "doctype",
                    "name": "Production Allocation",
                    "onboard": 1
                },
                {
                    "type": "doctype",
                    "name": "Packing Box Labels",
                    "onboard": 1
                },
                {
                    "type": "doctype",
                    "name": "Operation Item Price List",
                    "onboard": 1
                }
            ]
        },
        {
            "label": _("Gate Inward and Outward"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Gate Inward",
                    "onboard": 1
                },
                {
                    "type": "doctype",
                    "name": "Gate Outward",
                    "onboard": 1
                }
            ]
        },
        {
            "label": _("Reports"),
            "items": [
                {
                    "type": "report",
					"is_query_report": True,
					"name": "INCOMING STORE - Delivery Report Daily",
					"doctype": "Material Request",
					"onboard": 1,
                },
                {
                    "type": "report",
					"is_query_report": True,
					"name": "FINAL STORE - Delivery Report Daily",
					"doctype": "Material Request",
					"onboard": 1,
                },
                {
                    "type": "report",
					"is_query_report": True,
					"name": "DESPATCH - Received Report Daily",
					"doctype": "Material Request",
					"onboard": 1,
                },
                {
                    "type": "report",
					"is_query_report": True,
					"name": "Despatch Details Report",
					"doctype": "Sales Plan",
					"onboard": 1,
                }
            ]
        },
        {
            "label": _("PDC-Reports"),
            "items": [
                {
                    "type": "report",
					"is_query_report": True,
					"name": "PDC - Production Report Shiftwise",
					"doctype": "Operator Entry",
					"onboard": 1,
                },
                {
                    "type": "report",
					"is_query_report": True,
					"name": "PDC - Production Report Daily",
					"doctype": "Operator Entry",
					"onboard": 1,
                }
            ]
        },
        {
            "label": _("Gate Inward-Reports"),
            "items": [
                {
                    "type": "report",
					"is_query_report": True,
					"name": "Gate Inward Register ( Purchase Order )",
					"doctype": "Gate Inward",
					"onboard": 1,
                },
                {
                    "type": "report",
					"is_query_report": True,
					"name": "Gate Inward Register (Job Work Order)",
					"doctype": "Gate Inward",
					"onboard": 1,
                },
                {
                    "type": "report",
					"is_query_report": True,
					"name": "Gate Inward Register (Bills)",
					"doctype": "Gate Inward",
					"onboard": 1,
                },
                {
                    "type": "report",
					"is_query_report": True,
					"name": "Gate Inward Register (Couriers)",
					"doctype": "Gate Inward",
					"onboard": 1,
                },
                {
                    "type": "report",
					"is_query_report": True,
					"name": "Gate Inward Register (Visitors)",
					"doctype": "Gate Inward",
					"onboard": 1,
                }
            ]
        }
    ]

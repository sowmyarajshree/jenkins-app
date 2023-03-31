// Copyright (c) 2023, Nxweb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Rate Work Entry Ledger"] = {
	"filters": [
		{
	        "fieldname":"project",
			"label": __("Project"),
			"fieldtype": "Link",
			"width": 250,
			"options":"Project"
		},
		{
	        "fieldname":"subcontractor",
			"label": __("Subcontractor"),
			"fieldtype": "Link",
			"width": 250,
			"options":"Supplier"
		},
		{
			"label": "From Date",
			"fieldname": "from_date",
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
		},
		{
			"label": "To Date",
			"fieldname": "to_date",
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
		}

	]
};

// Copyright (c) 2016, nxweb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Gate Inward Report"] = {
	"filters": [
		{
				"fieldname":"posting_date",
				"label": __("From Date"),
				"fieldtype": "Date",
				"width": "80",
				"default": frappe.datetime.month_start()
			},
			{
				"fieldname":"posting_date",
				"label": __("To Date"),
				"fieldtype": "Date",
				"width": "80",
				"default": frappe.datetime.month_end()
			}
		]
};

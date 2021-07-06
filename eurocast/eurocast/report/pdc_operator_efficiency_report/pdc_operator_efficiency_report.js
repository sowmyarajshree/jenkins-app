// Copyright (c) 2016, nxweb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["PDC Operator Efficiency Report"] = {
	"filters": [
		{
				"fieldname":"from_date",
				"label": __("From Date"),
				"fieldtype": "Date",
				"width": "80",
				"default": frappe.datetime.month_start()
			},
			{
				"fieldname":"to_date",
				"label": __("To Date"),
				"fieldtype": "Date",
				"width": "80",
				"default": frappe.datetime.month_end()
			}
		]
};

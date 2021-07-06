// Copyright (c) 2016, nxweb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["PDC - Production Report Shiftwise"] = {
	"filters": [
		{
			"fieldname": "posting_date",
			"label": __("Posting Date"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "shift_type",
			"label": __("Shift Type"),
			"fieldtype": "Link",
			"options": "Shift Type"
		}
	]
};

// Copyright (c) 2016, nxweb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["PDC - Production Report Daily"] = {
	"filters": [
		{
			"fieldname": "posting_date",
			"label": __("Date"),
			"fieldtype": "Date",
			"reqd": 1
		}
	]
};
